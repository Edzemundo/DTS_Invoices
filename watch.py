import os
import time
import subprocess
# import multiprocessing
from file_handling import folderize


def run_scan_number():
    print(f"Running scan_number.py in {os.getcwd()}...")
    subprocess.run("python3 scan_number.py", shell=True)


def run_manual_watcher():
    while True:
        print("Scanning files in directory manually...")
        run_scan_number()
        time.sleep(15)


if __name__ == "__main__":
    folderize()  # Call folderize as a function
    try:
        run_manual_watcher()
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
        exit(0)

    # Alternative approach using multiprocessing (not recommended for docker containers).

    # Create processes
    # p1 = multiprocessing.Process(target=run_manual_watcher)

    # # Start processes
    # p1.start()

    # try:
    #     # Wait for processes to complete (which they won't, unless there's an error)
    #     while p1.is_alive():
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Keyboard interrupt received. Terminating processes.")
    # finally:
    #     # Ensure processes are terminated
    #     p1.terminate()
    #     p1.join()

    print("All processes have ended.")
