import os
import subprocess

original_script=r'''#-- Generated file from everything-newforma-sync-install.py
import json
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import subprocess
import re
from datetime import datetime

saved_ini_file_path = None
prepend = ""
debug = True

#-- Step 1 --

def startup():
    global saved_ini_file_path
    saved_ini_file_path = read_config()
    if saved_ini_file_path:
        return True
    else:
        saved_ini_file_path = get_ini_file_path()
        if saved_ini_file_path:
            return True
        else:
            return False

def read_config():
    global prepend
    config_file_path = get_config_file_path()
    if os.path.exists(config_file_path):
        print("Found config, reading")
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
        print("Found saved INI file path:", config.get("ini_file_path"))
        if config.get("prepend"):
            prepend = config.get("prepend")
            print(f"Prepend found:{prepend}")
            prepend = prepend + ","
        return config.get("ini_file_path")
    else:
        print("No config, continuing")
        return None

def get_ini_file_path():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(title="Select the Everything .INI File", filetypes=(("INI files", "*.ini"), ("All files", "*.*")))
    
    if file_path:
        print("Selected INI file:", file_path)
        save_config(file_path)
        return file_path
    else:
        print("No INI file selected.")
        return None

def save_config(ini_file_path):
    print("Saving config file for future runs")
    config = {"ini_file_path": ini_file_path}
    config_file_path = get_config_file_path()
    with open(config_file_path, "w") as config_file:
        json.dump(config, config_file)
    print("Config file saved to:", config_file_path)

def get_config_file_path():
    print("Checking for config file")
    appdata_path = os.getenv('APPDATA')
    return os.path.join(appdata_path, "everything-newforma-sync-config.json")

#-- Step 2 --

def list_shortcut_targets(folder_path):
    print("Reading folder contents")
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")
    
    targets = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".lnk"):
            lnk_path = os.path.join(folder_path, filename)
            target, args = parse_lnk_file(lnk_path)
            if debug:
                print(target)
            if target:
                targets.append(target)
    return ",".join(targets)

def parse_lnk_file(link_path) -> (str, str):
    """
    Get the target & args of a Windows shortcut (.lnk)
    :param link_path: The Path or string-path to the shortcut, e.g. "C:\\Users\\Public\\Desktop\\My Shortcut.lnk"
    :return: A tuple of the target and arguments, e.g. ("C:\\Program Files\\My Program.exe", "--my-arg")
    """
    # get_target implementation by hannes, https://gist.github.com/Winand/997ed38269e899eb561991a0c663fa49
    ps_command = \
        "$WSShell = New-Object -ComObject Wscript.Shell;" \
        "$Shortcut = $WSShell.CreateShortcut(\"" + str(link_path) + "\"); " \
        "Write-Host $Shortcut.TargetPath ';' $shortcut.Arguments "
    output = subprocess.run(["powershell.exe", ps_command], capture_output=True)
    raw = output.stdout.decode('utf-8')
    launch_path, args = [x.strip() for x in raw.split(';', 1)]
    return launch_path, args
    # TODO - Find a faster alternative to using Powershell like this

#-- Step 3 --

def copy_file_to_backup(original_file_path):
    print("Backing up INI file")
    try:
        # Get the directory and file name without extension
        directory, filename = os.path.split(original_file_path)
        filename_no_ext, ext = os.path.splitext(filename)    
        # Get the current datetime in a formatted string
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")     
        # Construct the backup file path with datetime
        backup_file_path = os.path.join(directory, f"{filename_no_ext}_backup_{current_datetime}{ext}")
        # Copy the file to backup
        shutil.copy(original_file_path, backup_file_path)
        print(f"File copied from {original_file_path} to {backup_file_path}")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

def replace_lines(file_path, pattern, new_line):
    flag = False
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if pattern.match(line):
                flag = True
                file.write(new_line + '\n')
            else:
                file.write(line)
    if flag:
        print("Found line")
        return True
    else:
        print("Couldn't fine line")
        return False

#-- Main --

if __name__ == "__main__":
    # Step 1
    print("Step 1 -- Starting up")
    if not startup():
        print("Startup failed, no config / INI")
        raise SystemExit

    # Step 2
    print("Step 2 -- Loading data")
    targets = list_shortcut_targets(os.path.expanduser("~/Documents/My Newforma Projects/"))
    print("Targets: ", targets) # DEBUG

    # Step 3
    print("Step 3 -- Modifying data")
    copy_file_to_backup(saved_ini_file_path)
    regex = re.compile(r'^folders=.*$', re.IGNORECASE)
    replace_lines(saved_ini_file_path, regex, f"folders={prepend}{targets}")
    print("Done")
'''

# Function to check if a file exists in the startup folder
def check_startup_file(filename):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    file_path = os.path.join(startup_folder, filename)
    return os.path.isfile(file_path)

# Function to create the file and write content to it if it doesn't exist
def create_startup_file(filename, content):
    print("Executing the script...")
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    file_path = os.path.join(startup_folder, filename)
    with open(file_path, 'w') as file:
        file.write(content)

def execute_startup_file(filename):
    print("Executing script")
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    file_path = os.path.join(startup_folder, filename)
    subprocess.run(["python", file_path])

if __name__ == "__main__":
    filename = "everything-newforma-sync.py"
    if not check_startup_file(filename):
        create_startup_file(filename, original_script)
        print(f"File '{filename}' created in the startup folder.")
    else:
        print(f"File '{filename}' already exists in the startup folder.")
    execute_startup_file(filename)
    print("Done")
