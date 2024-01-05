import argparse
import json
from pyatem.command import RecorderStatusCommand
from pyatem.protocol import AtemProtocol


def connection_ready(*args):
    global looping
    record = RecorderStatusCommand(recording = False)
    switcher.send_commands([record])
    switcher.loop()
    looping = False



with open("atem.config", "r") as config_file:
    config = json.load(config_file)

switcher = None
looping = True

switcher = AtemProtocol(ip=config["atemIP"])

switcher.on('connected', connection_ready)

switcher.connect()
while looping:
    switcher.loop()
