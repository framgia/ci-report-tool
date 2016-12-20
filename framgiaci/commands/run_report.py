import os
import sys
import time

from cleo import Command
from framgiaci.common import read_results, print_header, call_api, build_params


class RunReportCommand(Command):
    """
    Running report command to send copying request to CI Report service

    report
    """

    def chmod_git_folder():
        os.system('chmod R 755 .git')


    def create_report_queue(self, base_api_url, params):
        print('[+] Creating Report Queue ... ')
        retry_time = 10
        queue_id = None
        token = None
        for i in range(1, retry_time):
            queue_result = call_api(base_api_url, True, params, ['Content-Type: application/json'])
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
            result = call_api(base_api_url + '/' + str(queue_id), False, {}, ['token:' + str(token)])
            if result and 'errorCode' in result and not result['errorCode']:
                if 'error' in result['data'] or 'success' in result['data']['status']:
                    return True if result['data']['status'] == 'success' else False
                else:
                    print(i, 'API check queue status failed!')
                    print(result['data']['status'], result['data']['message'])
                    if ('message' in result):
                        print(result['message'])

        return False

    def handle(self):
        print_header('Sending Reports')
        base_api_url = self.app.ci_reports['url'] + '/api/queues'
        params = build_params()
        params['project_type'] = self.app.ci_reports['project_type'] if 'project_type' in self.app.ci_reports else None
        params['test_result'] = read_results(self.app.temp_file_name)
        queue_id, token = self.create_report_queue(base_api_url, params)
        if queue_id and token:
            self.track_queue(queue_id, token, base_api_url)
        else:
            sys.exit(1)
        sys.exit(0)
