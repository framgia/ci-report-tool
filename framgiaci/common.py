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