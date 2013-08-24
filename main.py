import utils
import json
import time
from api_client import RedditAPIClient

if __name__ == '__main__':
	auth_info = utils.get_auth_info()
	username, password = auth_info['username'], auth_info['password']
	reddit_api_client = RedditAPIClient(username, password)
	login = reddit_api_client.api_request('POST', '/api/login')
	time.sleep(2)
	print login
	me = reddit_api_client.api_request('GET', '/api/me.json')
	time.sleep(2)
	print me