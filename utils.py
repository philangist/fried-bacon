from argparse import ArgumentParser
from getpass import getpass

def get_auth_info():
	parser = ArgumentParser(description='Bulk edit all your Reddit comments'
										'nonsense and delete your account')
	parser.add_argument('-u', '--username', required=True)
	password = getpass()
	auth_info = vars(parser.parse_args())
	auth_info['password'] = password
	return auth_info
