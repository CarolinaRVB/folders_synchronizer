# One-Way Folder Synchronizer

## Overview
The One-Way Folder Synchronizer is a Python program designed to synchronize two folders: a **source** folder and a **replica** folder. The synchronization process ensures that the replica folder matches the contents of the source folder, copying new or modified files from the source and removing any files in the replica that are no longer present in the source.

## Features
- **Synchronization Thread**: A dedicated thread runs the synchronization process continuously, checking for changes in the source folder at specified intervals. This allows the program to perform synchronization operations in the background without blocking the main execution flow.
- **Input Thread**: A separate thread listens for user input, allowing the user to terminate the synchronization process gracefully by typing "stop". This means the user can interact with the program without interrupting the ongoing synchronization.
- **Argument Parsing**: Parses the arguments to verify folder's existence. Has commented section to run the program without the requirement of arguments. Creates default files and folders. 
- **File Comparison:** Uses file size, folders size, file permissions, and MD5 hash checks to verify the equality of files in the source and replica.
- **Error Handling:** Logs errors and warnings during the synchronization process, allowing for easier troubleshooting.
- **User Input Control:** Allows users to terminate the synchronization process gracefully.
- **Cross-Platform Support:** Works on various operating systems due to the use of the `pathlib` and `os` libraries.

## Installation
Ensure you have Python 3 installed on your machine. You can download Python from [python.org](https://www.python.org/downloads/).

Clone this repository or download the script files to your local machine.

## Usage
To run the program, use the following command in your terminal:

```bash
python3 main.py --source_path [sourcePath] --replica_path [replicaPath] --logfile_path [log] --sync_interval [interval in seconds]
```
## Arguments
- **source_path**: The path to the source folder that you want to synchronize from.
- **replica_path**: The path to the replica folder that you want to synchronize to.
- **logfile_path**: The path where the log file will be created to record synchronization events and errors.
- **sync_interval**: The time interval (in seconds) at which the synchronization should occur.

## Example
```bash
python3 main.py --source_path source --replica_path replica --logfile_path logger --sync_interval 5
```
**NOTE:** Program also works if no arguments are provided - sets default behavior

## Logging
The program logs all operations to the specified logfile and outputs to the console. Each log entry includes a timestamp, the logger name, log level, and a message describing the operation performed.

## Termination
To stop the synchronization process, type stop in the terminal. You can also terminate the program using Ctrl+C, which will invoke a graceful shutdown and log the termination.

## Error Handling
If the source or replica path is invalid, or if there are issues accessing files, the program will output an error message and terminate.

## Requirements
Python 3.x
os, sys, time, shutil, filecmp, logging, hashlib, pathlib, and threading standard libraries (included with Python).

## Documentation

## Main

**Functions:**

- **signal_handler(sig, frame)** 
Handles termination signals (Ctrl+C) by printing a warning message and exiting the program gracefully.

- **input_thread(stop_thread)** 
Runs a loop that prompts the user to input a command to stop synchronization. If the input matches the termination command, it sets the stop_thread event. It continues until the stop_thread is set.

- **set_logging(logfile)** 
Configures logging for the application, creating a logger that writes messages to both a specified log file and the console. Returns the configured logger instance.

**main() Initializes the application:**
- Parses command-line arguments to obtain the source folder, replica folder, log file, and synchronization interval.
- Sets up a signal handler for graceful termination.
- Creates a threading event to control synchronization stopping.
- Configures logging for the application.
- Starts a separate thread for user input to stop synchronization.
- Initializes the Sync class with the parsed parameters and starts the synchronization thread.
- Waits for the synchronization thread to finish.

## Class and Method Descriptions
# class Sync
This class handles folder synchronization between a source and replica folder.

**Attributes:**
- source (Path): The directory from which files are synchronized.
- replica (Path): The directory to which files are synchronized.
- logfile (Path): The path to the log file where events are recorded.
- interval (int): Time interval between synchronization checks.
- stop_thread (threading.Event): Event to stop the synchronization thread.
- logger (Logger): Logger object to log synchronization events.

**Methods:**

- **__init__(source, replica, logfile, interval, stop_thread, logger)**
Initializes the synchronization process with the provided source, replica, and logging configuration.

- **sync_thread()**
Starts the synchronization process, running it continuously at the defined interval. The process stops when stop_thread is set.

- **synchronize()**
Compares the source and replica folders. If both exist, proceeds with synchronization; otherwise, logs an error.

- **update_folder_and_log(result)**
Based on the comparison result (dircmp object), handles file and folder synchronization by calling helper methods.

- **delete_extra_replica_files(result)**
Deletes files or directories that exist only in the replica folder.

- **copy_new_files(result)**
Copies files or directories that exist only in the source folder to the replica.

- **double_check_common_files(result)**
Ensures files and directories that exist in both source and replica are identical (compares file content and permissions).

- **check_item_access(item, flag)**
Checks if an item in the source and replica folders is accessible for reading.

- **equal_files(item)**
Compares two files (source and replica) by checking their size, permissions, and content hashes.

- **equal_hashes(item)**
Computes and compares MD5 hash values of source and replica files.

- **check_permissions_in_subdirs(source, replica)**
Recursively checks and syncs the permissions of directories and files in the source and replica.

- **get_folder_size(path)**
Recursively calculates the total size of files in a directory.

- **handle_file(item, cpy_flag)**
Handles the deletion or copying of files from source to replica based on the comparison result.

- **delete(replica_path, item)**
Deletes a file or directory in the replica folder.

- **copy(source_path, replica_path, item)**
Copies a file or directory from the source folder to the replica.


# class Parser
This class handles the parsing of command-line arguments for the folder synchronization process.

**Attributes:**

- source_path (Path): The absolute path to the source folder that needs to be synchronized.
- replica_path (Path): The absolute path to the replica folder where files will be synchronized.
- logfile_path (Path): The absolute path to the log file where synchronization events will be recorded.
- sync_interval (int): The time interval (in seconds) between synchronization checks.

**Methods:**

- **init(self)** 
Initializes the parser with default values for source_path, replica_path, logfile_path, and sync_interval.

- **parse_args(self)** 
Parses command-line arguments to retrieve source folder path, replica folder path, log file path, and synchronization interval. Validates the inputs and sets the respective attributes.

- **check_path_arg(self, path: str, flag: int)** 
-> Optional[Path] Checks if a provided path exists and validates its type (directory or file) based on the flag. Returns the absolute path if valid, otherwise returns None.

- **create_folders_files(self, path: str, flag: int)**
Creates a directory or a log file if it does not exist, depending on the flag. If an error occurs during creation, it prints an error message and exits the program.