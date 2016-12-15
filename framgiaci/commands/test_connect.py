import sys
import time
import socket

from cleo import Command


class TestConnectCommand(Command):
    """
    Test connection to specific host and port

    test-connect
        {host : target host}
        {port : target port}
        {timeout? : custom timeout, defautl 120 seconds}
        {--debug : show error each try}
    """

    TIMEOUT = 120

    def try_connect(self, host, port, timeout=1, debug=False):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as e:
            if debug:
                self.line("<comment>%s</comment>" % e)
            return False

    def handle(self):
        host = self.argument('host')
        port = int(self.argument('port'))
        timeout = int(self.argument('timeout')) if self.argument('timeout') else self.TIMEOUT
        debug = self.option('debug')
        self.line("<comment>Try connect to %s:%s (timeout: %s seconds)</comment>" % (host, port, timeout))
        count = 0
        while count < timeout:
            count += 1
            if self.try_connect(host, port, timeout, debug=debug):
                self.line("<info>OK, %d tried</info>" % count)
                break
            time.sleep(1)

        sys.exit(0)
