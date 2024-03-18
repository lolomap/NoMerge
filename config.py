import configparser

path = ''
url = ''
track_files = ''
username = ''


def init():
	global path, url, track_files

	config = configparser.ConfigParser()
	config.read('.config', encoding='utf-8')
	path = config['DEFAULT']['Path']
	url = config['DEFAULT']['Url']
	track_files = config['DEFAULT']['TrackFiles']