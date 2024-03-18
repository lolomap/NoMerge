import platform
import sys
import os
import threading
import time
import logging
import re
import subprocess
import requests
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileSystemEvent

import config
import utils
import tray


config.username = platform.node()


class FileChangesEventHandler(FileSystemEventHandler):
	def on_any_event(self, event: FileSystemEvent) -> None:
		if re.match(config.track_files, event.src_path):
			utils.send_file_state(event.src_path, config.username)


if __name__ == "__main__":
	config.init()

	if not os.path.isdir(config.path):
		print(f'Path {config.path} is not a dir')
		# For Windows service to see if app was started
		subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
		sys.exit(1)

	gitrun = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE, shell=True)
	config.username = gitrun.stdout.decode(encoding='utf-8')[:-1]

	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)

	daemon = threading.Thread(
		name='daemon_tray_icon',
		target=tray.tray_create
	)
	daemon.daemon = True
	daemon.start()

	logging.info(f'start watching directory {config.path!r}')
	event_handler = FileChangesEventHandler()
	observer = Observer()
	observer.schedule(event_handler, config.path, recursive=True)

	observer.start()
	try:
		while True:
			time.sleep(1)
	finally:
		observer.stop()
		observer.join()
