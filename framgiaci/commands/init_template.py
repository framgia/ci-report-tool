import os
import sys

from cleo import Command
from framgiaci.common import buid_template_file_path

class InitTemplateCommand(Command):
    """
    Init new config file base-ed on template. Supported project type: php, ruby, android, ios

    init
        {project_type : Supported project type}
        {--short : create compact init file}
    """

    def handle(self):
        project_type = self.argument('project_type')
        if project_type not in self.app.PROJ_TYPES:
            self.line('<error>Invalid project type !</error>')
        else:
            if os.path.isfile(self.app.configure_file_name):
                while True:
                    answer = input('Overwrite file (y/n) ?: ')
                    if answer in ['y', 'n']:
                        break
                    else:
                        self.line("<comment>Please response 'y' or 'n'</comment>")
            else:
                answer = 'y'

            if answer == 'y':
                with open(buid_template_file_path(self.app.TEMPLATES_DIR, project_type), 'r') as fin:
                    with open(self.app.configure_file_name, 'w') as fout:
                        if self.option('short'):
                            fout.write("from: %s" % project_type)
                        else:
                            fout.write(fin.read())
                        self.line("<info>Wrote to file: %s</info>" % self.app.configure_file_name)

        sys.exit(0)
