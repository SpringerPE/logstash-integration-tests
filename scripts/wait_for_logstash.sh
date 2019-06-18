#!/usr/bin/env bash

# This script will wait for logstash to be started (will try to connect via TCP) and, in case of success, will run the
# tests.
# Exit with error in case logstash doesn't start on time.

IP=192.168.200.2
PORT=5514

MAX_ATTEMPTS=90
ATTEMPTS=1
INTERVAL=1

$(rm -rf /data/logstash.csv)

$(nc -z $IP $PORT)
status=$?

while [[ $status -gt 0 && $ATTEMPTS -lt $MAX_ATTEMPTS ]]
do
  $(nc -z $IP $PORT)
  status=$?
  sleep $INTERVAL
  ((ATTEMPTS++))
done

if [[ $ATTEMPTS -lt $MAX_ATTEMPTS ]]
then
  $(/tmp/run_tests.sh)
  exit $?
else	
  echo "FAILURE: logstash start timed out"
  exit 1
fi
