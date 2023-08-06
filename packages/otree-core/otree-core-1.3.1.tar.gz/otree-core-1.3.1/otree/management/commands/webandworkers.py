#!/usr/bin/env python
import os
import re
import sys

from honcho.manager import Manager

from channels.log import setup_logger

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

naiveip_re = re.compile(r"""^
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
)$""", re.X)


class Command(BaseCommand):
    help = 'Run otree web services for the production environment.'

    default_port = 8000

    def add_arguments(self, parser):
        BaseCommand.add_arguments(self, parser)

        ahelp = ('TODO')
        parser.add_argument(
            '--reload', action='store_true', dest='use_reloader',
            default=False, help=ahelp)
        ahelp = (
            'Port number to listen on. Defaults to the environment variable '
            '$PORT (if defined), or 8000.'
        )
        parser.add_argument(
            '--port', action='store', type=int, dest='port', default=None,
            help=ahelp)
        parser.add_argument(
            '--addr', action='store', type=str, dest='addr', default='0.0.0.0',
            help='The host/address to bind to (default: 0.0.0.0)')
        parser.add_argument(
            '--botworker', action='store_true',
            dest='botworker', default=False,
            help='--botworker flag is deprecated and has no effect')

    def get_env(self, options):
        return os.environ.copy()

    def get_port(self, suggested_port):
        if suggested_port is None:
            suggested_port = os.environ.get('PORT', None)
        try:
            return int(suggested_port)
        except (ValueError, TypeError):
            return self.default_port

    def get_addr(self, suggested_addr):
        if not naiveip_re.match(suggested_addr):
            raise CommandError('--addr option must be a valid IP address.')
        return suggested_addr

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity', 1)
        self.logger = setup_logger('django.channels', self.verbosity)
        manager = self.get_honcho_manager(options)
        manager.loop()
        sys.exit(manager.returncode)

    def get_honcho_manager(self, options):
        self.addr = self.get_addr(options['addr'])
        self.port = self.get_port(options['port'])

        manager = Manager()

        daphne_cmd = 'daphne otree.asgi:channel_layer -b {} -p {}'.format(
            self.addr,
            self.port
        )

        print('Starting daphne server on {}:{}'.format(self.addr, self.port))

        manager.add_process('daphne', daphne_cmd, env=self.get_env(options))
        for i in range(3):
            manager.add_process(
                'worker{}'.format(i),
                'otree runworker',
                env=self.get_env(options))

        return manager
