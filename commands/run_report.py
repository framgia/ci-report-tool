import json
import os
import sys
import time

import requests
from cleo import Command


class RunReportCommand(Command):
    """
    Running report command to send request to CI Report service

    report
    """

    def chmod_git_folder():
        os.system('chmod R 755 .git')

    def build_params(self):
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

    def call_api(self, url, is_post=False, params={}, headers=[]):
        print(params, headers)
        if is_post:
            r = requests.post(url, data=params, headers=headers)
        else:
            r = requests.post(url, params=params, headers=headers)

        try:
            return json.loads(r.text)
        except Exception:
            return {'errorCode': 'Server Error !'}

    def create_report_queue(self, base_api_url, params):
        print("[+] Creating Report Queue ... ")
        retry_time = 10
        queue_id = None
        token = None
        for i in range(1, retry_time):
            queue_result = self.call_api(base_api_url, True, params, {'ContentType': 'application/json'})
            if (queue_result and 'errorCode' in queue_result and not queue_result['errorCode']):
                queue_id = queue_result['data']['queueId']
                token = queue_result['data']['token']
                break
            else:
                print(i, " API create report failed!")
            time.sleep(5)

        return queue_id, token

    def track_queue(self, queue_id, token, base_api_url):
        retry_time = 10
        print("[+] Tracking queue", queue_id)
        for i in range(1, retry_time):
            time.sleep(5)
            result = self.call_api(base_api_url + "/" + str(queue_id), False, {}, {'token:' + str(token)})
            if result and "errorCode" in result and not result["errorCode"]:
                print(result["data"]["status"], result["data"]['message'])
                if "error" in result["data"] or "success" in result["data"]["status"]:
                    return True if result["data"]["status"] == "success" else False
                else:
                    print(i, " API check queue status failed!")

            return False

    def handle(self):
        base_api_url = self.app.ci_reports['url'] + "/api/queues"
        params = self.build_params()
        queue_id, token = self.create_report_queue(base_api_url, params)
        if queue_id:
            self.track_queue(queue_id, token, base_api_url)
        sys.exit(0)
