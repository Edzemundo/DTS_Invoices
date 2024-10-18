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
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=False)
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
                p3 = multiprocessing.Process(target=run_scan_number())
                p3.start()
                p3.join()
                print(f"Monitoring for new files in directory...")
           
                
def run_scan_number():
    print("Running scan_number.py...")
    subprocess.run("python3 scan_number.py", shell=True)
    
def run_manual_watcher():
    while True:
        time.sleep(10)
        print("Scanning files in directory manually...")
        p3 = multiprocessing.Process(target=run_scan_number())
        p3.start()
        p3.join()
        
                       

if __name__ == "__main__":
    current_directory = os.getcwd()
    folderize

    # To be used when running in a virtual environment/container
    p1 = multiprocessing.Process(target=run_manual_watcher())
    p1.start()
    
    #To be used when running natively outside a virtual environment/container
    watcher = Watcher(current_directory)
    p2 = watcher.run()
    p2.start()

    p1.join()
    p2.join()