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

logger = logging.getLogger(__file__)


class Instagram(object):

    def get_user_info(self, user_id):
        """Return information about FB User ID
            :param user_id User id of FB
        """

        try:
            url = 'https://i.instagram.com/api/v2/users/{}/info/'.format(
                user_id
            )
            response = requests.get(url)

        except Exception as error:
            logger.exception('Error connecting to Instagram Server')
            raise HTTPMethodError(
                'Error Connecting to Instagram Server %s', error)
        else:
            if response.ok:
                data = response.json()
                data.update({
                    'instagram': self._get_instagram_link(data)
                })

                return data
        return None

    def _get_instagram_link(self, data):
        insta_id = data['user']['username']
        return 'https://instagram.com/{}'.format(insta_id)
