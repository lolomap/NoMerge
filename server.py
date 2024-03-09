import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

from nicegui import ui

hostname = 'localhost'
port = 8085
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
		ui.item_label('Уже редактирующиеся файлы (опасно для мерджа)').props('header').classes('text-bold')
		ui.separator()
		for file, users in list(files.items()):
			with ui.item():
				with ui.item_section():
					with ui.row():
						ui.item_label(file.split('\\')[-1])
						ui.item_label(file)
						for user in users:
							ui.item_label(user)


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

			data[post_data['user']] = post_data['files']
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


daemon = threading.Thread(
	name='daemon_server',
	target=start_server
)
daemon.daemon = True
daemon.start()


ui_list()
ui.run(reload=False)
