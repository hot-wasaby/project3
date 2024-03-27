Introduction:
The Folder Monitor is a Python script designed to monitor a specified folder for changes in its contents. It can detect additions, deletions, and modifications of files within the monitored folder. This user manual provides instructions on how to use the Folder Monitor script effectively.

Requirements:

Python 3.x installed on your system.
Basic understanding of using the command line or terminal.
Setup:

Download the Python script file (folder_monitor.py) to your local machine.
Ensure that Python is properly installed and configured on your system.
Usage:

Run the Script:

Open a command line or terminal window.
Navigate to the directory containing the folder_monitor.py script.
Run the script by executing the command: python folder_monitor.py.
Input Commands:

After running the script, you'll be prompted to input commands.
The available commands are:
commit: Takes a snapshot of the current folder state, recording any changes.
info filename: Displays detailed information about a specific file in the monitored folder.
status: Prints the status of the monitored folder, showing changes since the last commit.
exit: Terminates the script and exits the program.
Committing Changes:

To capture the current state of the folder, use the commit command.
This action records all additions, deletions, and modifications of files since the last commit.
It updates the log file with the snapshot time and details of added, deleted, and changed files.
File Information:

Use the info filename command to retrieve detailed information about a specific file.
Replace filename with the name of the file you want to inspect.
Information includes file extension, creation time, update time, and additional details based on file type (e.g., line count, word count, character count).
Folder Status:

The status command provides an overview of changes since the last commit.
It displays the time of the last commit and lists files that have been added, deleted, or modified since then.
Exiting the Program:

To exit the Folder Monitor program, simply input the exit command.
This will terminate the script and close the program.
Important Notes:

Ensure that the folder path specified in the script (folder_path) points to the directory you want to monitor.
The script runs continuously, monitoring the folder for changes in real-time.
The log file (Log.txt) records all events and changes detected by the Folder Monitor.
Modifications to files include changes in content as well as metadata such as creation and modification times.
By following these instructions, you can effectively utilize the Folder Monitor script to track changes within your designated folder and stay informed about file modifications, additions, and deletions.
