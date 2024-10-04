import os
import time
import shutil
import filecmp
from hashlib import md5
from pathlib import Path

class Sync():
	def __init__(self, source, replica, logfile, interval, first, stop_thread, logger) -> None:
		self.source = source
		self.replica = replica
		self.logfile = logfile
		self.interval = interval
		self.first = first
		self.stop_thread = stop_thread
		self.logger = logger
		
	def sync_thread(self):
		self.logger.warning("*** New synchronization process ***")
		while not self.stop_thread.is_set():
			try:
				if not self.synchronize():
					self.stop_thread.set()
			except Exception as err:
				self.logger.error(f"Synchronization error: '{err}'")
				self.stop_thread.set()

			time.sleep(self.interval)

	def synchronize(self):
		if self.source.exists() and self.replica.exists() and self.logfile.exists():
			result = filecmp.dircmp(self.source, self.replica)
			self.update_folder_and_log(result)
		else:
			self.logger.error("Issue with logger or folders found.\nExiting synchronization.")
			return False
		return True

	def update_folder_and_log(self, result):
		self.delete_extra_replica_files(result)
		self.copy_new_files(result)
		self.double_check_common_files(result)

	def delete_extra_replica_files(self, result):
		for item in result.right_only:
			self.handle_file(item, False)

	def copy_new_files(self, result):
		for item in result.left_only:
			if item in result.common_funny:
				if self.check_item_access(item):
					self.handle_file(item, True)
			else:
				self.logger.info(f"Item '{item}' was created in replica folder.")
				self.handle_file(item, True)

	# def double_check_common_files(self, result):
	# 	for item in result.common:
	# 		if item in result.common_funny:
	# 			print("here in common")
	# 			if self.check_item_access(item):
	# 				self.handle_file(item, True)
	# 			else:
	# 				self.handle_file(item, False)
	# 		else:
	# 			source_path = self.source / item
	# 			if source_path.is_file():
	# 				if not self.equal_files(item):
	# 					self.handle_file(item, True)
	# 			elif source_path.is_dir():
	# 				source_size = self.get_folder_size(source_path)
	# 				replica_size = self.get_folder_size(self.replica / item)
	# 				if source_size != replica_size:
	# 					self.handle_file(item, True)
 
	def double_check_common_files(self, result):
		for item in result.common:
			if self.check_item_access(item):
				source_path = self.source / item
				if source_path.is_file():
					if not self.equal_files(item):
						self.handle_file(item, True)
				elif source_path.is_dir():
					source_size = self.get_folder_size(source_path)
					replica_size = self.get_folder_size(self.replica / item)
					if source_size != replica_size:
						self.handle_file(item, True)
			else:
				self.handle_file(item, False)

	def check_item_access(self, item):
		source_path = self.source / item
		replica_path = self.replica / item
		if not os.access(source_path, os.R_OK):
			self.logger.error(f"Item '{item}' cannot be read. Manual Synchronization required.")
			return False
		if not os.access(replica_path, os.R_OK):
			return False
		return True

	def equal_files(self, item):
		source_file = self.source / item
		replica_file = self.replica / item
		if os.stat(source_file).st_mode != os.stat(replica_file).st_mode:
			self.logger.warning(f"Permissions differ for {source_file} and {replica_file}.")
			return False
		if source_file.stat().st_size != replica_file.stat().st_size: 
			return False
		return self.equal_hashes(item)

	def equal_hashes(self, item):
		source_file = self.source / item
		replica_file = self.replica / item
		with open(source_file, 'rb') as file:
			source_hash = md5(file.read()).hexdigest()
		with open(replica_file, 'rb') as file:
			replica_hash = md5(file.read()).hexdigest()
		return source_hash == replica_hash

	def get_folder_size(self, path):
		total_size = 0
		with os.scandir(path) as item:
			for entry in item:
				if entry.is_file(follow_symlinks=False):
					total_size += entry.stat().st_size
				elif entry.is_dir(follow_symlinks=False):
					total_size += self.get_folder_size(entry.path)
		return total_size

	def handle_file(self, item, cpy_flag):
		replica_path = self.replica / item
		try:
			if replica_path.exists():
				if replica_path.is_file() or replica_path.is_symlink():
					replica_path.unlink()
					self.logger.info(f"File '{item}' was deleted from replica folder.")
				elif replica_path.is_dir():
					shutil.rmtree(replica_path)
					self.logger.info(f"Folder '{item}' was deleted from replica folder.")
			
			if cpy_flag:
				source_path = self.source / item
				if source_path.exists():
					if source_path.is_file():
						shutil.copy2(source_path, self.replica, follow_symlinks=False)
						self.logger.info(f"File '{item}' was copied.")
					elif source_path.is_dir():
						shutil.copytree(source_path, self.replica / item, dirs_exist_ok=False)
						self.logger.info(f"Folder '{item}' was copied.")
		except (IOError, OSError) as err:
			self.logger.error(f"Error handling '{item}': {str(err)}")
