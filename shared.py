#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Settings:

  symbols = {
      'error': ' ',
      'warning': ' ',
      'info': ' ',
      'debug': ' ',
      'verbose': ' ',
  }

  colors = {
      'error': ((200, 0, 0), (255, 255, 255)),
      'warning': ((255, 87, 191), (255, 255, 255)),
      'info': ((255, 224, 102), (255, 255, 255)),
      'debug': ((64, 255, 64), (255, 255, 255)),
      'verbose': ((155, 155, 155), (130, 130, 130)),
      'time_sep': ((130, 130, 130), (70, 70, 70)),
  }


def colorize(text, rgb):
  r, g, b = rgb
  return f'\033[38;2;{r};{g};{b}m{text}\033[0m'
