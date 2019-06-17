import re, shutil, tempfile
import json

# This script will read the input data from the `input.json` field and fill the files with that information:
## Will insert the fields to be asserted into the output.conf logstash file;
## Will create the input.log file that will be read by logstash;
## Will create the array of expectations in the test script.

# Credits to https://stackoverflow.com/a/31499114/10985108
def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

def build_output_conf(output_conf_path):
    with open('input.json') as json_file:  
        data = json.load(json_file)
        fields_str='fields => ['
        for f in data['fields']:
            fields_str += '\"' + f + '\", '
        fields_str = fields_str[:-2] + ']'
        sed_inplace(output_conf_path, r'fields => \[\]', fields_str)

def build_input_log(log_path):
    with open('input.json') as json_file:  
        data = json.load(json_file)
        f = open(log_path, 'w+')
        f.write(data['log'])
        f.write('\n')
        f.write(' ')
        f.close()

def build_assertions(file_path):
    with open('input.json') as json_file:  
        data = json.load(json_file)
        expectations = 'expectations=('
        for v in data['expected_field_values']:
            expectations += '\"' + v + '\" '
        expectations += ')'
        sed_inplace(file_path, r'expectations=\(\)', expectations)

build_output_conf('conf/output.conf')
build_input_log('data/input.log')
build_assertions('scripts/run_tests.sh')
