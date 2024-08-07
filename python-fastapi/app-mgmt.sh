#!/bin/bash


SUBCMD=$1
ENVFILE=env

function show_usage() {
  echo
  echo "Usage: ./app-mgmt.sh [ACTION]"
  echo
  echo "  ACTION:"
  echo "    start"
  echo "    stop"
  echo "    daemon"
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
   --reload
}

function daemon_app() {
  uvicorn webapp.main:app \
   --env-file $ENVFILE \
   --host 0.0.0.0 \
   --port 8000 \
   --reload &
}

function stop_app() {
  pkill uvicorn
}


if [ $# -lt 1 ]
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

if [ $SUBCMD == "daemon" ]
then
  daemon_app
fi

if [ $SUBCMD == "status" ]
then
  status
fi
