import platform
import sys
import time
import logging
import re
import subprocess
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileSystemEvent

path = './test'
username = platform.node()
data = {}


class FileChangesEventHandler(FileSystemEventHandler):
	def on_modified(self, event: FileSystemEvent) -> None:
		if re.match('.*.txt', event.src_path):
			# If changes make file to up-to-day, remove it from user editings
			_gitrun = subprocess.run(['git', 'status', path], stdout=subprocess.PIPE)
			_output = _gitrun.stdout.decode(encoding='utf8')
			if event.src_path.split('\\')[-1] not in _output:
				if username in data.keys() and event.src_path in data[username]:
					data[username].remove(event.src_path)
				return

			if username not in data.keys():
				data[username] = [event.src_path]
			elif event.src_path not in data[username]:
				data[username].append(event.src_path)
			logging.info(data)


if __name__ == "__main__":
	gitrun = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
	username = gitrun.stdout.decode(encoding='utf8')

	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S'
	)

	path = sys.argv[1] if len(sys.argv) > 1 else path
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
