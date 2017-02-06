import os
import sys
from cleo import Application

from framgiaci.common import read_yaml_file, read_template_file, merge_test_config

class ReportApplication(Application):

    PROJ_TYPES = ['php', 'ruby', 'android', 'ios']
    TEMPLATES_DIR = 'templates'

    def __init__(self, *args, **kwargs):
        super(ReportApplication, self).__init__()

    def register_command(self, command_class):
        command = command_class()
        command.app = self
        self.add(command)

    def check_configure_file_exists(self):
        if not os.path.isfile(self.configure_file_name):
            print('.framgia-ci.yml file does not exists')
            sys.exit(1)

    def config(self, configure_file_name, temp_file_name):
        self.configure_file_name = configure_file_name
        self.temp_file_name = temp_file_name
        if os.path.isfile(configure_file_name):
            self.load_ci_reports()

    def load_ci_reports(self):
        if len(sys.argv) == 2 and sys.argv[1] == 'check-config':
            pass
        else:
            self.ci_reports = self.parse_ci_config()
            if 'url' not in self.ci_reports:
                self.ci_reports['url'] = 'https://ci-reports.framgia.vn'

    def parse_ci_config(self):
        raw = read_yaml_file(self.configure_file_name)
        if 'from' in raw:
            base = read_template_file(self.TEMPLATES_DIR, raw['from'])
            final = {'from': raw['from']}
            final['test'] = merge_test_config(base['test'], raw['test'] if 'test' in raw else {})
            final['project_type'] = raw['project_type'] if 'project_type' in raw else base['project_type']

            return final
        else:
            return raw
