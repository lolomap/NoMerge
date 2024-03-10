import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import sys
import pickle
import os

from nicegui import ui

hostname = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = sys.argv[2] if len(sys.argv) > 2 else 8085
db_path = 'db.pkl'

data = {}


@ui.refreshable
def ui_list() -> None:
	files = {}
	for _user, _files in list(data.items()):
		for _file in _files:
			if _file not in files.keys():
				files[_file] = [_user]
			else:
				files[_file].append(_user)

	with ui.list().props('bordered separator'):
		ui.item_label('Busy files (unsafe for simultaneous editing)').props('header').classes('text-bold')
		ui.separator()
		for file, users in list(files.items()):
			with ui.item():
				with ui.item_section():
					with ui.row():
						ui.item_label(file.split('\\')[-1])
						ui.item_label(file)
						for user in users:
							ui.item_label(user)


def save_data(user, files):
	data[user] = files
	with open(db_path, 'wb') as f:
		pickle.dump(data, f)


def load_data():
	global data
	if os.path.isfile(db_path):
		with open(db_path, 'rb') as f:
			data = pickle.load(f)


class WebServer(BaseHTTPRequestHandler):
	def do_POST(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()

			content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
			raw = self.rfile.read(content_length).decode('utf-8')
			post_data = json.loads(raw)
			# print(post_data)

			save_data(post_data['user'], post_data['files'])
			ui_list.refresh()

			print(data)

		except Exception as e:
			print(e)
			self.send_response(500)


def start_server():
	web_server = HTTPServer((hostname, port), WebServer)
	print('Server started...')
	try:
		web_server.serve_forever()
	except KeyboardInterrupt:
		pass

	web_server.server_close()
	print('Server stopped')


# EXECUTION #


load_data()

daemon = threading.Thread(
	name='daemon_server',
	target=start_server
)
daemon.daemon = True
daemon.start()


ui_list()
ui.run(reload=False)
