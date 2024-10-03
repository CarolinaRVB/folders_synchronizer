import os
import sys
import time
import shutil
import filecmp
import logging
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
			if not self.synchronize():
				self.stop_thread.set()
				break 
			time.sleep(self.interval)

	def synchronize(self):
		if Path(self.source).exists() and Path(self.replica).exists():
			result = filecmp.dircmp(self.source, self.replica)
			self.update_folder_and_log(result)
		else:
			print("\033[91mError\033[0m: source folder not found\nExiting synchronization.")
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
				self.logger.warning(f"Item '{item}' requires manual synchronization [check permissions, file corruption or symbolic links].")
			else:
				self.logger.info(f"Item '{item}' was created in replica folder.")
				self.handle_file(item, True)

	def double_check_common_files(self, result):
		for item in result.common:
			if item in result.common_funny:
				self.logger.warning(f"Item '{item}' requires manual synchronization [check permissions, file corruption or symbolic links].")
				self.handle_file(item, False)
			else:
				source_path = self.source / item
				if source_path.is_file():
					if not self.equal_hashes(item):
						self.handle_file(item, True)
				elif source_path.is_dir():
					source_size = self.get_folder_size(source_path)
					replica_size = self.get_folder_size(self.replica / item)
					if source_size != replica_size:
						self.handle_file(item, True)

	def equal_hashes(self, item):
		check = list()
		source_file = self.source / item
		replica_file = self.replica / item
		for file_name in [source_file, replica_file]:
			with open(file_name, 'rb') as file:
				hash = md5(file.read()).hexdigest()
				check.append(hash)
		return check[0] == check[1]

	def get_folder_size(self, path):
		total_size = 0
		for dir_path, dir_names, file_names in os.walk(path):
			for file_name in file_names:
				file_path = os.path.join(dir_path, file_name)
				total_size += os.path.getsize(file_path)

	def handle_file(self, item, cpy_flag):
		path = self.replica / item
		if path.exists() and path.is_file() or path.is_symlink():
			path.unlink()
			self.logger.info(f"File '{item}' was deleted from replica folder.")
		elif path.exists() and path.is_dir():
			shutil.rmtree(path)
			self.logger.info(f"Folder '{item}' was deleted from replica folder.")
		if cpy_flag:
			source_path = self.source / item
			if source_path.is_file():
				shutil.copy2(source_path, self.replica, follow_symlinks=True)
				self.logger.info(f"File '{item}' was copied.")
			elif source_path.is_dir():
				shutil.copytree(source_path, self.replica / item, dirs_exist_ok=True)
				self.logger.info(f"Folder '{item}' was copied.")
