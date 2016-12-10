import sys
import os

from cleo import Command


class RunAllCommand(Command):
    """
    Running test, report, finish command

    run
    """

    def handle(self):
        for command in ["test", "report", "finish"]:
            self.call(command)

        sys.exit(0)
