import utils
import sys
import json
from reddit import (
	RedditAPIClient,
	RedditUser,
)

AUTH_ERROR_MESSAGE = """Your account could not be authenticated. Please ensure
that your provided credentials are correct/ It's also possible that Reddit's API
is being a complete bitch. Try again in a few minutes"""

if __name__ == '__main__':
	auth_info = utils.get_auth_info()
	username, password = auth_info['username'], auth_info['password']
	reddit_user = RedditUser(username, password)
	print 'Connecting to Reddit...'
	if reddit_user.login():
		print 'Downloading comments and self posts'
		download = reddit_user.download_self()
		if download[0] == download[1] == 0:
			print 'No comments or posts found on that account'
			sys.exit()
		print 'Downloaded %d submitted posts' % download[0]
		print 'Downloaded %d submitted comments' % download[1]
		print 'Editing comments and self posts'
		reddit_user.edit_content()
		print 'Deleting comments and self posts'
		reddit_user.delete_content()
		print 'Deleting self'
		reddit_user.delete_self()
		print 'Done!'
	else:
		print AUTH_ERROR_MESSAGE
