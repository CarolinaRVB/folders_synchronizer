import os
import sys
import argparse
from pathlib import Path

MIN_INTERVAL = 1
MAX_INTERVAL = 10

class Parser():
	def __init__(self) -> None:
		self.source_path = None
		self.replica_path = None
		self.logfile_path = None
		self.sync_interval = None

	def parse_args(self):
		parser = argparse.ArgumentParser(description = "Synchronization of Folders")

		parser.add_argument('--source_path', type=str, help="Source Folder Path")
		parser.add_argument('--replica_path', type=str, help="Replica Folder Path")
		parser.add_argument('--logfile_path', type=str, help="Log File Path")
		parser.add_argument('--sync_interval', type=int, help="Synchronization Interval")

		args = parser.parse_args()

		# # Uncomment the following section to run code without arguments  
		# if args.source_path is None or args.replica_path is None or \
		# args.lofile_path is None or args.sync_interval is None:
		# 	self.source_path = Path("source").resolve()
		# 	if not self.source_path.exists():
		# 		self.create_folders_files("source", 0)
		# 	self.replica_path = Path("replica").resolve()
		# 	if not self.replica_path.exists():
		# 		self.create_folders_files("replica", 0)
		# 	self.logfile_path = Path("logger").resolve()
		# 	if not self.logfile_path.exists():
		# 		self.create_folders_files("logger", 1)
		# 	if not self.sync_interval:
		# 		self.sync_interval = 5
		# 	return 

		self.source_path = self.check_path_arg(args.source_path, 0)
		self.replica_path = self.check_path_arg(args.replica_path, 0)
		self.logfile_path = self.check_path_arg(args.logfile_path, 1)
		if not MIN_INTERVAL <= args.sync_interval <= MAX_INTERVAL:
			print("\033[91mError\033[0m: Please choose a synchronization interval between 1 and 10 seconds (included).")
			sys.exit(1)
		self.sync_interval = args.sync_interval
  
		if not self.source_path or not self.replica_path or not self.logfile_path or not self.sync_interval:
			print("\033[91mError\033[0m: run: '\033[92mpython3 main.py --source_path [sourcePath] --replica_path [replicaPath] --logfile_path [loggerPath] --sync_interval [intervalInSeconds]\033[0m'")
			sys.exit(1)

	def check_path_arg(self, path, flag):
		if path:
			abs_path = Path(path).resolve()
			if not abs_path.exists():
				print(f"Error: The path '{abs_path}' does not exist.")
				return None
			if flag == 0:
				if not abs_path.is_dir():
					print(f"Error: The path '{abs_path}' is not a directory.")
					return None
			else:
				if not abs_path.is_file():
					print(f"Error: The path '{abs_path}' is not a file.")
			return abs_path
		return None

	# def create_folders_files(self, path, flag):
	# 	if not flag:
	# 		try:
	# 			os.makedirs(path, exist_ok=True)
	# 		except Exception as err:
	# 			print(f"Error creating directory {path}: {err}")
	# 			sys.exit(1)
	# 	else:
	# 		try:
	# 			self.logfile_path.touch()
	# 		except Exception as err:
	# 			print(f"Error creating file {path}: {err}")
	# 			sys.exit(1)
