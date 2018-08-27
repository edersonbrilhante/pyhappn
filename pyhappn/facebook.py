"""
   Copyright 2018 Ederson Bilhante

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging

import requests

from .exceptions import HTTPMethodError
from .utils import FB_USER_FIELDS

LOGGER = logging.getLogger(__file__)


class Facebook(object):

    url = 'https://graph.facebook.com/v2.12/'

    def __init__(self, access_token, app_secret_proof):
        self.access_token = access_token
        self.app_secret_proof = app_secret_proof

    def get_user_info(self, user_id):
        """Return information about FB User ID
            :param user_id User id of FB
        """

        uri = '{}/?fields={}&access_token={}&appsecret_proof={}'.format(
            user_id, FB_USER_FIELDS, self.access_token, self.app_secret_proof)

        try:
            response = requests.get(self.url + uri)
        except Exception:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')
        else:
            status = response.status_code
            data = response.json()
            if response.ok:
                data.update({
                    'facebook': self._get_facebook_link(data)
                })

                return data
            else:
                LOGGER.warning('Error: %d - %s', status, data)
                raise HTTPMethodError(data, status)

    def _get_facebook_link(self, data):
        fb_id = data.get('picture').get('data').get('cache_key').split(':')[0]
        res = {
            'account': 'https://facebook.com/{}'.format(fb_id),
        }
        if data.get('albums'):
            albums = [{'album': 'https://facebook.com/{}'.format(album['id'])}
                      for album in data.get('albums').get('data')]
            res['albums'] = albums
        return res
