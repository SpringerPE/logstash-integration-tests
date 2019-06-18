#!/usr/bin/env bash

# This script will load the logstash output file and compare the values of the fields that are defined there with the
# expectations.
# Returns `exit 1` in case of failure.

INPUT="/data/logstash.csv"

# Credits to https://stackoverflow.com/a/24597941/10985108
function error_exit {
    echo "$1" >&2   ## Send message to stderr. Exclude >&2 if you don't want it that way.
    exit "${2:-1}"  ## Return a code specified by $2 or 1 by default.
}

run_tests ()
{
    declare -a expectations
    expectations=()

    while IFS= read -r line
    do
      IFS=';' read -ra arr <<< "$line"
      for i in "${!arr[@]}"; do
         if [ "${arr[$i]}" == "${expectations[$i]}" ]
         then
           printf "TEST $i PASSED; \n"
         else
           error_exit "TEST FAILED: got | ${arr[$i]} |; expected | ${expectations[$i]} |" 105
         fi
      done
    done < "$INPUT"
}

check_if_file_exists ()
{
    max_attempts=90
    attempts=1

    while ! test -f $INPUT && [[ $attempts -lt $max_attempts ]]
    do
	    sleep 1
	    ((attempts++))
    done
    
    if [[ $attempts -eq $max_attempts ]]
    then
	    error_exit "FAILED: $INPUT does not exist" 104
    fi
}

check_if_file_exists
run_tests
