import os

from cleo import Command
from framgiaci.common import read_yaml_file, read_template_file, merge_test_config

class CheckConfigCommand(Command):
    """
    Validate config file

    check-config
    """

    ALLOWED_BLOCKS = {
        'command': [str, list],
        'comment': bool,
        'ignore': bool,
        'enable': bool,
    }

    def handle(self):
        self.app.check_configure_file_exists()
        self.line('<info>Start checking...</info>')
        try:
            raw = read_yaml_file(self.app.configure_file_name)
            if 'project_type' not in raw:
                self.line("<comment>No project_type block found !</comment>")

            if 'from' in raw and raw['from'] not in self.app.PROJ_TYPES:
                self.line("<comment>Invalid project type '%s' !</comment>" % raw['from'])
            else:
                base = {}
                extended = {}
                if 'test' not in raw and 'from' not in raw:
                        self.line('<comment>No test block and from block found !</comment>')
                if 'test' in raw:
                    extended = raw['test']
                if 'from' in raw:
                    base = read_template_file(self.app.TEMPLATES_DIR, raw['from'])['test']

                merged_configs = merge_test_config(base, extended)
                for tool, config in merged_configs.items():
                    for key in config.keys():
                        if key not in self.ALLOWED_BLOCKS.keys():
                            self.line("<comment>Block '%s' in tool '%s' is invalid !</comment>" % (key, tool))
                        else:
                            actual = config[key]
                            expected = self.ALLOWED_BLOCKS[key]
                            if isinstance(expected, list):
                                if type(actual) not in expected:
                                    self.line("<comment>Value '%s' of block '%s' in tool '%s' is invalid !</comment>" % (actual, key, tool))
                            elif type(actual) != expected:
                                    self.line("<comment>Value '%s' of block '%s' in tool '%s' is invalid !</comment>" % (actual, key, tool))

        except Exception as e:
            self.line("<comment>Error: %s</comment>" % e)
        finally:
            self.line('<info>Done! Your configuration is valid!</info>')
