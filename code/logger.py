#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import datetime
import logging
import colorlog


# setup console logs
def setup_console_log():
    log = logging.getLogger()  # root logger
    log.setLevel(logging.INFO)
    format_str = "%(asctime)s - [%(filename)30s:%(lineno)3s - %(funcName)25s() ]- %(levelname)s - %(message)s"
    date_format = '%d-%b-%y %H-:%M:%S'
    cformat = '%(log_color)s' + format_str
    colors = {'DEBUG': 'green',
              'INFO': 'cyan',
              'WARNING': 'bold_yellow',
              'ERROR': 'bold_red',
              'CRITICAL': 'bold_purple'}
    formatter = colorlog.ColoredFormatter(cformat, date_format, log_colors=colors)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log


def setup_file_handler():
    log_formatter = logging.Formatter(
        "%(asctime)s - [%(filename)30s:%(lineno)3s - %(funcName)25s() ]- %(levelname)s - %(message)s",
        datefmt='%d/%m/%Y %H:%M:%S')
    # Setup File handler
    now = datetime.datetime.now()
    log_file = os.path.join(os.getcwd(), 'logs', 'output_' + now.strftime("%Y_%m_%d") + '.log')
    file_handler = logging.FileHandler(log_file, "a", "UTF-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    return file_handler


# choose either with log file or not
def logger_config(with_file=False):
    # output to console
    app_log = setup_console_log()
    if with_file:   # output to file
        file_handler = setup_file_handler()
        app_log.addHandler(file_handler)
    return app_log


def change_level(level):
    print(level)