#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import socket
import time
from datetime import datetime
from time import sleep

import requests

from event import Event

SESSION_TIMESTAMP = datetime.now().isoformat(timespec='milliseconds')


class FakeEvent:

  levels = ('error', 'warning', 'info', 'debug', 'verbose')
  appNames = ('JacKit', 'iOSKit', 'SocialKit', 'RandomUser')
  subsystems = (
      'AppDelegate',
      'HomeViewController.viewDidAppear',
      'JacKit.wakeup',
      'SocialKit.QQSDKManager.shareTo',
      'SocialKit.WeiboSDKManager.loginTo',
      'RandomUser.RamdomUserGenerator.females',
      'iOSKit.MBProgressHUB.show',
      'iOSKit.The.xApp',
  )
  bundleIDPrefix = 'io.github.mudox'

  def __init__(self):
    self.sessionID = '{}.{}-{}'.format(
        FakeEvent.bundleIDPrefix,
        random.choice(FakeEvent.appNames),
        SESSION_TIMESTAMP
    )
    self.timestamp = time.time()
    self.level = random.choice(FakeEvent.levels)
    self.subsystem = random.choice(FakeEvent.subsystems)
    self.message = self._random_message()

  def _random_message(self):
    return '\n'.join([f'message at line #{no}'
                      for no in range(random.randrange(1, 6))])

  def jsonDict(self):
    return {
        'sessionID': self.sessionID,
        'timestamp': self.timestamp,
        'level': self.level,
        'subsystem': self.subsystem,
        'message': self.message,
    }


class Test:

  def __init__(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    self.hostIP = s.getsockname()[0]
    print(f'Host IP address: {self.hostIP}\n')

  def start(self):
    self.postANewSession()

    while True:
      baseInterval = 0.03
      interval = random.randrange(20) * 0.04
      sleep(baseInterval + random.randrange(15) * interval)

      dice = random.randrange(18)
      if dice == 0:
        self.postANewSession()
      else:
        self.postAEvent()

  def postAEvent(self):
    e = Event(FakeEvent().jsonDict())
    print('\n' + e.logLine())

    try:
      requests.post(
          f'http://{self.hostIP}:7086/event/',
          data=json.dumps(e.jsonDict),
          timeout=3
      )
    except requests.exceptions.Timeout:
      print('\n   [x] timeout ...')
    except requests.exceptions.ConnectionError:
      print('\n   [x] connection error ...')

  def postANewSession(self):
    session = {
        'bundleID': f'io.github.mudox.JacServerFakeApp.{random.randrange(1, 7)}',
        'timestamp': time.time(),
    }
    print("\n\n---- NEW SESSION ----\n\n")
    try:
      requests.post(
          f'http://{self.hostIP}:7086/session/',
          data=json.dumps(session),
          timeout=3
      )
    except requests.exceptions.Timeout:
      print('\n   [x] timeout ...')
    except requests.exceptions.ConnectionError:
      print('\n   [x] connection error ...')


if __name__ == "__main__":
  Test().start()
