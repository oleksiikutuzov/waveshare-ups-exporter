from prometheus_client import start_http_server
import logging
import time
import sys
import os
import waveshare_ups
from INA219 import INA219
import signal
from threading import Event

"""
Environment variable labels used to read values from.
UPDATE_INTERVAL Sets interval between updates in seconds, default is 10.0 seconds
"""

TIMEOUT_LABEL = 'UPDATE_INTERVAL'

exit = Event()


def signalShuttdown(self, *args):
    exit.set()


config = {
    'host_port': 9090,
    'lat': '',
    'lon': '',
    'token': '',
    'timeout': 10.0
}

if TIMEOUT_LABEL in os.environ:
    config['timeout'] = float(os.environ[TIMEOUT_LABEL])


def create_logger(scope):
    logger = logging.getLogger(scope)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%dT%H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':

    logger = create_logger('waveshare-ups-exporter')

    start_http_server(config['host_port'])

    signal.signal(signal.SIGTERM, signalShuttdown)
    signal.signal(signal.SIGHUP, signalShuttdown)
    signal.signal(signal.SIGINT, signalShuttdown)
    signal.signal(signal.SIGABRT, signalShuttdown)

    ina219 = INA219(addr=0x42)

    while not exit.is_set():

        waveshare_ups.extract_metrics(logger, ina219)
        logger.info(f"Request succeeded")

        sleepTime = 0.0

        while (config['timeout'] > sleepTime) and not exit.is_set():
            time.sleep(0.1)
            sleepTime += 0.1

    logger.info("shutting down")
