#!/bin/bash

# Bail on any errors during the script execution.
set -e

# Hide control characters in terminal output
stty -echoctl

function main() {
  showBanner "Yacht Dev"

  # run setup
  setup

  # Parse args, if there are any
  case "${1}" in
  --disable-auth | -d)
    setDisableAuth=true
    export DISABLE_AUTH=true
    runBackend
    runFrontend
    ;;

  --backend-only | -b)
    echo "Running backend only..."
    echo ""
    runBackend
    ;;

  --frontend-only | -f)
    echo "Running frontend only..."
    echo ""
    runFrontend
    ;;

  --help | -h)
    echo "We're working on it, for now just run the script with no options."
    ;;

  *)
    runBackend
    runFrontend
    ;;

  esac

  echo ""
  echo "Press [Ctrl+C] to exit..."

  while true; do
    sleep 1
  done
}

# Setup a few things before we start.
function setup() {
  showBanner "Setup"

  BASE_DIR="$(dirname $(
    cd "$(dirname "$0")"
    pwd -P
  ))"

  echo "  BASE_DIR = $BASE_DIR"
  echo ""

  mkdir -p "${BASE_DIR}"/tmp
}

# This runs between each step in this file, to show the steps that are happening
function showBanner() {

  startString="  ${1}"

  echo -e "\033[32m======================================================\033[0m"
  echo "${startString}                            ($(date +%r))"
  echo -e "\033[32m======================================================\033[0m"
}

function runBackend() {
  showBanner "Backend"
  pushd "${BASE_DIR}/backend"

  checkBackendDeps

  echo "  Starting the backend..."
  echo "    Log file -> ${BASE_DIR}/tmp/backend.log"
  if [[ -f "${BASE_DIR}/tmp/backend.log" ]]; then
    echo "    Moving old log -> ${BASE_DIR}/tmp/backend.log.old"
    mv ${BASE_DIR}/tmp/backend.log ${BASE_DIR}/tmp/backend.log.old
  fi

  uvicorn api.main:app --reload --host 0.0.0.0 &>${BASE_DIR}/tmp/backend.log &
  echo $! >${BASE_DIR}/tmp/backend.pid

  if [[ $setDisableAuth ]]; then
    echo "    DISABLE_AUTH: true"
  fi

  echo "    Backend running on PID $(cat ${BASE_DIR}/tmp/backend.pid)"
  echo ""

  popd
}

function runFrontend() {
  showBanner "Frontend"
  pushd "${BASE_DIR}"/frontend

  checkFrontendDeps

  echo "  Starting the frontend..."
  echo "    Log file -> ${BASE_DIR}/tmp/frontend.log"
  if [[ -f "${BASE_DIR}/tmp/frontend.log" ]]; then
    echo "    Old log -> ${BASE_DIR}/tmp/frontend.log.old"
    mv ${BASE_DIR}/tmp/frontend.log ${BASE_DIR}/tmp/frontend.log.old
  fi

  npm start &>${BASE_DIR}/tmp/frontend.log &
  echo $! >${BASE_DIR}/tmp/frontend.pid
  echo "    frontend running on PID $(cat ${BASE_DIR}/tmp/frontend.pid)"
  echo ""

  popd
}

function checkBackendDeps() {
  echo "  Checking backend dependencies..."

  if [[ ! -d "venv" ]]; then
    echo "    Python virtual environment not found, creating..."
    python -m venv venv
  elif [[ -d "venv" && ! $VIRTUAL_ENV ]]; then
    echo "    Found python virtual environment, loading..."
    source ./venv/bin/activate
  fi

  if [[ $VIRTUAL_ENV && ! -f "venv/bin/uvicorn" ]]; then
    echo ""
    echo "  Installing dependencies..."
    echo "    Log file -> ${BASE_DIR}/tmp/pip.log"
    echo "  pip install -r requirements.txt &>${BASE_DIR}/tmp/pip.log &"
    echo ""
  elif [[ $VIRTUAL_ENV && -f "venv/bin/uvicorn" ]]; then
    echo "    Found /venv/bin/uvicorn, skipping dependency install."
    echo ""
  fi
}

function checkFrontendDeps() {
  echo "  Checking for dependencies..."
  if [[ ! -d "./node_modules" ]]; then
    echo "  Installing dependencies..."
    echo "  npm install"
  else
    echo "  Found node_modules, skipping."
    echo ""
  fi
}

# silence pushd/popd default output
function pushd() {
  command pushd "$@" >/dev/null
}

function popd() {
  command popd "$@" >/dev/null
}

# trap here to ensure cleanup
function cleanup() {
  showBanner "CleanUp"

  pushd "${BASE_DIR}"/tmp/

  echo "    Stopping all processes..."

  for pidfile in *.pid; do
    pid=$(cat "$pidfile")
    echo "      Killing $pid..."

    { kill $pid && wait $pid; } 2>/dev/null
    rm $pidfile
  done

  popd

  # show ctrl characters in terminal
  stty echoctl

  if [[ setDisableAuth ]]; then
    unset DISABLE_AUTH
  fi
}

# On any exit of the script, run cleanup
trap cleanup EXIT

# Run the main function, passing all args
main ${@}
