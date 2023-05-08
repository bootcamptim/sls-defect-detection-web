import os
import shutil
import time
import threading
from queue import Queue
import concurrent.futures

pi_dir = os.path.join('/Volumes', "fhcwdev's home", 'sls-defect-detection-pi', 'output')
dest_dir = os.path.join('output')

def get_files(directory):
    return set([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

def copy_file(file):
    try:
        src_file = os.path.join(pi_dir, file)
        dst_file = os.path.join(dest_dir, file)

        if os.path.exists(dst_file):
            pass
        else:
            shutil.copy2(src_file, dst_file)
            print(f'Copied {dst_file}')

    except Exception as e:
        print(f"Error occurred while copying file: {e}")

def poll_directory(queue, polling_interval=1):
    last_seen_files = get_files(pi_dir)

    while True:
        current_files = get_files(pi_dir)
        new_files = current_files - last_seen_files

        if new_files:
            # Sort files by creation time
            sorted_files = sorted(new_files, key=lambda f: os.path.getctime(os.path.join(pi_dir, f)))
            queue.put(sorted_files)

        last_seen_files = current_files
        time.sleep(polling_interval)

polling_interval = 0.5  # Polling interval in seconds
file_queue = Queue()

# Start a separate thread to poll the network drive
polling_thread = threading.Thread(target=poll_directory, args=(file_queue, polling_interval))
polling_thread.daemon = True
polling_thread.start()

print('Waiting for Files...')

try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            # Process new files if available
            if not file_queue.empty():
                new_files = file_queue.get()
                executor.map(copy_file, new_files)
            time.sleep(0.01)

except KeyboardInterrupt:
    print('\nAborted.')
