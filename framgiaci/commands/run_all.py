import sys
import os

from cleo import Command


class RunAllCommand(Command):
    """
    Running test, report, finish command

    run
        {--local : run test and finish only}
    """

    def handle(self):
        self.app.check_configure_file_exists()
        commands = ['test', 'upload', 'finish']
        if self.option('local'):
            commands.remove('upload')
        for command in commands:
            try:
                self.call(command)
            except SystemExit as exception:
                if exception.code:
                    sys.exit(exception.code)

        sys.exit(0)
