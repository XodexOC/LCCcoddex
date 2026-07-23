#!/usr/bin/env bash
# Xodex Documentation Browser — browse markdown lessons with less
set -euo pipefail

DOCS_ROOT="${DOCS_ROOT:-${XODEX_HOME:-/usr/local/xodex}/docs}"
PAGER="${PAGER:-less}"
PROGRAM="$(basename "$0")"

usage() {
  cat >&2 <<EOF
Usage: ${PROGRAM} [command] [args]

Commands:
  list                    List all available tracks with lesson counts
  show <track> [level]    Show a track README or a specific lesson
  search <query>          Search across all lesson files
  (no args)               Interactive menu (fzf or numbered)

Examples:
  ${PROGRAM} list
  ${PROGRAM} show c
  ${PROGRAM} show c 04
  LANG=ru ${PROGRAM} show asm 00
  ${PROGRAM} search malloc
EOF
  exit 1
}

die() { echo "Error: $*" >&2; exit 1; }

# ----------------------------------------------------------------
#  Helpers
# ----------------------------------------------------------------

detect_lang() {
  local lang="${LANG:-${LC_ALL:-en_US}}"
  case "${lang,,}" in *ru*) echo "ru" ;; *) echo "en" ;; esac
}

# Best language directory for a track (tries ru if preferred, falls back to en)
lang_dir() {
  local track="$1" lang
  lang=$(detect_lang)
  if [ -d "${DOCS_ROOT}/${track}/${lang}" ]; then
    echo "${DOCS_ROOT}/${track}/${lang}"
  elif [ -d "${DOCS_ROOT}/${track}/en" ]; then
    echo "${DOCS_ROOT}/${track}/en"
  else
    echo ""
  fi
}

