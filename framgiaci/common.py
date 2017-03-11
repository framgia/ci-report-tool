import os
import yaml
import sys
import pycurl
import json

from io import BytesIO

def run_command(command):
    try:
        print("[+] Running: ", command)
        return os.system(command)

    except Exception as e:
        print('[!] Error:', e)
        return 1


def read_yaml_file(file):
    try:
        with open(file, "r") as f:
            return yaml.load(f.read())
    except Exception as e:
        print('Can not read file', file)
        sys.exit(1)


def read_results(temp_file):
    return read_yaml_file(temp_file)


def write_results(results, temp_file):
    with open(temp_file, 'w') as outfile:
        yaml.dump(results, outfile, default_flow_style=False)


def print_header(text):
    print("\n------------------------------------------")
    print(text)
    print("------------------------------------------\n")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, relative_path)

def buid_template_file_path(template_dir, file_name):
    return os.path.join(resource_path(template_dir), "%s.yml" % file_name)

def read_template_file(template_dir, file_name):
    return read_yaml_file(buid_template_file_path(template_dir, file_name))

def merge_test_config(base, overwrite):
    if not base:
        return overwrite
    result = {}
    merged_tools = [key for key in overwrite.keys()] + [key for key in base.keys()]
    merged_tools = list(set(merged_tools))
    defaults = {
        'comment': True,
        'ignore': False,
        'enable': True
    }
    for tool in merged_tools:
        if tool not in overwrite:
            result[tool] = base[tool]
        else:
            result[tool] = {}
            for key, value in defaults.items():
                result[tool][key] = overwrite[tool].get(key, base[tool].get(key, defaults[key]))
            result[tool]['command'] = overwrite[tool].get('command', base[tool]['command'])
            for key in [k for k in overwrite[tool].keys() if k not in list(defaults.keys()) + ['command']]:
                result[tool][key] = overwrite[tool][key]

    return result

def build_params():
    repo = os.environ.get('DRONE_REPO').split('/')
    return {
        'workspace': {
            'path': os.environ.get('DRONE_DIR')
        },
        'repo': {
            'owner': repo[0],
            'name': repo[1],
            'full_name': os.environ.get('DRONE_REPO')
        },
        'build': {
            'number': os.environ.get('DRONE_BUILD_NUMBER'),
            'commit': os.environ.get('DRONE_COMMIT'),
            'branch': os.environ.get('DRONE_BRANCH'),
            'pull_request_number': os.environ.get('DRONE_PULL_REQUEST')
        },
        'job': {
            'number': os.environ.get('DRONE_JOB_NUMBER')
        }
    }

def call_api(url, is_post=False, params={}, headers=[], files=[]):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.WRITEDATA, buffer)
    if is_post:
        postfields = []
        for k,v in params.items():
            postfields.append((k, json.dumps(v)))
        if files != []:
            for tag, file in files:
                postfields.append((tag, (c.FORM_FILE, file)))
        c.setopt(c.HTTPPOST, postfields)

    if headers != []:
        c.setopt(c.HTTPHEADER, headers)

    c.perform()
    c.close()

    body = buffer.getvalue()
    body = body.decode('iso-8859-1')
    try:
        return json.loads(body)
    except Exception:
        return {'errorCode': 'Server Error !'}
