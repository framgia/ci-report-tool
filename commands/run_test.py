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
                if 'enable' in options and options['enable']:
                    result = run_command(options['command'])
                    ignore = 'ignore' in options and options['ignore'] == True
                    results[tool] = {
                        "exit_code": result,
                        "ignore": ignore
                    }
            write_results(results, self.app.temp_file_name)
            sys.exit(0)
