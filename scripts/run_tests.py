import json
import os
import sys
import time

# This script will read the input data from the `input.json` file and test the expectations against the actual results.

LOGSTASH_OUTPUT = '/data/logstash.json'
SOURCE_FILE = '/data/input.json'


# Parses the field names that are in the output file.
# For example, a JSON field like {"field":{"nested":"value}} will be parsed to {"[field][nested]":"value"}
def parse_field_names(result, field_name, field_value, result_with_parsed_fields):
    if isinstance(result, dict):
        for k, v in result.items():
            if isinstance(k, dict):
                parse_field_names(k, field_name, '', result_with_parsed_fields)
            else:
                parse_field_names(v, field_name + '][' + k, v, result_with_parsed_fields)
    else:
        if field_name.startswith(']['):
            f = field_name[2:]
            f = '[' + f
            f = f[:len(f)] + ']'
            d = {f: str(field_value)}
            result_with_parsed_fields.update(d)


# Aux function that will return a list with the parsed fields.
# Will be needed to compare with the expectations.
def transform_results():
    transformed_results = {}
    with open(LOGSTASH_OUTPUT) as logstash_results:
        for result in logstash_results:
            r = json.loads(result)
            parsed_fields = {}
            parse_field_names(r, '', '', parsed_fields)
            transformed_results[parsed_fields['[@test][message]']] = parsed_fields
    return transformed_results


# Test each event against the expectations.
def test_event(ev, logstash_results):
    for log, fields in logstash_results.items():
        if log == ev['log']:
            for expectation in ev['expectations']:
                for field, value in expectation.items():
                    if field in fields and value == fields[field]:
                        print "PASS: " + field + ' | ' + value
                    else:
                        if field in fields:
                            sys.exit('TEST FAILED: expected |' + value + '| got |' + fields[field] + '|. Source event: |' + log + '|')
                        else:
                            sys.exit('TEST FAILED: field |' + field + '| was expected but was not found! Source event: |' + log + '|')


# Runs the tests that are defined in the `input.json` file.
def run_tests():
    logstash_results = transform_results()
    with open(SOURCE_FILE) as source_file:
        events = json.load(source_file)
        for ev in events:
            test_event(ev, logstash_results)


# Check if the output file (the one that has the actual results) already exists.
# This is needed because logstash can take a while to process the events.
def check_if_file_exists():
    exists = os.path.isfile(LOGSTASH_OUTPUT)
    max_attempts = 90
    attempts = 1

    while not exists and attempts < max_attempts:
        exists = os.path.isfile(LOGSTASH_OUTPUT)
        time.sleep(1)
        attempts += 1

    if attempts == max_attempts:
        sys.exit('FAILED: ' + LOGSTASH_OUTPUT + ' does not exist')


check_if_file_exists()
run_tests()
