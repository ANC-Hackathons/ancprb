import argparse
import time
import uuid

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
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_LOSS = 5

pebble_app_uuid = uuid.UUID("7f1e9122-6a6b-4b58-8e1a-484d5c51e861")

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

def game_win():
    messenger.send_message(pebble_app_uuid, {
        PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_WIN.value)
    })

def game_loss():
    messenger.send_message(pebble_app_uuid, {
        PebbleKeys.GAME_OVER.value: Uint8(PebbleKeys.GAME_LOSS.value)
    })

messenger = AppMessageService(pebble)
messenger.register_handler("appmessage", handler)

while(True):
    time.sleep(10)
    game_loss()
    time.sleep(10)
    game_win()

