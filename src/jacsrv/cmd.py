#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from os import system

from jaclog import jaclog

from . import server, settings

__version__ = '1.0.0'


class Command():

  def __init__(self):
    self.parser = argparse.ArgumentParser(
        description='JacServer, server side of the iOS logging framework JacKit')

    self.parser.add_argument(
        '-p',
        '--port',
        help='Port number (default: 7080)',
        default=7086,
        type=int
    )

    self.parser.add_argument(
        '-t',
        '--time-interval',
        dest='timeInterval',
        help='Interval (in seconds) for a time line (default: 3)',
        default=3,
        type=int
    )

  def run(self):

    try:
      # disable terminal echo & hide cursor
      system('stty -echo; clear; tput civis')

      args = self.parser.parse_args()
      settings.port = args.port
      settings.timeInterval = args.timeInterval

      jaclog.configure(appName='jacsrv', fileName=f'port{settings.port}.log')

      server.start(args.port)
    except KeyboardInterrupt:
      exit(0)
    except ConnectionResetError:
      server.log('\n\nConnection is reset, bye ....\n\n')
    else:
      exit(0)
    finally:
      # unhidden cursor & re-enalbe terminal eche
      system('tput cnorm; stty echo')


def run():
  Command().run()
