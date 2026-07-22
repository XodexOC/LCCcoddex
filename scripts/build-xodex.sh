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
    --bootappend-live "boot=live components hostname=xodex username=xodex locales=ru_RU.UTF-8,en_US.UTF-8 keyboard-layouts=us,ru timezone=UTC" \
    --binary-images iso-hybrid \
    --win32-loader false
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

  rsync -a --delete \
    --exclude '.git' \
    "${ROOT}/docs/" "${XDEST}/docs/" 2>/dev/null || cp -a "${ROOT}/docs" "${XDEST}/"
  rsync -a --delete \
    "${ROOT}/examples/" "${XDEST}/examples/" 2>/dev/null || cp -a "${ROOT}/examples" "${XDEST}/"
  rsync -a --delete \
    "${ROOT}/courses/" "${XDEST}/courses/" 2>/dev/null || cp -a "${ROOT}/courses" "${XDEST}/"
  rsync -a --delete \
    "${ROOT}/tools/" "${XDEST}/tools/" 2>/dev/null || cp -a "${ROOT}/tools" "${XDEST}/"

  # Menu on PATH
  install -m 0755 "${ROOT}/tools/xodex-menu" config/includes.chroot/usr/local/bin/xodex-menu

  # Copy short README into image
  install -m 0644 "${ROOT}/README.md" "${XDEST}/README.md"
  install -m 0644 "${ROOT}/README.ru.md" "${XDEST}/README.ru.md"
}

build_image() {
  info "lb build (this can take a long time)"
  cd "${BUILD_DIR}"
  lb build
  info "Build finished. Look for ISO under ${BUILD_DIR}/"
  ls -lh "${BUILD_DIR}/"*.iso 2>/dev/null || ls -lh "${BUILD_DIR}/" | head -50
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
