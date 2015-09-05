import argparse

from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.protocol import *

parser = argparse.ArgumentParser()
parser.add_argument('--serial', type=str, default="/dev/cu.PebbleTime1EBA-SerialPo", help="Connect to Pebble directly, given a path to a serial device. Should look something like: /dev/cu.PebbleTimeXXXX-SerialPo")

pebble = PebbleConnection(SerialTransport(parser.parse_args().serial))
pebble.connect()
pebble.run_async()

def handler(self):
    print "in handler"

pebble.register_endpoint(PingPong, handler)

pebble.send_packet(PingPong(message=Ping(), cookie=53))
pebble.send_packet(PingPong(message=Ping(), cookie=53))
pebble.send_packet(PingPong(message=Ping(), cookie=53))
print pebble.read_from_endpoint(PingPong)

