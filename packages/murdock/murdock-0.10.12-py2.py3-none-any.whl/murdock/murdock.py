# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.murdock`
------------------------

Provides entry point main(): Parses command-line and configuration file, sets
up a Murdock `~.runner.Runner` runs it.

Signal handling:
~~~~~~~~~~~~~~~~

    SIGINT:
        Abort Murdock softly (rewrite all reports and result files).

    SIGTERM:
        Abort Murdock quickly (rewrite status and timing information).

    SIGKILL:
        Kill Murdock.

Exit status codes:
~~~~~~~~~~~~~~~~~~

    0:
        Murdock finished regularly with at least one successful docking run.

    1:
        Murdock aborted via signal, configuration error or bad input data.

    2:
        Murdock crashed unexpectedly.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import signal
import socket
import sys
import traceback
import warnings

from murdock import __version__, CRASH_MESSAGE, collected_warnings
from murdock.logger import Logger
from murdock.runner import Configuration, MurdockInterrupt, MurdockTerminate

def main():
    """Main entry point for Murdock.
    """
    sys.exit(_run())


def _handle_warning(message, category, filename, lineno):
    log.debug(
        '%s in file `%s`, line %d: %s.', category.__name__, filename, lineno,
        message)


def _raise_murdock_interrupt(signum, frame):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    raise MurdockInterrupt


def _raise_murdock_terminate(signum, frame):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    raise MurdockTerminate


def _run():
    cfg = Configuration()
    if not cfg.parse_command_line():
        return 1
    main_logger = Logger(
        name='murdock', group='murdock', logdir=cfg.cmdline.result_directory,
        filename='murdock.log', file_level=cfg.log_file_level,
        console_level=cfg.log_console_level)
    global log
    log = main_logger.logger
    warnings.showwarning = _handle_warning
    if not cfg.validate_command_line():
        return 1
    try:
        hostname = socket.gethostname()
    except:
        log.info('Start Murdock v%s.', __version__)
    else:
        log.info('Start Murdock v%s on `%s`.', __version__, hostname)
    for warn_args in collected_warnings:
        log.warning(*warn_args)
    cfg.log_command_line()
    try:
        if cfg.parse_configfile():
            log.info(
                'Configuration file `%s` parsed and verified successfully.',
                cfg.cmdline.config)
        else:
            log.fatal(
                'Parsing of configuration file `%s` failed.',
                cfg.cmdline.config)
            return 1
        log.info(
            'Murdock is working now. Check the other log files for details.')
        runner = cfg.setup()
        if not runner:
            log.fatal('Configuration error.')
            return 1
        if not runner.run():
            log.warning('Murdock finished with errors.')
            return 1
    except (MurdockInterrupt, MurdockTerminate):
        log.info('Murdock aborted.')
        return 1
    except:
        log.fatal(traceback.format_exc())
        log.fatal('Murdock crashed due to bad code. %s', CRASH_MESSAGE)
        return 2
    finally:
        log = main_logger.logger
        for handler in log.handlers:
            handler.setLevel(logging.INFO)
        log.info('Murdock done.')
        logging.shutdown()
    return 0


signal.signal(signal.SIGINT, _raise_murdock_interrupt)
signal.signal(signal.SIGTERM, _raise_murdock_terminate)
