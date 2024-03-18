import subprocess
import requests
import logging

import config

data = set()


def is_uptodate(file_name: str, path: str) -> bool:
	_gitrun = subprocess.run(['git', 'status', path, '-s'], stdout=subprocess.PIPE, shell=True)
	_output = _gitrun.stdout.decode(encoding='utf-8')
	return file_name not in _output


def send_file_state(src_path: str, username: str) -> None:
	# If changes make file to up-to-day, remove it from user editings
	if is_uptodate(src_path.split('\\')[-1], config.path):
		if src_path in data:
			data.remove(src_path)
			logging.info(data)
			try:
				requests.post(config.url, json={'user': username, 'files': list(data)})
			except Exception as e:
				print(e)
		return

	# Otherwise inform that file is unsafe to merge
	data.add(src_path)
	logging.info(data)
	try:
		requests.post(config.url, json={'user': username, 'files': list(data)})
	except Exception as e:
		print(e)


def send_user_data(username: str, user_data: set) -> None:
	try:
		requests.post(config.url, json={'user': username, 'files': list(data)})
	except Exception as e:
		print(e)
