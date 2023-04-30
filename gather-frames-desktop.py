import os
import shutil
import filecmp
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# /Volumes/fhcwdev's home/sls-defect-detection-pi/output

# intialize paths
pi_dir = os.path.join('/Volumes', "fhcwdev's home", 'sls-defect-detection-pi', 'output')
dest_dir = os.path.join('output')

print(os.listdir(pi_dir))
print(os.listdir(dest_dir))

# intialize watchdog
class EventHandler(FileSystemEventHandler):

    def on_created(self, event):

        if not event.is_directory:

            try:
                src_file = event.src_path
                file = os.path.basename(src_file)
                dst_file = os.path.join(dest_dir, file)

                # Check if file exists in local folder
                if os.path.exists(dst_file):
                    pass

                else:
                    # If file does not exist copy
                    shutil.copy2(src_file, dst_file)
                    print(f'Copied {src_file}')

            except Exception as e:
                print(f"Error occurred while copying file: {e}")

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler, path=pi_dir, recursive=False)

try:
    observer.start()
    print("Watching for new files... Press Ctrl+C to stop.")

    while True:
        pass

except KeyboardInterrupt:
    observer.stop()

observer.join()