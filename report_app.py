import os
from cleo import Application

from common import read_yaml_file

class ReportApplication(Application):

    PROJ_TYPES = ['php', 'ruby', 'android']
    TEMPLATES_DIR = os.path.join(os.getcwd(), 'templates')

    def __init__(self, *args, **kwargs):
        super(ReportApplication, self).__init__()

    def register_command(self, command_class):
        command = command_class()
        command.app = self
        self.add(command)

    def config(self, configure_file_name, temp_file_name):
        self.configure_file_name = configure_file_name
        self.temp_file_name = temp_file_name
        self.load_ci_reports()

    def load_ci_reports(self):
        self.ci_reports = self.parse_ci_config()
        if 'url' not in self.ci_reports:
            self.ci_reports['url'] = 'http://ci-reports.framgia.vn'

    def parse_ci_config(self):
        raw = read_yaml_file(self.configure_file_name)
        if 'from' in raw:
            template_file = os.path.join(self.TEMPLATES_DIR, "%s.yml" % raw['from'])
            base = read_yaml_file(template_file)
            defaults = {
                'comment': True,
                'ignore': False,
                'enable': True
            }
            final = {'from': raw['from']}
            final['test'] = {}
            merged_tools = [key for key in raw['test'].keys()] + [key for key in base['test'].keys()]
            merged_tools = list(set(merged_tools))
            for tool in merged_tools:
                if tool not in raw['test']:
                    final['test'][tool] = base['test'][tool]
                else:
                    final['test'][tool] = {}
                    for key, value in defaults.items():
                        final['test'][tool][key] = raw['test'][tool].get(key, base['test'][tool].get(key, defaults[key]))
                    final['test'][tool]['command'] = raw['test'][tool].get('command', base['test'][tool]['command'])

            return final
        else:
            return raw