# Sorted list of track directory names beneath DOCS_ROOT
get_tracks() {
  local d
  for d in "${DOCS_ROOT}"/*/; do
    [ -d "$d" ] || continue
    local t; t=$(basename "$d")
    [[ "${t}" == @(en|ru) ]] && continue
    printf '%s\0' "${t}"
  done | sort -z | xargs -0 -n1 printf '%s\n'
}

# Number of lesson files (non-README .md) in a directory
lesson_count() {
  local dir="$1"
  find "${dir}" -maxdepth 1 -name '*.md' ! -name 'README.md' 2>/dev/null | wc -l
}

# Open a file with the pager
open_file() {
  local file="$1"
  [ -f "${file}" ] || die "File not found: ${file}"
  ${PAGER} "${file}"
}

# ----------------------------------------------------------------
#  Commands
# ----------------------------------------------------------------

cmd_list() {
  [ -d "${DOCS_ROOT}" ] || die "DOCS_ROOT not found: ${DOCS_ROOT}"
  local lang; lang=$(detect_lang)
  echo "Xodex Documentation Tracks  (lang=${lang})"
  echo "Root: ${DOCS_ROOT}"
  echo
  printf "  %-16s %s\n" "TRACK" "LESSONS"
  printf "  %-16s %s\n" "-----" "-------"
  local found=0
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    found=1
    local ld count
    ld=$(lang_dir "$t")
    if [ -n "$ld" ]; then
      count=$(lesson_count "$ld")
    else
      count=$(find "${DOCS_ROOT}/${t}" -maxdepth 1 -name '*.md' ! -name 'README.md' 2>/dev/null | wc -l)
    fi
    printf "  %-16s %d\n" "${t}" "${count}"
  done < <(get_tracks)
  [ "${found}" -eq 1 ] || echo "  (no tracks found)"
}

cmd_show() {
  [ $# -ge 1 ] || usage
  local track="$1" level="${2:-}"

  [ -d "${DOCS_ROOT}/${track}" ] || die "Track '${track}' not found in ${DOCS_ROOT}"
  local ld; ld=$(lang_dir "$track")
  [ -n "$ld" ] || die "No language directory found for track '${track}'"

  if [ -z "${level}" ]; then
    # Show track README
    local readme="${ld}/README.md"
    [ -f "${readme}" ] || die "No README.md for track '${track}' in ${ld}"
    open_file "${readme}"
  else
    # Show specific lesson — try exact, then .md, then glob prefix
    local matches=()
    if [ -f "${ld}/${level}" ]; then
      matches+=("${ld}/${level}")
    elif [ -f "${ld}/${level}.md" ]; then
      matches+=("${ld}/${level}.md")
    else
      while IFS= read -r -d '' f; do
        matches+=("$f")
      done < <(find "${ld}" -maxdepth 1 -name "${level}*.md" -print0 2>/dev/null)
    fi

    if [ ${#matches[@]} -eq 0 ]; then
      echo "No lesson matching '${level}' found in track '${track}'." >&2
      echo "Available lessons:" >&2
      while IFS= read -r -d '' f; do
        echo "  $(basename "$f" .md)" >&2
      done < <(find "${ld}" -maxdepth 1 -name '*.md' ! -name 'README.md' -print0 2>/dev/null | sort -z)
      exit 1
    elif [ ${#matches[@]} -gt 1 ]; then
      echo "Multiple matches for '${level}':" >&2
      printf '  %s\n' "${matches[@]}" >&2
      echo "Using first match." >&2
    fi
    open_file "${matches[0]}"
  fi
}

cmd_search() {
  [ $# -ge 1 ] || usage
  local query="$*"
  local results
  results=$(grep -rn --include='*.md' -i "${query}" "${DOCS_ROOT}" 2>/dev/null) || true
  if [ -z "${results}" ]; then
    echo "No matches found for '${query}' in ${DOCS_ROOT}"
    exit 0
  fi
  echo "${results}" | ${PAGER} -F
}

cmd_interactive() {
  [ -d "${DOCS_ROOT}" ] || die "DOCS_ROOT not found: ${DOCS_ROOT}"

  # Gather tracks
  local tracks=()
  while IFS= read -r t; do
    [ -n "$t" ] && tracks+=("$t")
  done < <(get_tracks)
  [ ${#tracks[@]} -gt 0 ] || die "No tracks found in ${DOCS_ROOT}"

  local track=""
  if command -v fzf >/dev/null 2>&1; then
    track=$(printf '%s\n' "${tracks[@]}" | fzf --prompt="Track > " --height=15 --reverse)
    [ -n "${track}" ] || exit 0
  else
    PS3="Track (number, or 0 to quit): "
    select track in "${tracks[@]}"; do
      if [ -z "${track}" ]; then
        [ "${REPLY}" = "0" ] && exit 0
        echo "Invalid choice: ${REPLY}" >&2
      else
        break
      fi
    done
  fi

  local ld; ld=$(lang_dir "$track")
  [ -n "$ld" ] || die "No language directory for track '${track}'"

  # Build lesson list (README first, then sorted lesson files)
  local lessons=() names=()
  local readme="${ld}/README.md"
  [ -f "${readme}" ] && { lessons+=("${readme}"); names+=("README — track overview"); }
  while IFS= read -r -d '' f; do
    lessons+=("$f")
    names+=("$(basename "$f" .md)")
  done < <(find "${ld}" -maxdepth 1 -name '*.md' ! -name 'README.md' -print0 2>/dev/null | sort -z)
  [ ${#lessons[@]} -gt 0 ] || die "No lessons found for track '${track}'"

  local choice=""
  if command -v fzf >/dev/null 2>&1; then
    local sel
    sel=$(printf '%s\n' "${names[@]}" | fzf --prompt="Lesson > " --height=15 --reverse)
    [ -n "${sel}" ] || exit 0
    for i in "${!names[@]}"; do
      if [ "${names[$i]}" = "${sel}" ]; then
        choice="${lessons[$i]}"
        break
      fi
    done
  else
    PS3="Lesson (number, or 0 to quit): "
    select sel in "${names[@]}"; do
      if [ -z "${sel}" ]; then
        [ "${REPLY}" = "0" ] && exit 0
        echo "Invalid choice: ${REPLY}" >&2
      else
        for i in "${!names[@]}"; do
          if [ "${names[$i]}" = "${sel}" ]; then
            choice="${lessons[$i]}"
            break
          fi
        done
        break
      fi
    done
  fi

  open_file "${choice}"
}

# ----------------------------------------------------------------
#  Main
# ----------------------------------------------------------------

if [ ! -d "${DOCS_ROOT}" ]; then
  die "DOCS_ROOT directory not found: ${DOCS_ROOT}"
fi

case "${1:-}" in
  list|ls)       cmd_list ;;
  show)          shift; cmd_show "$@" ;;
  search|grep)   shift; cmd_search "$@" ;;
  -h|--help)     usage ;;
  "")            cmd_interactive ;;
  *)             echo "Unknown command: $1" >&2; usage ;;
esac
