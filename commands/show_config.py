import sys
import os
import yaml

from cleo import Command


class ShowConfigCommand(Command):
    """
    Display current config

    show-config
    """

    def handle(self):
        print(yaml.dump(self.app.ci_reports, default_flow_style=False))
        sys.exit(0)
