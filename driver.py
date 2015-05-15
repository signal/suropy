#!/usr/bin/env python
"""Simple program to exercise the suro client class.

Usage:
  driver.py [--host=<h>] [--port=<p>] [--key=<k>] MESSAGE ...

Arguments:
   MESSAGE string messages to send, each message should be enclosed in quotes

Options:
  --key=<k>  The routing key to use for the messages [default: suropy-driver]
  --host=<h>  The hostname of the suro server to connect to [default: localhost]
  --port=<p>  The port of the suro server to connect to [default: 7101]
"""

from docopt import docopt
import logging
from logging import config
from thrift import Thrift

from suro.client import SuroClient

logging_config = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "console": {
      "format": "%(asctime)s %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "console",
      "level": logging.DEBUG,
      "stream": "ext://sys.stdout"
    }
  },
  "root": {
    "level": logging.DEBUG,
    "handlers": ["console"]
  }
}

if __name__=="__main__":
  args = docopt(__doc__)
  config.dictConfig(logging_config)
  try:
    with SuroClient(args['--host'], int(args['--port'])) as client:
      client.send_messages(args['--key'], *[x.encode('utf-8') for x in args['MESSAGE']])
  except Thrift.TException, tx:
    print '%s' % (tx.message)
