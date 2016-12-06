from cleo import Application

from common import read_yaml_file


class ReportApplication(Application):

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
        self.ci_reports = read_yaml_file(self.configure_file_name);
