import os
import yaml
import sys

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


def read_template_file(template_dir, file_name):
    template_file = os.path.join(template_dir, "%s.yml" % file_name)
    return read_yaml_file(template_file)

def merge_test_config(base, overwrite):
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