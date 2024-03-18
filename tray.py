import os
from pystray import Icon, Menu, MenuItem
from PIL import Image

import config
import utils


def close_client():
	os._exit(1)


def force_check():
	files_list = [f for f in os.listdir(config.path) if os.path.isfile(os.path.join(config.path, f))]
	for file in files_list:
		print(config.path + '\\' + file)
		utils.send_file_state(config.path + '\\' + file, config.username)


def force_clear():
	utils.data.clear()
	utils.send_user_data(config.username, utils.data)


def tray_create():
	image = Image.open('icon.png')

	icon = Icon(
		'NoMerge',
		icon=image,
		menu=Menu(
			MenuItem('Force Check', force_check),
			MenuItem('Force Clear', force_clear),
			MenuItem('Exit', close_client)
		)
	)

	icon.run()
	print('Tray icon created')
