import os
import subprocess
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from slippi.parse import parse
from slippi.parse import ParseEvent
import sys

# Replace 'your_folder' with the folder you want to monitor
current_date = datetime.date.today()
formatted_date = current_date.strftime("%Y-%m")
folder_to_watch = "D:\Documents\Slippi\{}".format(formatted_date)
print(folder_to_watch)

# Function to process a new file
def process_new_file(file_path):
    print(f"Processing new file: {file_path}")
    time.sleep(1)
    print("Sleeping done")
    # Create the tail command
    tail_command = ['tail', '-c+1', '-f', file_path]

    # Start the tail process
    tail_process = subprocess.Popen(tail_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Monitor the output of the tail process in real-time
    while True:
        line = tail_process.stdout.readline()
        handlers = {ParseEvent.METADATA: print}
        parse(sys.stdin.buffer, handlers)
        print("===done===")
        if not line:
            break  # No more data from tail, exit the loop
        
    # Optionally, handle errors or perform cleanup
    print("terminating")
    tail_process.terminate()

# Define a custom event handler for new file creation
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".slp"):
            process_new_file(event.src_path)

# Create an observer that watches the folder
observer = Observer()
event_handler = NewFileHandler()
observer.schedule(event_handler, path=folder_to_watch, recursive=False)

# Start the observer
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
