import platform
import sys
import os
import time
import logging
import re
import subprocess
import requests
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileSystemEvent


path = sys.argv[1] if len(sys.argv) > 1 else '.\\test'
url = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:8085'
track_files = sys.argv[3] if len(sys.argv) > 3 else '.*.txt'

username = platform.node()
data = set()


class FileChangesEventHandler(FileSystemEventHandler):
	def on_modified(self, event: FileSystemEvent) -> None:
		if re.match(track_files, event.src_path):

			# If changes make file to up-to-day, remove it from user editings
			_gitrun = subprocess.run(['git', 'status', path, '-s'], stdout=subprocess.PIPE)
			_output = _gitrun.stdout.decode(encoding='utf-8')
			if event.src_path.split('\\')[-1] not in _output:
				if event.src_path in data:
					data.remove(event.src_path)
					logging.info(data)
					try:
						requests.post(url, json={'user': username, 'files': list(data)})
					except Exception as e:
						print(e)
				return

			# Otherwise inform that file is unsafe to merge
			data.add(event.src_path)
			logging.info(data)
			try:
				requests.post(url, json={'user': username, 'files': list(data)})
			except Exception as e:
				print(e)


if __name__ == "__main__":

	if not os.path.isdir(path):
		print(f'Path {path} is not a dir')
		exit()

	gitrun = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
	username = gitrun.stdout.decode(encoding='utf-8')[:-1]

	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)

	logging.info(f'start watching directory {path!r}')
	event_handler = FileChangesEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)

	observer.start()
	try:
		while True:
			time.sleep(1)
	finally:
		observer.stop()
		observer.join()
