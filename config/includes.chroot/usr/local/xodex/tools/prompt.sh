# shellcheck shell=bash
# Xodex status-aware prompt (time + optional battery/net stubs)

_xodex_battery() {
  local cap=""
  if [ -r /sys/class/power_supply/BAT0/capacity ]; then
    cap=$(cat /sys/class/power_supply/BAT0/capacity 2>/dev/null || true)
    [ -n "${cap}" ] && printf '%s%%' "${cap}" && return
  fi
  printf 'AC'
}

_xodex_net() {
  if command -v ip >/dev/null 2>&1; then
    if ip -4 route get 1.1.1.1 >/dev/null 2>&1; then
      printf 'net●'
      return
    fi
  fi
  printf 'net○'
}

_xodex_prompt() {
  local theme="${XODEX_THEME:-dark}"
  local c_user c_reset
  if [ "${theme}" = "light" ]; then
    c_user='\e[1;34m'
  else
    c_user='\e[1;32m'
  fi
  c_reset='\e[0m'
  if [ "$PWD" = "$HOME" ]; then
    PS1="\[${c_user}\]xodex@xodex\w@;\[${c_reset}\] "
  else
    PS1="\[${c_user}\]xodex@xodex\w~@;\[${c_reset}\] "
  fi
}

PROMPT_COMMAND=_xodex_prompt
