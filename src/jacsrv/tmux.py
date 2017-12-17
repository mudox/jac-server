#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system


class Tmux:
  '''
  Tmux command manager:
  - Create specific tmux server for showing JacKit log
  - Create new window for each new project session group
  - Recreate the window for each new session of the project session group
  - Watch and destory windows if the underlying project session is inactive for a time
  - Recreate the window if a supposedly dead project turn up live some time later
  - ...
  '''

  def __init__(self):
    pass
