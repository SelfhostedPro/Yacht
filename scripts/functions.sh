#!/bin/bash

##############################################################################
# PARSE ALL ARGS
##############################################################################
function parseArgs {
  while [[ $# > 0 ]]
  do
    case "${1}" in
    --disable-auth | -d)
      setDisableAuth="true"
      ;;

    --backend-only | -b)
      setRunBackendOnly="true"
      ;;

    --frontend-only | -f)
      setRunFrontendOnly="true"
      ;;

    --use-tmux | -t)
      setUseTmux="true"
      ;;

    -tmux)
      setUseTmuxScript="true"
      ;;

    --help | -h)
      echo "  Script Usage:"
      echo "    -d, --disable-auth                  set DISABLE_AUTH=true"
      echo "    -b, --backend-only                  only run Yacht backend"
      echo "    -f, --frontend-only                 only run Yacht frontend"
      echo "    -t, --use-tmux                      run dev with tmux *experimental*"
      echo "    -h, --help                          view this help message"
      echo ""
      exit 0
      ;;

    *)
      runBackend
      runFrontend
      ;;

    esac
    shift
  done
}

##############################################################################
# CHECK OPTIONS FOR ERRORS
##############################################################################
function checkOpts {
  if [[ "$setRunBackendOnly" == "true" && "$setRunFrontendOnly" == "true" ]]; then
    red "  ERROR: Opts \`-b\` and \`-f\` are mutually exclusive"
    exit 1
  fi

  if [[ "$setUseTmux" == "true" ]]; then
    if [[ "$setRunBackendOnly" == "true" || "$setRunFrontendOnly" == "true" ]]; then
    red "  ERROR: Opt \`-t\` and \`-f\`/\`-b\` are mutually exclusive"
    exit 1
    fi
  fi

  if [[ "$setRunBackendOnly" == "true" || "$setRunFrontendOnly" == "true" || "$setDisableAuth" == "true" ]]; then
  echo "  Running with the following options:"
    if [[ "$setDisableAuth" == "true" ]]; then
      export DISABLE_AUTH=true
      echo "    DISABLE_AUTH: true"
    fi

    if [[ "$setBackendOnly" == "true" ]]; then
      echo "    Backend only: true"
    fi

    if [[ "$setFrontendOnly" == "true" ]]; then
      echo " Frontend only: true"
    fi
  fi
}

##############################################################################
# CHECK BACKEND DEPENDENCIES
# TODO:  Re-write this to _actually_ check dependencies
##############################################################################
function checkBackendDeps {
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
    pip install -r requirements.txt &>${BASE_DIR}/tmp/pip.log &
    echo ""
  elif [[ $VIRTUAL_ENV && -f "venv/bin/uvicorn" ]]; then
    echo "    Found /venv/bin/uvicorn, skipping dependency install."
    echo ""
  fi
}

##############################################################################
# CHECK FRONTEND DEPENDENCIES
# TODO:  Possibly re-write this to check package.json for changes?
##############################################################################
function checkFrontendDeps {
  echo "  Checking for dependencies..."
  if [[ ! -d "./node_modules" ]]; then
    echo "  Installing dependencies..."
    echo "  npm install"
  else
    echo "  Found node_modules, skipping."
    echo ""
  fi
}

##############################################################################
# START BACKEND
##############################################################################
function runBackend {
  showBanner "Backend"
  pushd "${BASE_DIR}/backend"

  checkBackendDeps

  echo "  Starting the backend..."
  echo "    Log file -> ${BASE_DIR}/tmp/backend.log"
  if [[ -f "${BASE_DIR}/tmp/backend.log" ]]; then
    echo "    Moving old log -> ${BASE_DIR}/tmp/backend.log.old"
    mv ${BASE_DIR}/tmp/backend.log ${BASE_DIR}/tmp/backend.log.old
  fi

  if [[ ! "$setUseTmuxScript" == "true" ]]; then
    uvicorn api.main:app --reload --host 0.0.0.0 &>${BASE_DIR}/tmp/backend.log &
  else
    printf "\033c"
    uvicorn api.main:app --reload --host 0.0.0.0 | tee ${BASE_DIR}/tmp/backend.log
  fi
  echo $! >${BASE_DIR}/tmp/backend.pid

  echo "    Backend running on PID $(cat ${BASE_DIR}/tmp/backend.pid)"
  echo ""

  popd
}

##############################################################################
# START FRONTEND
##############################################################################
function runFrontend {
  showBanner "Frontend"
  pushd "${BASE_DIR}"/frontend

  checkFrontendDeps

  echo "  Starting the frontend..."
  echo "    Log file -> ${BASE_DIR}/tmp/frontend.log"
  if [[ -f "${BASE_DIR}/tmp/frontend.log" ]]; then
    echo "    Moving old log -> ${BASE_DIR}/tmp/frontend.log.old"
    mv ${BASE_DIR}/tmp/frontend.log ${BASE_DIR}/tmp/frontend.log.old
  fi

  if [[ ! "$setUseTmuxScript" == "true" ]]; then
    npm start &>${BASE_DIR}/tmp/frontend.log &
  else
    printf "\033c"
    npm start | tee ${BASE_DIR}/tmp/frontend.log
  fi

  echo $! >${BASE_DIR}/tmp/frontend.pid
  echo "    frontend running on PID $(cat ${BASE_DIR}/tmp/frontend.pid)"
  echo ""

  popd
}

##############################################################################
# RUN DEVELOPMENT SETUP WITH OPTIONS
##############################################################################
function runDev {
  if [[ "$setUseTmux" == "true" ]]; then 
    if [[ ! "$setRunFrontendOnly" == "true" && ! "$setRunBackendOnly" == "true" ]]; then
      tmux new-session -d -s yacht-dev ;
      tmux split-window -h ;
      tmux select-pane -L
      tmux send-keys -t yacht-dev ${SCRIPT_DIR}'/dev.sh -tmux -b -d' C-m
      tmux select-pane -R
      tmux send-keys -t yacht-dev ${SCRIPT_DIR}'/dev.sh -tmux -f' C-m
      tmux attach-session -d -t yacht-dev 
      exit 0
    fi
  else
    if [[ "$setRunBackendOnly" == "true" ]]; then
      runBackend
    elif [[ "$setRunFrontendOnly" == "true" ]]; then
      runFrontend
    else
      runBackend
      runFrontend
    fi
  fi

echo ""
echo "Press [Ctrl+C] to exit..."

while true; do
  sleep 1
done
}

##############################################################################
# SILENCE PUSHD AND POPD
##############################################################################
function pushd() {
  command pushd "$@" >/dev/null
}

function popd() {
  command popd "$@" >/dev/null
}

##############################################################################
# COLORS
##############################################################################
default="\033[0m"
bright="\033[1m"
dim="\033[2m"

red="\033[31m"
green="\033[32m"
yellow="\033[33m"
blue="\033[34m"
magenta="\033[35m"
cyan="\033[36m"

function green {
  echo -e "${green}${1}${default}"
}

function red {
  echo -e "${red}${1}${default}"
}
