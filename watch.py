import os
import time
import subprocess
import multiprocessing
from file_handling import folderize
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.event_handler = Handler()
        self.observer = Observer()

    def run(self):
        print(f"Monitoring directory: {self.directory_to_watch}")
        self.observer.schedule(
            self.event_handler, self.directory_to_watch, recursive=False
        )
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


# Custom event handler to handle file creation events
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            # Log the file creation event
            if not os.path.basename(event.src_path).startswith("temp_"):
                print(f"File created: {event.src_path}")
                # Perform additional actions, e.g., trigger another Python script
                time.sleep(5)
                run_scan_number()


def run_scan_number():
    print("Running scan_number.py...")
    subprocess.run("python3 scan_number.py", shell=True)


def run_watcher(directory):
    watcher = Watcher(directory)
    watcher.run()

def run_manual_watcher():
    while True:
        print("Scanning files in directory manually...")
        run_scan_number()
        time.sleep(15)


if __name__ == "__main__":
    current_directory = os.getcwd()
    folderize()  # Call folderize as a function

    watcher = Watcher(current_directory)

    # Create processes
    p1 = multiprocessing.Process(target=run_manual_watcher)
    p2 = multiprocessing.Process(target=run_watcher, args=(current_directory,))

    # Start processes
    p1.start()
    p2.start()

    try:
        # Wait for processes to complete (which they won't, unless there's an error)
        while p1.is_alive() and p2.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Terminating processes.")
    finally:
        # Ensure processes are terminated
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()
    
    print("All processes have finished.")
