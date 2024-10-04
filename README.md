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
