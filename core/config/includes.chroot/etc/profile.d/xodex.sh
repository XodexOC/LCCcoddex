# Xodex environment — sourced for login shells
export XODEX_HOME="${XODEX_HOME:-/usr/local/xodex}"
export PATH="/usr/local/bin:${PATH}"

# Readable default prompt with theme-friendly colors
if [ -n "${PS1:-}" ]; then
  # shellcheck disable=SC2034
  XODEX_THEME="${XODEX_THEME:-dark}"
  if [ -f /usr/local/xodex/tools/prompt.sh ]; then
    # shellcheck source=/dev/null
    . /usr/local/xodex/tools/prompt.sh
  else
    PS1='\[\e[1;32m\][student@xodex \W]\$\[\e[0m\] '
  fi
fi

# First interactive login hint
if [ -n "${PS1:-}" ] && [ -z "${XODEX_MOTD_SHOWN:-}" ]; then
  export XODEX_MOTD_SHOWN=1
  if [ -t 1 ] && command -v xodex-menu >/dev/null 2>&1; then
    echo
    echo "  Xodex Live — type: xodex-menu"
    echo "  Docs: ${XODEX_HOME}/docs   Examples: ${XODEX_HOME}/examples"
    echo "  User: student  Password: xodex  (sudo without password)"
    echo
  fi
fi
