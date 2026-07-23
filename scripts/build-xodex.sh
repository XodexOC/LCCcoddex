#!/usr/bin/env bash
# Build Xodex Live ISO using Debian live-build.
# Run as root on Debian/Ubuntu. Does not push anywhere.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${BUILD_DIR:-${ROOT}/build}"
DIST="${DIST:-bookworm}"
ARCH="${ARCH:-amd64}"
IMAGE_NAME="${IMAGE_NAME:-xodex-live}"

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "==> $*"; }

need_root() {
  if [ "$(id -u)" -ne 0 ]; then
    die "Run as root: sudo $0 $*"
  fi
}

check_deps() {
  local missing=()
  for c in lb debootstrap mksquashfs xorriso; do
    command -v "${c}" >/dev/null 2>&1 || missing+=("${c}")
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    cat >&2 <<EOF
Missing tools: ${missing[*]}

Install on Debian/Ubuntu:
  sudo apt update
  sudo apt install -y live-build debootstrap squashfs-tools xorriso \\
    grub-pc-bin grub-efi-amd64-bin mtools isolinux syslinux-common
EOF
    exit 1
  fi
}

prepare_workspace() {
  info "Workspace: ${BUILD_DIR}"
  mkdir -p "${BUILD_DIR}"
  cd "${BUILD_DIR}"

  # Fresh config each full configure; keep cache if present for faster rebuilds
  if [ "${CLEAN:-0}" = "1" ]; then
    info "CLEAN=1 — removing previous build tree"
    lb clean --all 2>/dev/null || true
    rm -rf config binary* chroot* .stage cache 2>/dev/null || true
  fi

  info "lb config (${DIST} ${ARCH})"
  lb config \
    --mode debian \
    --distribution "${DIST}" \
    --architectures "${ARCH}" \
    --archive-areas "main contrib non-free non-free-firmware" \
    --apt-recommends false \
    --debian-installer false \
    --firmware-binary true \
    --firmware-chroot false \
    --iso-application "Xodex" \
    --iso-preparer "XodexOC" \
    --iso-publisher "XodexOC https://github.com/XodexOC/XodexOC" \
    --iso-volume "XODEX" \
    --security false \
    --bootappend-live "boot=live components hostname=xodex username=xodex locales=ru_RU.UTF-8,en_US.UTF-8 keyboard-layouts=us,ru timezone=UTC console=ttyS0,115200" \
    --binary-images iso-hybrid \
    --win32-loader false \
    --initsystem systemd
}

