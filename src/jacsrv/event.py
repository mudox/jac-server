#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from textwrap import indent

from . import settings
from .screen import sgrRGB

LOG_ROOT = Path('~/Library/Logs/JacKit/').expanduser()
LOG_ROOT.mkdir(exist_ok=True)


class Event:

  # Hold all opened file object for each senssionID
  # Created on each `POST /session/`
  # Where
  #   - key: session ID
  #   - value: opened file object
  jsonFiles = {}
  logFiles = {}

  def __init__(self, jsonDict):
    self.jsonDict = jsonDict

  def sessionID(self):
    return self.jsonDict['sessionID']

  def timestamp(self):
    return self.jsonDict['timestamp']

  def subsystem(self):
    return self.jsonDict['subsystem']

  def level(self):
    return self.jsonDict['level']

  def message(self):
    return self.jsonDict['message']

  def logLine(self):
    symbol = settings.symbols[self.level()]
    color1, color2 = settings.colors[self.level()]

    headLine = sgrRGB(f' {symbol}{self.subsystem()}', color1)
    messageLines = indent(self.message(), '\x20' * 3)
    messageLines = sgrRGB(messageLines, color2)
    return '\n'.join([headLine, messageLines])
