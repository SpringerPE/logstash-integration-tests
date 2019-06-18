import json

# This script will read the input data from the `input.json` field and fill the files with that information:
## Will create the input.log file that will be read by logstash;

INPUT_FILE = 'data/input.json'

def build_input_log(log_path):
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        f = open(log_path, 'w+')
        for d in data:
            f.write(d['log'])
            f.write('\n')
        f.close()


build_input_log('data/input.log')
