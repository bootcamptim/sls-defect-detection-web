import os
import shutil
import filecmp
import time

# /Volumes/fhcwdev's home/sls-defect-detection-pi/output

# intialize paths
pi_dir = os.path.join('/Volumes', "fhcwdev's home", 'sls-defect-detection-pi', 'output')
dest_dir = os.path.join('output')

def get_files(directory):
    return set([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])


def copy_files(network_files):
    for file in network_files:
        try:
            src_file = os.path.join(pi_dir, file)
            dst_file = os.path.join(dest_dir, file)

            # Check if file exists in local folder
            if os.path.exists(dst_file):
                pass
                   
            else:
                # If file does not exist copy
                shutil.copy2(src_file, dst_file)
                print(f'Copied {dst_file}')

        except Exception as e:
            print(f"Error occurred while copying file: {e}")

last_seen_files = get_files(pi_dir)

try:
    while True:
        print("Checking for new files...")
        current_files = get_files(pi_dir)
        new_files = current_files - last_seen_files
        if new_files:
            print("New files found: ", new_files)
            copy_files(new_files)
        last_seen_files = current_files
        time.sleep(1)  # wait for 1 second before checking again

except KeyboardInterrupt:
    print("File monitoring stopped.")