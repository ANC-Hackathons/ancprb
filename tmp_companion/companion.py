import argparse
import time

from enum import Enum

from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.services.appmessage import *
from libpebble2.events import BaseEventHandler
from libpebble2.protocol import *

parser = argparse.ArgumentParser()
parser.add_argument('--serial', type=str, default="/dev/cu.PebbleTime1EBA-SerialPo", help="Connect to Pebble directly, given a path to a serial device. Should look something like: /dev/cu.PebbleTimeXXXX-SerialPo")

class PebbleKeys(Enum):
    BUTTON_PRESS_KEY = 0
    LEFT_PRESS = 1
    RIGHT_PRESS = 2

pebble = PebbleConnection(SerialTransport(parser.parse_args().serial))
pebble.connect()
pebble.run_async()
print "Connection established to:", parser.parse_args().serial

def handler(self, uuid, data):
    if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.LEFT_PRESS.value:
        print PebbleKeys.LEFT_PRESS.name
        # Code to update LEFT rotation / position goes here

    if data[PebbleKeys.BUTTON_PRESS_KEY.value] == PebbleKeys.RIGHT_PRESS.value:
        print PebbleKeys.RIGHT_PRESS.name
        # Code to update RIGHT rotation / position goes here

messenger = AppMessageService(pebble)
messenger.register_handler("appmessage", handler)

while(True):
    time.sleep(1)

