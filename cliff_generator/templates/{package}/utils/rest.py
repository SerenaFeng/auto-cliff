import httplib
import json
import os

import requests


class RestManager(object):
    headers = {}

    def __init__(self, cli_options=None):
        self.cli_options = cli_options
        self.session = requests.Session()

    def get(self, url):
        return self._parse_response('Get',
                                    self._request('get', url,
                                                  headers=self.headers))

    def post(self, url, data):
        if 'results' in url or 'deployresults' in url:
            self.headers['X-Auth-Token'] = os.environ.get('testapi_token')
        return self._parse_response('Create',
                                    self._request('post', url,
                                                  data=json.dumps(data),
                                                  headers=self.headers))

    def put(self, url, data):
        return self._parse_response('Update',
                                    self._request('put', url,
                                                  data=json.dumps(data),
                                                  headers=self.headers))

    def delete(self, url, *args):
        data = json.dumps(args[0]) if len(args) > 0 else None
        return self._parse_response('Delete',
                                    self._request('delete', url,
                                                  data=data,
                                                  headers=self.headers))

    def _request(self, method, *args, **kwargs):
        return getattr(self.session, method)(*args, **kwargs)

    def _raise_failure(self, op, response):
        raise Exception('{} failed: {}'.format(op, response.reason))

    def _parse_response(self, op, response):
        if response.status_code == httplib.OK:
            if op != 'Delete' and response.text != '':
                return response.json()
            else:
                return None
        else:
            self._raise_failure(op, response)
