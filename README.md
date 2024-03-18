*No warranty of any kind. Use at your own peril.*

# everything-newforma-sync
## Intro
The purpose of this script is to synchronize your [Everything](https://www.voidtools.com/) configuration file with Newforma. This will update the Everything INI file so that it searches any folders in your Newforma "My Projects". In order to do this we rely on Newforma's function where it saves MS `.lnk` files to `This PC\My Newforma Projects`.

![image](https://github.com/KaiStarkk/everything-newforma-sync/assets/1722064/9bdc3fe2-5794-4d5a-8a89-7797ce578f81)

## Install
Download this .py file and run it.
You might need to [install Python first](https://www.python.org/downloads/) - it can be installed to `%APPDATA%` (administrative privileges not required).

## Functions
The rough order of operations is as below:
- This install script installs another python file in your startup directory (`~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup`).
- That other script does these operations each time the computer starts
    - Step 1 - Starting up
        - Check for its own config (saved in `%APPDATA%`)
        - If it finds it, read the Everything INI file path
        - Otherwise, ask for the Everything INI file path
        - Save the path to the config file to simplify future runs
    - Step 2 - Loading data
        - Loads all LNK files in the Newforma folder
        - Reads their binary data using PowerShell to find the link target
        - Compiles a CSV of all targets
    - Step 3 - Modifying data
        - Backs up the INI file to `original-path_backup_datetime.ini` 
        - Creates a regex pattern to match the requisite line in Everything's INI file
        - Reads through the INI file and replaces the corresponding line with the new targets

## NB
Due to needing to build a config on first run, the installer also runs the script after installing it. In the file dialog that opens, the user needs to select their Everything.INI file location. Depending on how you installed Everything, this might be `%APPDATA%\Everything`, or if you downloaded and extracted a portable version, wherever you extracted it (e.g. `Downloads` folder / `Desktop` / your personal `OneDrive`, or similar).

## FAQ
You can reach me at my work email for questions.

## Known issues
- Since it's a straight sync, any other folders you've added to Everything will be removed. Will look at a workaround.
- Only runs on startup, it's not a daemon watching the folder, so if you don't shut down your computer you'll need to manually run it to update after changing Newforma proejcts. 
- It's kinda slow. This is because of the PowerShell module for reading LNK files. In the future I'd like to manually read the data from the binary file based on the [Shell Link binary file format](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-shllink/16cb4ca1-9339-4d0c-a68d-bf1d6cc0f943)
- This is currently a manual install process. Would be nice to create a package on PIP so people can install that way; not a priority though since corporate environment often blocks pip.
