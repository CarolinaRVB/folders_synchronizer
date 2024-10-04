import os
import sys
import signal
import logging
import threading
from parser import Parser
from synchronizer import Sync

def signal_handler(sig, frame):
	print("\n\033[91mWarning\033[0m: forced termination of synchronization (Ctrl+C).\nExiting program.")
	sys.exit(0)

def input_thread(stop_thread):
	while not stop_thread.is_set():
		stop_sign = input("Write '\033[92mstop\033[0m' to terminate synchronization: \n")
		if stop_sign.lower() == "stop":
			stop_thread.set()
			print("\033[92m*** Synchronization terminated ***\nStopping threads and exiting program...\033[0m")
		else:
			print("\033[91mInvalid input: only 'stop' is accepted.\033[0m")

def set_logging(logfile):
	log = logging.getLogger(os.path.basename(logfile))
	log.setLevel(logging.INFO)
	
	file_handler = logging.FileHandler(logfile)
	file_handler.setLevel(logging.INFO)
	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.INFO)

	formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
									datefmt='%d/%m/%Y %H:%M:%S')
	stdout_handler.setFormatter(formatter)
	file_handler.setFormatter(formatter)
	
	log.addHandler(stdout_handler)
	log.addHandler(file_handler)
	return log

def main():
	# Set folder paths from cmd-line arguments
	parser = Parser()
	parser.parse_args()
	source_path = parser.source_path
	replica_path = parser.replica_path
	logfile_path = parser.logfile_path
	sync_interval = parser.sync_interval

	# Handle user signals
	signal.signal(signal.SIGINT, signal_handler)

	# Create Thread event
	stop_thread = threading.Event()

	# Setup logget config
	log = set_logging(logfile_path)

	# Set infinite loop in separate thread until user requests to stop or sync fails
	input_thread_loop = threading.Thread(target=input_thread, args=(stop_thread,), daemon=True)
	input_thread_loop.start()

	# Set synchronization of folders over each self.interval
	sync = Sync(source=source_path, replica=replica_path, logfile=logfile_path, interval=sync_interval,
			 	first=True, stop_thread=stop_thread, logger=log)
	sync_thread = threading.Thread(target=sync.sync_thread, daemon=True)
	sync_thread.start()

	# Join thread
	sync_thread.join()


if __name__ == "__main__":
	main()
