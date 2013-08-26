import json
import requests
import time
from utils import logger_factory

reddit_logger = logger_factory('reddit')

class RedditAPIClient(object):
    """
    A lot of this code is based on https://gist.github.com/Nikola-K/5375314
    """
    def __init__(self, username, password, hostname='http://www.reddit.com'):
        self.default_request_params = {
            'user': username,
            'passwd': password,
            'api_type': 'JSON',
        }
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Reddit Account Delete -- %s' % username}
        )
        self.hostname = hostname

    def _http_request(self, method, url, params):
        if method == 'GET':
            api_call = self.session.get(url, params=params)
        elif method == 'POST':
            api_call = self.session.post(url, data=params)
        elif method == 'PUT':
            api_call = self.session.put(url, params=params)
        else:
            api_call = self.session.delete(url, params=params)

        status_code = int(api_call.status_code)

        if status_code >= 400:
            reddit_logger.info(
                'The %s request for url: %s with params: %s '
                'failed with error code: %s'
                % (method, url, params, status_code))
            return (status_code,
                    'ERROR: Invalid HTTP method %s for url: %s with params: %s'
                    % (method, url, params))
        reddit_logger.info('%s call made to endpoint \'%s\''
                              ' with params %s successfully. status'
                              ' code returned: %s'
                              % (method, url, params, status_code))
        return (status_code, api_call.text)

    def api_request(self, method, url, params={}, update_params=True):
        url = self.hostname + url
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            reddit_logger.info('HTTP method %s not recognized' % method)
            return ('405', 'ERROR: HTTP method %s not recognized' % method)

        if update_params:
            payload = self.default_request_params
            payload.update(params)
        else:
            payload = params

        response = self._http_request(method, url, params=payload)
        time.sleep(2)
        return response

class RedditUser(object):

    def __init__(self, username, password):
        self.username = username
        self._comments = []
        self._posts = []
        self.api_client = RedditAPIClient(username, password)

    def login(self):
        login = self.api_client.api_request('POST', '/api/login')
        login = json.loads(login[1])
        if len(login['jquery']) == 17:
            #when the user login fails the length of the list of jquery
            #elements on the page is 17.
            return False
        else:
            user_data = self.api_client.api_request('GET', '/api/me.json')
            user_data = json.loads(user_data[1])
            self.user_id = user_data['data']['id']
            self.modhash = user_data['data']['modhash']
            return True

    def _get_content(self, content_type):
        more_content = True
        offset = None
        content = []
        destination_url = '/user/%s/%s.json' % (
            self.username, content_type
        )
        while more_content:
            params = {}
            if offset:
                params = {'after': offset}
            content_response = self.api_client.api_request(
                'GET', destination_url, params
            )
            content_response = json.loads(content_response[1])
            content_data = content_response['data']
            list_of_content = content_data['children']
            for content_object in list_of_content:
                content_id = content_object['data']['id']
                content.append(content_id)
            before = content_data['before']
            offset = content_data['after']
            if not offset:
                more_content = False
        if content_type == 'comments':
            self._comments = content
        else:
            self._posts = content

    def download_self(self):
        self._get_content('comments')
        self._get_content('submitted')

    def edit_comments(self):
        type_prefix = 't1_'
        for comment in [self._comments[0]]:
            fullname = type_prefix + comment
            text = 'The best BLTs are made in New Jersey'
            params = {
                'api_type': 'JSON',
                'text': text,
                'thing_id': fullname,
                'uh': self.modhash,
            }
            edit = self.api_client.api_request('POST', '/api/editusertext', params, update_params=False)
            print edit