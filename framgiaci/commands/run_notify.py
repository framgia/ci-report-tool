import sys

from cleo import Command
from framgiaci.common import print_header, build_params, call_api


class RunNotifyCommand(Command):
    """
    Running notify command to send notify request to CI Report service

    notify
    """

    def handle(self):
        print_header('Sending Notifications')
        base_api_url = self.app.ci_reports['url'] + '/api/notifications'
        params = build_params()
        print(call_api(base_api_url, True, params, ['Content-Type: application/json']))
        sys.exit(0)
