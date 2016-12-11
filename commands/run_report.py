import json
import os
import sys
import time
import pycurl

from io import BytesIO
from cleo import Command
from urllib.parse import urlencode
from common import read_results, print_header


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
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        if is_post:
            postfields = json.dumps(params)
            c.setopt(c.POSTFIELDS, postfields)
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

    def create_report_queue(self, base_api_url, params):
        print('[+] Creating Report Queue ... ')
        retry_time = 10
        queue_id = None
        token = None
        for i in range(1, retry_time):
            queue_result = self.call_api(base_api_url, True, params, ['Content-Type: application/json'])
            if (queue_result and 'errorCode' in queue_result and not queue_result['errorCode']):
                queue_id = queue_result['data']['queueId']
                token = queue_result['data']['token']
                break
            else:
                print(i, 'API create report failed!')
                if ('message' in queue_result):
                    print(queue_result['message'])
            time.sleep(5)

        return queue_id, token

    def track_queue(self, queue_id, token, base_api_url):
        retry_time = 10
        print('[+] Tracking queue', queue_id)
        for i in range(1, retry_time):
            time.sleep(5)
            result = self.call_api(base_api_url + '/' + str(queue_id), False, {}, ['token:' + str(token)])
            if result and 'errorCode' in result and not result['errorCode']:
                print(result['data']['status'], result['data']['message'])
                if 'error' in result['data'] or 'success' in result['data']['status']:
                    return True if result['data']['status'] == 'success' else False
                else:
                    print(i, 'API check queue status failed!')
                    if ('message' in result):
                        print(result['message'])

        return False

    def handle(self):
        print_header('Sending Reports')
        base_api_url = self.app.ci_reports['url'] + '/api/queues'
        params = self.build_params()
        params['project_type'] = self.app.ci_reports['project_type'] if 'project_type' in self.app.ci_reports else None
        params['test_result'] = read_results(self.app.temp_file_name)
        queue_id, token = self.create_report_queue(base_api_url, params)
        if queue_id and token:
            self.track_queue(queue_id, token, base_api_url)
        else:
            sys.exit(1)
        sys.exit(0)