sync_config() {
  info "Sync package-lists, hooks, includes from core/"
  mkdir -p config/package-lists config/hooks/live config/includes.chroot config/archives

  # Add correct security archive (live-build on Ubuntu 24.04 generates wrong suite for Bookworm)
  cat > config/archives/security.list.chroot << 'SECEOF'
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
SECEOF
  cp config/archives/security.list.chroot config/archives/security.list.binary

  cp -a "${ROOT}/core/config/package-lists/." config/package-lists/
  cp -a "${ROOT}/core/config/hooks/live/." config/hooks/live/
  chmod +x config/hooks/live/*.chroot 2>/dev/null || true

  # Overlay includes
  if [ -d "${ROOT}/core/config/includes.chroot" ]; then
    cp -a "${ROOT}/core/config/includes.chroot/." config/includes.chroot/
  fi

  # Inject educational content into Live rootfs
  local XDEST="config/includes.chroot/usr/local/xodex"
  mkdir -p "${XDEST}" config/includes.chroot/usr/local/bin

  for subdir in docs examples courses tools; do
    local src="${ROOT}/${subdir}"
    if [ -d "${src}" ]; then
      rm -rf "${XDEST}/${subdir}"
      cp -a "${src}" "${XDEST}/"
    fi
  done

  # Session / Login / Menu on PATH
  install -m 0755 "${ROOT}/tools/xodex-session" config/includes.chroot/usr/local/bin/xodex-session
  install -m 0755 "${ROOT}/tools/xodex-login" config/includes.chroot/usr/local/bin/xodex-login
  install -m 0755 "${ROOT}/tools/xodex-menu" config/includes.chroot/usr/local/bin/xodex-menu

  # Copy syslinux bootloader templates
  local ISOLINUX_TMPL="/usr/share/live/build/bootloaders/isolinux"
  if [ -d "${ISOLINUX_TMPL}" ]; then
    mkdir -p config/bootloaders/isolinux
    cp -a "${ISOLINUX_TMPL}/." config/bootloaders/isolinux/
    # Remove splash.svg.in so lb_binary_syslinux doesn't try to process it
    rm -f config/bootloaders/isolinux/splash.svg.in
    # Create bootlogo placeholder (small cpio archive)
    mkdir -p /tmp/xodex-bootlogo
    echo "xodex" > /tmp/xodex-bootlogo/placeholder
    (cd /tmp/xodex-bootlogo && echo "placeholder" | cpio -o > "${BUILD_DIR}/config/bootloaders/isolinux/bootlogo" 2>/dev/null) || true
    rm -rf /tmp/xodex-bootlogo
  fi

  # Copy syslinux library modules required by isolinux 6.x
  local SYS_MODULES="/usr/lib/syslinux/modules/bios"
  if [ -d "${SYS_MODULES}" ]; then
    for mod in ldlinux.c32 libcom32.c32 libutil.c32 libmenu.c32 menu.c32; do
      if [ -f "${SYS_MODULES}/${mod}" ]; then
        install -m 0644 "${SYS_MODULES}/${mod}" config/bootloaders/isolinux/
      fi
    done
  fi

  # Custom isolinux.cfg — use text menu.c32 instead of vesamenu.c32
  cat > config/bootloaders/isolinux/isolinux.cfg << 'ISOLINUXCFG'
include menu.cfg
default menu.c32
prompt 0
timeout 50
ISOLINUXCFG

  # Custom live.cfg.in — without hardcoded 'boot=live config' (already in @LB_BOOTAPPEND_LIVE@)
  cat > config/bootloaders/isolinux/live.cfg.in << 'LIVECFG'
label live-@FLAVOUR@
	menu label ^Live (@FLAVOUR@)
	menu default
	kernel @KERNEL@
	append initrd=@INITRD@ @LB_BOOTAPPEND_LIVE@

label live-@FLAVOUR@-failsafe
	menu label ^Live (@FLAVOUR@ failsafe)
	menu default
	kernel @KERNEL@
	append initrd=@INITRD@ @LB_BOOTAPPEND_LIVE@ @LB_BOOTAPPEND_FAILSAFE@
LIVECFG

  # Copy short README into image
  install -m 0644 "${ROOT}/README.md" "${XDEST}/README.md"
  install -m 0644 "${ROOT}/README.ru.md" "${XDEST}/README.ru.md"
}

build_image() {
  info "lb build (this can take a long time)"
  cd "${BUILD_DIR}"
  lb build || true

  # The ISO is built inside chroot; find and hybridize it
  local ISO_SRC=""
  ISO_SRC=$(find "${BUILD_DIR}/chroot" -maxdepth 1 -name "*.hybrid.iso" -type f 2>/dev/null | head -1)
  if [ -n "${ISO_SRC}" ] && [ -f "${ISO_SRC}" ]; then
    info "Applying isohybrid to: ${ISO_SRC}"
    isohybrid "${ISO_SRC}" 2>/dev/null || true
    local ISO_DEST="${BUILD_DIR}/${IMAGE_NAME}-${ARCH}.iso"
    cp "${ISO_SRC}" "${ISO_DEST}"
    chmod 644 "${ISO_DEST}"
    info "ISO: ${ISO_DEST}"
    ls -lh "${ISO_DEST}"
  else
    info "Looking for ISO in binary/..."
    ls -lh "${BUILD_DIR}/"*.iso 2>/dev/null || ls -lh "${BUILD_DIR}/" | head -30
  fi
}

usage() {
  cat <<EOF
Usage: sudo $0 [configure|build|all|clean]

  configure  — lb config + sync Xodex files (default first step)
  build      — run lb build (requires prior configure)
  all        — configure + build (default)
  clean      — lb clean --all and remove build artifacts

Env:
  BUILD_DIR   default: ${ROOT}/build
  DIST        default: bookworm
  ARCH        default: amd64
  CLEAN=1     wipe build tree before configure
  IMAGE_NAME  default: xodex-live
EOF
}

main() {
  local cmd="${1:-all}"
  case "${cmd}" in
    -h|--help|help) usage; exit 0 ;;
  esac

  need_root
  check_deps

  case "${cmd}" in
    configure)
      prepare_workspace
      sync_config
      info "Configure done. Next: sudo $0 build"
      ;;
    build)
      [ -d "${BUILD_DIR}/config" ] || die "No config — run: sudo $0 configure"
      build_image
      ;;
    all)
      prepare_workspace
      sync_config
      build_image
      ;;
    clean)
      cd "${BUILD_DIR}" 2>/dev/null || exit 0
      lb clean --all 2>/dev/null || true
      info "Clean requested. BUILD_DIR=${BUILD_DIR}"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"
