import logging

from argparse import ArgumentParser
from getpass import getpass

def get_auth_info():
	parser = ArgumentParser(description='Bulk edit all your Reddit comments'
										'nonsense and delete your account')
	parser.add_argument('-u', '--username', required=True)
	parser.add_argument('-c', '--content-delete', action='store_true', default=False)
	parser.add_argument('-s', '--self-delete', action='store_true', default=False)
	auth_info = vars(parser.parse_args())
	password = getpass()
	auth_info['password'] = password
	return auth_info

def logger_factory(name, filename='default'):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	if filename == 'default':
		filename = name + '.log'
	file_handler = logging.FileHandler(filename)
	format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
	file_handler.setFormatter(format)
	logger.addHandler(file_handler)
	return logger