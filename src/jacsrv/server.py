#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import json
import logging
import socket
import time
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import system

from . import settings
from .event import Event
from .screen import sgrRGB

logger = logging.getLogger(__name__)


def getFreePort():
  with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
    sock.bind(('', 0))
    return sock.getsockname()[1]


def getIPAddress():
  with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
    sock.connect(('8.8.8.8', 80))
    return sock.getsockname()[0]


def start(port):
  ip = getIPAddress()

  try:
    server = HTTPServer((ip, port), HTTPRequestHandler)
    print(f'Start server listening at {ip}:{port} ...\n\n')

  except OSError as e:
    if e.errno == 48:
      alternatePort = getFreePort()
      print(f'Port {port} is occupied, try using port {alternatePort}')
      server = HTTPServer((ip, alternatePort), HTTPRequestHandler)
      print(f'Start server listening at {ip}:{alternatePort} ...\n\n')
    else:
      raise

  server.serve_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
  """Handle the request sent to server"""

  server_version = 'JackServer/0.1'
  protocol_version = 'HTTP/1.1'  # enable persistent connection

  lastTimestamp = time.time()

  def do_POST(self):
    if self.path == '/session/':
      self.newSession()
    elif self.path == '/event/':
      self.newEvent()
    else:
      self.send_error(
          403,
          'Invalid API path',
          '''
          Currently JackServeronly support:

            - POST /session/ HTTP/1.1
              Notify of a new Xcode project running session

            - POST /event/   HTTP/1.1
              Send a new event
          '''
      )
      return

  def newSession(self):
    self.send_response(200)
    self.send_header('Content-Length', 0)
    self.end_headers()

    # TODO: request body containing session info not used yet
    size = int(self.headers['Content-Length'])
    jsonDict = json.loads(self.rfile.read(size))

    print('\n' * 20)
    system('clear')

    print(f'\n\x1b[38;2;255;100;0m{jsonDict["greeting"]}\x1b[0m\n\n')

  def newEvent(self):
    self.send_response(200)
    self.send_header('Content-Length', 0)
    self.end_headers()

    size = int(self.headers['Content-Length'])
    jsonDict = json.loads(self.rfile.read(size))
    self.event = Event(jsonDict)

    self.printTimeSeparatorIfNeeded()
    print(self.event.logLine())

  def printTimeSeparatorIfNeeded(self):
    seconds = self.event.timestamp() - HTTPRequestHandler.lastTimestamp

    if seconds > settings.timeInterval:
      color1, color2 = settings.colors['time_sep']

      delta = datetime.timedelta(seconds=seconds)
      prefix = sgrRGB('\n -- ', color2)
      deltaColored = sgrRGB(delta, color1)
      suffix = sgrRGB(' elapsed ---\n', color2)
      timeLine = f'{prefix}{deltaColored}{suffix}'

      print(timeLine)

    HTTPRequestHandler.lastTimestamp = self.event.timestamp()

  def log_message(self, format, *args):
    if args[1] != '200':
      logger.debug(format % tuple(args) + '\n')
