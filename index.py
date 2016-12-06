#!/usr/local/bin/python
# coding: utf-8

from report_app import ReportApplication
from commands.run_finish import RunFinishCommand
from commands.run_report import RunReportCommand
from commands.run_test import RunTestCommand

YAML_CONFIGURE_FILE = '.framgia-ci.yml'
RESULT_TEMP_FILE = '.framgia-ci-result.temp.yml'

if __name__ == '__main__':
    print("Framgia CI Report Tool")
    app = ReportApplication()
    app.config(YAML_CONFIGURE_FILE, RESULT_TEMP_FILE)
    app.register_command(RunTestCommand)
    app.register_command(RunReportCommand)
    app.register_command(RunFinishCommand)
    app.run()
