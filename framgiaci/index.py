#!/usr/local/bin/python
# coding: utf-8

import sys
from framgiaci.version import __version__
from framgiaci.report_app import ReportApplication
from framgiaci.commands.run_finish import RunFinishCommand
from framgiaci.commands.run_report import RunReportCommand
from framgiaci.commands.run_test import RunTestCommand
from framgiaci.commands.init_template import InitTemplateCommand
from framgiaci.commands.run_all import RunAllCommand
from framgiaci.commands.check_config import CheckConfigCommand
from framgiaci.commands.show_config import ShowConfigCommand
from framgiaci.commands.run_notify import RunNotifyCommand
from framgiaci.commands.test_connect import TestConnectCommand
from framgiaci.commands.run_upload import RunUploadCommand

YAML_CONFIGURE_FILE = '.framgia-ci.yml'
RESULT_TEMP_FILE = '.framgia-ci-result.temp.yml'

COMMANDS = [
    RunTestCommand, RunReportCommand, RunFinishCommand, InitTemplateCommand,
    CheckConfigCommand, ShowConfigCommand, RunAllCommand, RunNotifyCommand,
    TestConnectCommand, RunUploadCommand
]

def main():
    print('Framgia CI Report Tool', __version__)
    app = ReportApplication()
    app.config(YAML_CONFIGURE_FILE, RESULT_TEMP_FILE)
    for command in COMMANDS:
        app.register_command(command)
    app.run()
    sys.exit(0)

if __name__ == '__main__':
    main()
