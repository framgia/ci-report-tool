#!/usr/local/bin/python
# coding: utf-8

import yaml
import sys
import json
import time
import os
import pycurl
from io import BytesIO
from cleo import Application, Command
from urllib.parse import urlencode

YAML_CONFIGURE_FILE = '.framgia-ci.yml'
RESULT_TEMP_FILE = '.framgia-ci-result.temp.yml'
print("Framgia CI Report Tool")

def get_exit_code(child):
    return child.exitstatus if child.exitstatus != None else child.signalstatus

def run_command(command):
    try:
        print("[+] Running: ", command)
        return os.system(command)

    except Exception as e:
        print('[!] Error:', e)
        return 1

def read_yaml_file(file):
    f = open(file)
    return yaml.load(f.read())

def read_results():
    return read_yaml_file(RESULT_TEMP_FILE)

def write_results(results):
    with open(RESULT_TEMP_FILE, 'w') as outfile:
        yaml.dump(results, outfile, default_flow_style=False)

def print_header(text):
    print("\n------------------------------------------")
    print(text)
    print("------------------------------------------\n")

global ci_reports
ci_reports = read_yaml_file(YAML_CONFIGURE_FILE);

class RunTestCommand(Command):
    """
    Running test tools

    test
    """
    def handle(self):
        print_header("Running Test")
        if ci_reports['test']:
            test_commands = ci_reports['test']
            results = {}
            for tool, options in test_commands.items():
                if 'enable' in options and options['enable']:
                    result = run_command(options['command'])
                    ignore = 'ignore' in options and options['ignore'] == True
                    results[tool] = {
                        "exit_code": result,
                        "ignore": ignore
                    }
            write_results(results)
            sys.exit(0)

class RunReportCommand(Command):
    """
    Running report command to send request to CI Report service

    report
    """
    def chmodGitFolder():
        os.system('chmod -R 755 .git')

    def buildParams(self):
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

    def callAPI(self, url, isPost=False, params={}, headers=[]):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        if isPost:
            postfields = json.dumps(params)
            c.setopt(c.POSTFIELDS, postfields)
        if headers != []:
            c.setopt(c.HTTPHEADER, headers)

        c.perform()
        c.close()

        body = buffer.getvalue()
        body = body.decode('iso-8859-1')
        return body

    def createReportQueue(self, base_api_url, params):
        print("[+] Creating Report Queue ... ")
        retry_time = 10
        queue_id = None
        token = None
        for i in range(1, retry_time):
            create_report_result = self.callAPI(base_api_url, True, params, ['Content-Type: application/json'])
            queue_result = json.loads(create_report_result)
            if (queue_result and 'errorCode' in queue_result and not queue_result['errorCode']):
                queue_id = queue_result['data']['queueId']
                token = queue_result['data']['token']
                break
            else:
                print(i, "- API create report failed!")
            time.sleep(5)
        return queue_id, token

    def trackQueue(self, queue_id, token, base_api_url):
        retry_time = 10
        print("[+] Tracking queue", queue_id)
        for i in range(1, retry_time):
            time.sleep(5)
            check_queue_result = self.callAPI(base_api_url + "/" + str(queue_id), False, {}, ['token:' + str(token)])
            result = json.loads(check_queue_result)
            if result and "errorCode" in result and not result["errorCode"]:
                print(result["data"]["status"], result["data"]['message'])
                if "error" in result["data"] or "success" in result["data"]["status"]:
                    return True if result["data"]["status"] == "success" else False
                else:
                    print(i, "- API check queue status failed!")
            return False

    def handle(self):
        base_api_url = "http://ci-reports.framgia.vn/api/queues";
        params = self.buildParams();
        params['project_type'] = ci_reports['project_type'] if 'project_type' in ci_reports else None
        params['test_result'] = read_results()
        queue_id, token = self.createReportQueue(base_api_url, params)
        if queue_id:
            self.trackQueue(queue_id, token, base_api_url)
        sys.exit(0)

class RunFinishCommand(Command):
    """
    Running finish command tools

    finish
    """
    def handle(self):
        results = read_results()
        final_result = True
        final_text = ""
        for tool, result in results.items():
            if result["exit_code"] != 0:
                if result["ignore"] == True:
                    final_text = final_text + "[*] " + tool + ": failed but ignored\n"
                else:
                    result_text = "failed"
                    final_text = final_text + "[X] " + tool + ": failed\n"
                    final_result = False
            else:
                final_text = final_text + "[O] " + tool + ": success\n"
        if final_result:
            print_header("[O] Build Success!")
            print(final_text)
            sys.exit(0)
        else:
            print_header("[X] Build Fail!")
            print(final_text)
            sys.exit(1)

application = Application()
application.add(RunTestCommand())
application.add(RunReportCommand())
application.add(RunFinishCommand())
application.run()

