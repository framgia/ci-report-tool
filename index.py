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

YAML_CONFIGURE_FILE = '.framgia-ci.yml'
RESULT_TEMP_FILE = '.framgia-ci-result.temp.yml'
VERSION = '0.1.0'

if __name__ == '__main__':
    print('Framgia CI Report Tool', VERSION)
    app = ReportApplication()
    app.config(YAML_CONFIGURE_FILE, RESULT_TEMP_FILE)
    app.register_command(RunTestCommand)
    app.register_command(RunReportCommand)
    app.register_command(RunFinishCommand)
    app.register_command(InitTemplateCommand)
    app.register_command(RunAllCommand)
    app.register_command(CheckConfigCommand)
    app.run()
    sys.exit(0)
