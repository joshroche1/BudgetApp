#!/bin/bash


SUBCMD=$2
ENVFILE=$1

function show_usage() {
  echo
  echo "Usage: ./app-mgmt.sh [ENV_FILE] [ACTION]"
  echo
  echo "  ACTION:"
  echo "    start"
  echo "    stop"
  echo "    status"
  echo
  exit 0
}

function status() {
  echo
  echo "[netstat -tulnp]"
  echo
  netstat -tulnp | grep 8000
  echo
  echo "[ps aux | grep uvicorn]"
  echo
  ps aux | grep uvicorn
  echo
}

function start_app() {
  uvicorn webapp.main:app \
   --env-file $ENVFILE \
   --host 0.0.0.0 \
   --port 8000 \
   --reload &
}

function stop_app() {
  pkill uvicorn
}


if [ $# -lt 2 ]
then
  show_usage
fi

if [ $SUBCMD == "start" ]
then
  start_app
fi

if [ $SUBCMD == "stop" ]
then
  stop_app
fi

if [ $SUBCMD == "status" ]
then
  status
fi
