import os
from pystray import Icon, Menu, MenuItem
from PIL import Image


def close_client():
	os._exit(1)


def tray_create():
	image = Image.open('icon.png')

	icon = Icon(
		'NoMerge',
		icon=image,
		menu=Menu(
			MenuItem('Exit', close_client)
		)
	)

	icon.run()
	print('Tray icon created')
