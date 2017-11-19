#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import json
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import system
from pathlib import Path

from event import Event
from shared import Settings, colorize

LOG_ROOT = Path('~/Library/Logs/JacKit/').expanduser()
SERVER_LOG_FILE = (LOG_ROOT / 'jacserver.log').open('w')


def start():
  """Start the server
  """
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]

  httpd = HTTPServer((ip, 7086), HTTPRequestHandler)
  print('Start server listening at {}:7086 ...\n\n'.format(ip))
  httpd.serve_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
  """Handle the request sent to server"""

  server_version = 'JackServer/0.1'
  protocol_version = 'HTTP/1.1'  # enable persistent connection

  time_interval = 3
  last_timestamp = time.time()

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

    print(f'\n[38;2;255;100;0m{jsonDict["greeting"]}[0m\n\n')

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
    seconds = self.event.timestamp() - HTTPRequestHandler.last_timestamp

    if seconds > HTTPRequestHandler.time_interval:
      color1, color2 = Settings.colors['time_sep']

      delta = datetime.timedelta(seconds=seconds)
      prefix = colorize('\n -- ', color2)
      deltaColored = colorize(delta, color1)
      suffix = colorize(' elapsed ---\n', color2)
      timeLine = f'{prefix}{deltaColored}{suffix}'

      print(timeLine)

    HTTPRequestHandler.last_timestamp = self.event.timestamp()

  def log_message(self, format, *args):
    if args[1] != '200':
      SERVER_LOG_FILE.write(format % tuple(args) + '\n')
      SERVER_LOG_FILE.flush()


def main():
  try:
    system('stty -echo; clear; tput civis')
    start()
  except KeyboardInterrupt:
    exit(0)
  except Exception as e:
    exit(1)
  except ConnectionResetError:
    print('\n\nApp terminated, bye ....\n\n')
  else:
    exit(0)
  finally:
    system('tput cnorm; stty echo')


if __name__ == "__main__":
  main()
