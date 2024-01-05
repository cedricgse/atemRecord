import argparse
import json
from pyatem.command import RecorderStatusCommand, RecordingSettingsSetCommand, CutCommand, PreviewInputCommand
from pyatem.protocol import AtemProtocol


def connection_ready(*args):
    global looping
    select = PreviewInputCommand(index=0, source=_switch_to)
    switch = CutCommand(index=0)
    recordSettings = RecordingSettingsSetCommand(filename = _filename)
    record = RecorderStatusCommand(recording = True)
    switcher.send_commands([select, switch, recordSettings, record])
    switcher.loop()
    looping = False



with open("atem.config", "r") as config_file:
    config = json.load(config_file)

switcher = None
looping = True
_switch_to = None
_filename = "Record"

parser = argparse.ArgumentParser(description="Start Recording")
parser.add_argument('source', help='Index of Source (0-4)')
parser.add_argument('filename', help='Output file name')
args = parser.parse_args()

_switch_to = int(args.source)
_filename = args.filename

switcher = AtemProtocol(ip=config["atemIP"])

switcher.on('connected', connection_ready)

switcher.connect()
while looping:
    switcher.loop()
