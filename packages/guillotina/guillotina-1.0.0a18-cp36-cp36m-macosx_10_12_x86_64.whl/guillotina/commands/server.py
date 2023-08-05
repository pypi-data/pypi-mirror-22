from aiohttp import web
from guillotina.commands import Command


try:
    import aiomonitor
    HAS_AIOMONITOR = True
except ImportError:
    HAS_AIOMONITOR = False


try:
    import aiohttp_autoreload
    HAS_AUTORELOAD = True
except ImportError:
    HAS_AUTORELOAD = False


class ServerCommand(Command):
    description = 'Guillotina server runner'

    def get_parser(self):
        parser = super(ServerCommand, self).get_parser()
        parser.add_argument('-m', '--monitor', action='store_true',
                            dest='monitor', help='Monitor', default=False)
        parser.add_argument('-r', '--reload', action='store_true',
                            dest='reload', help='Auto reload on code changes',
                            default=False)
        return parser

    def _run(self, arguments, settings, app):
        port = settings.get('address', settings.get('port'))
        web.run_app(app, host=settings.get('host', '0.0.0.0'), port=port)

    def run(self, arguments, settings, app):
        if arguments.monitor:
            if not HAS_AIOMONITOR:
                return print('You must install aiomonitor for the --monitor option to work'
                             'Use `pip install aiomonitor` to install aiomonitor.')
            # init monitor just before run_app
            loop = self.get_loop()
            with aiomonitor.start_monitor(loop=loop):
                self._run(arguments, settings, app)
        if arguments.reload:
            if not HAS_AUTORELOAD:
                return print('You must install aiohttp_autoreload for the --reload option to work'
                             'Use `pip install aiohttp_autoreload` to install aiohttp_autoreload.')
            aiohttp_autoreload.start()

        self._run(arguments, settings, app)
