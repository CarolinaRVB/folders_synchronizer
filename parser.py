import sys
import argparse
from pathlib import Path

# Checks and validates folders
# Works for different OS's
class Parser():
	def __init__(self) -> None:
		self.source_path = None
		self.replica_path = None
		self.logfile_path = None
		self.sync_interval = None

	def parse_args(self):
		# parse args
		parser = argparse.ArgumentParser(description = "Synchronization of Folders")
		
		# Set only 4 possible args
		parser.add_argument('--source_path', type=str, help="Source Folder Path")
		parser.add_argument('--replica_path', type=str, help="Replica Folder Path")
		parser.add_argument('--logfile_path', type=str, help="Log File Path")
		parser.add_argument('--sync_interval', type=int, help="Synchronization Interval")

		# Parse args to check if valid
		args = parser.parse_args()

		# No args provided, set default folders and return
		# if args.source_path is None and args.replica_path is None:
		# 	self.source_path = Path("source").resolve()
		# 	if not self.source_path.exists():
		# 		self.create_folders("source")
		# 	self.replica_path = Path("replica").resolve()
		# 	if not self.replica_path.exists():
		# 		self.create_folders("replica")
		# 	return 

		# Check if both Folders exits
		self.source_path = self.check_path_arg(args.source_path, 0)
		self.replica_path = self.check_path_arg(args.replica_path, 0)
		self.logfile_path = self.check_path_arg(args.logfile_path, 1)
		self.sync_interval = args.sync_interval
		# If not valid return error message and exit program
		if not self.source_path or not self.replica_path or not self.logfile_path or not self.sync_interval:
			print("\033[91mError\033[0m: Missing or invalid arguments.\nRUN: '\033[92mpython3 main.py --source_path [sourcePath] --replica_path [replicaPath] --logfile_path [log] --sync_interval [interval in seconds]\033[0m'")
			sys.exit(1)

	# def create_folders(self, path):
	# 	try:
	# 		os.makedirs(path, exist_ok=True)
	# 	except Exception as e:
	# 		print(f"Error creating directory {path}: {e}")
	# 		sys.exit(1)

	def check_path_arg(self, path, flag):
		if path:
			#convert path to absolute path
			abs_path = Path(path).resolve()
			if not abs_path.exists():
				print(f"Error: The path '{abs_path}' does not exist.")
				return None
			#Check if it's a directory
			if flag == 0:
				if not abs_path.is_dir():
					print(f"Error: The path '{abs_path}' is not a directory.")
					return None
			else:
				if not abs_path.is_file():
					print(f"Error: The path '{abs_path}' is not a file.")
			return abs_path
		return None
