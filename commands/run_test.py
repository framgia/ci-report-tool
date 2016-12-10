import sys

from cleo import Command

from common import print_header, run_command, write_results


class RunTestCommand(Command):
    """
    Running test tools

    test
    """

    def handle(self):
        print_header("Running Test")
        if self.app.ci_reports['test']:
            test_commands = self.app.ci_reports['test']
            results = {}
            for tool, options in test_commands.items():
                if options.get('enable', True):
                    to_run_cmds = []
                    if isinstance(options['command'], str):
                        to_run_cmds.append(options['command'])
                    elif isinstance(options['command'], list):
                        to_run_cmds = options['command']

                    general_result = 0
                    for command in to_run_cmds:
                        general_result = run_command(command)
                        if general_result:
                            break

                    results[tool] = {
                        "exit_code": general_result,
                        "ignore": options.get('ignore', False) == True
                    }
            write_results(results, self.app.temp_file_name)
            sys.exit(0)
