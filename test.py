from slippi.parse import parse
from slippi.parse import ParseEvent
import sys
replay_file_path = 'D:/Documents/Code/Slippi-Ranked-Tool/replays/inprogress.slp'
#handlers = {ParseEvent.METADATA: print}
offset = 589
# handlers = {ParseEvent.START: print}
# parse(sys.stdin.buffer, handlers)
# Open the binary file in read mode
with open(replay_file_path, 'rb') as replay_file:
    # Seek to the desired offset from the beginning of the file
    replay_file.seek(offset)

    # Define event handlers
    handlers = {ParseEvent.START: print}

    # Parse the binary data from the desired offset
    parse(replay_file, handlers)