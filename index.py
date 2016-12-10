#!/usr/local/bin/python
# coding: utf-8

import sys
from report_app import ReportApplication
from commands.run_finish import RunFinishCommand
from commands.run_report import RunReportCommand
from commands.run_test import RunTestCommand
from commands.init_template import InitTemplateCommand
from commands.run_all import RunAllCommand
from commands.check_config import CheckConfigCommand
from commands.show_config import ShowConfigCommand

YAML_CONFIGURE_FILE = '.framgia-ci.yml'
RESULT_TEMP_FILE = '.framgia-ci-result.temp.yml'
VERSION = '0.1.0'

COMMANDS = [
    RunTestCommand, RunReportCommand, RunFinishCommand, InitTemplateCommand,
    CheckConfigCommand, ShowConfigCommand
]

if __name__ == '__main__':
    print('Framgia CI Report Tool', VERSION)
    app = ReportApplication()
    app.config(YAML_CONFIGURE_FILE, RESULT_TEMP_FILE)
    for command in COMMANDS:
        app.register_command(command)
    app.run()
    sys.exit(0)
