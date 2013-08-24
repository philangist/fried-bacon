import requests
import json
from utils import logger_factory

reddit_logger = logger_factory('reddit')

class RedditAPIClient(object):
    """
    A lot of this code is based on https://gist.github.com/Nikola-K/5375314
    """
    def __init__(self, user_name, password, hostname='http://www.reddit.com'):
        self.default_request_params = {
            'user': user_name,
            'passwd': password,
            'api_type': 'JSON',
        }
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Reddit Account Delete -- %s' % user_name}
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

        status_code = str(api_call.status_code)

        if status_code[0] in ['4', '5']:
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

    def api_request(self, method, url, params={}):
        url = self.hostname + url
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            reddit_logger.info('HTTP method %s not recognized' % method)
            return ('405', 'ERROR: HTTP method %s not recognized' % method)

        if len(params.keys()) == 0:
            params = self.default_request_params

        response = self._http_request(method, url, params)
        return response