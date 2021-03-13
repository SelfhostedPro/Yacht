#!/bin/bash

# Bail on any errors during the script execution.
set -e

# Hide control characters in terminal output
stty -echoctl

function main {
  showBanner "Yacht Dev"

  setup

  parseArgs ${@}
  checkOpts

  runDev
}

##############################################################################
# PREPARE SOME THINGS BEFORE RUNNING
##############################################################################
function setup {
  SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

  BASE_DIR="$(dirname $(
    cd "$(dirname "$0")"
    pwd -P
  ))"

  # Make a tmp directory for storing temporary files and logs
  mkdir -p "${BASE_DIR}"/tmp

  # Source additional script files
  source "$SCRIPT_DIR/functions.sh"

  showBanner "Setup"

  echo "  BASE_DIR = $BASE_DIR"
  echo "  SCRIPT_DIR = $SCRIPT_DIR"
  echo ""
}

##############################################################################
# PRINT A PRETTY BANNER BETWEEN STEPS
##############################################################################
function showBanner {
  pad=$(printf '%0.1s' " "{1..70})
  startString="  ${1}"
  endString="$(date +%r)  "
  padLength=80

  echo -e "\033[32m================================================================================\033[0m"
  printf '%s' "$startString"
  printf '%*.*s' 0 $((padLength - ${#startString} - ${#endString} )) "$pad"
  printf '%s\n' "$endString"
  echo -e "\033[32m================================================================================\033[0m"
}

##############################################################################
# CLEANUP ON ANY EXIT
##############################################################################
function cleanup {
  showBanner "CleanUp"

  pushd "${BASE_DIR}"/tmp/

  if [[ -f 'frontend.pid' || -f 'backend.pid' ]]; then
    echo "    Stopping all processes..."

    for pidfile in *.pid; do
      pid=$(cat "$pidfile")
      echo "      Killing $pid..."

      { kill $pid && wait $pid; } 2>/dev/null
      rm $pidfile
    done
  fi

  popd

  # restore ctrl characters in terminal
  stty echoctl

  if [[ "$setDisableAuth" == "true" ]]; then
    unset DISABLE_AUTH
  fi
}

# On any exit of the script, run cleanup
trap cleanup EXIT

# Run the main function, passing all args
main ${@}
