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
import json
import logging
import random
from copy import deepcopy

import requests

from .exceptions import HTTPMethodError
from .settings import CLIENT_ID
from .settings import CLIENT_SECRET
from .utils import CONVERSATION_FIELDS
from .utils import DEFAULT_HEADERS
from .utils import generate_settings
from .utils import HTTP_CODES
from .utils import MESSAGE_FIELDS
from .utils import NOTIFIER_FIELDS
from .utils import USER_FIELDS

LOGGER = logging.getLogger(__file__)


class Relations(object):
    none = 0
    liked = 1
    matched = 4


class User:
    """ User class for making Happn API calls from """

    headers = DEFAULT_HEADERS

    def __init__(self, fbtoken=None):
        """Constructor for generating the Happn User object
            :param fbtoken Facebook user access token used to fetch the Happn OAuth token
        """
        self.fbtoken = fbtoken
        self.oauth, self.id = self.get_oauth()
        self.app_secret_proof = self.get_app_secret_proof()

        LOGGER.debug('Happn User Generated. ID: %s', self.id)

    def set_device_id(self, device_id):
        """ Set device id """

        self.device_id = device_id

    def set_position(self, latitude, longitude):
        """ Set the position of the user using Happn's API
            :param latitude Latitude to position the User
            :param longitude Longitude to position the User
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        url = 'https://api.happn.fr/api/users/{}/devices/{}'.format(
            self.id, self.device_id
        )

        payload = {
            'alt': 20 + random.uniform(-10, 10),
            'latitude': round(latitude, 10),
            'longitude': round(longitude, 10),
            'circle_size': 500
        }

        try:
            response = requests.put(
                url, headers=headers, data=payload)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            self.lat = latitude
            self.lon = longitude
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def delete_user(self):
        """Delete user"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        url = 'https://api.happn.fr/api/users/{}'.format(self.id)

        try:
            response = requests.delete(
                url, headers=headers)
        except Exception as e:
            raise HTTPMethodError('Error Deleting User: {}'.format(e))

        if response.status_code == 200:
            return response.json()
        else:

            LOGGER.warning(
                'Server denied request for delete user: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def update_activity(self):
        """ Updates User activity """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="' + self.oauth + '"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Happn-DID': self.device_id
        })

        payload = {
            'update_activity': 'true'
        }

        url = 'https://api.happn.fr/api/users/{}'.format(self.id)

        try:
            response = requests.put(url, headers=headers, data=payload)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            LOGGER.debug('Updated User activity')
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def create_device(self, payload=None):
        """Create new device"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        if payload is None:
            payload = generate_settings()

        url = 'https://api.happn.fr/api/users/{}/devices'.format(self.id)

        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(payload))
        except Exception as e:
            raise HTTPMethodError('Error Creating Device: {}'.format(e))

        if response.status_code == 200:
            self.device_id = response.json()['data']['id']
            return response.json()['data'], payload
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def set_device(self, payload=None):
        """Set device"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        if payload is None:
            payload = generate_settings()

        url = 'https://api.happn.fr/api/users/{}/devices/{}'.format(
            self.id, self.device_id
        )

        try:
            response = requests.put(
                url, headers=headers, data=json.dumps(payload))
        except Exception as e:
            raise HTTPMethodError('Error Setting Device: {}'.format(e))

        if response.status_code == 200:
            self.device_id = response.json()['data']['id']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_device(self):
        """Get device"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        url = 'https://api.happn.fr/api/users/{}/devices/{}'.format(
            self.id, self.device_id)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            raise HTTPMethodError('Error Getting Device: {}'.format(e))

        if response.status_code == 200:
            return response.json()['data']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_device_list(self):
        """List devices"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json'
        })

        url = 'https://api.happn.fr/api/users/{}/devices'.format(
            self.id)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            raise HTTPMethodError('Error Getting Devices: {}'.format(e))

        if response.status_code == 200:
            return response.json()['data']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def like_user(self, user_id):
        """ Like user
            :user_id id of the user to like
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="' + self.oauth + '"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Happn-DID': self.device_id
        })

        payload = {
            'id': user_id
        }

        url = 'https://api.happn.fr/api/users/{}/accepted/{}'.format(
            self.id, str(user_id)
        )

        try:
            response = requests.post(
                url, headers=headers, data=payload)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            LOGGER.debug('Liked User ' + str(user_id))
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def reject_user(self, user_id):
        """ Reject user
            :user_id id of the user to reject
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="' + self.oauth + '"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Happn-DID': self.device_id
        })

        payload = {
            'id': user_id
        }

        url = 'https://api.happn.fr/api/users/{}/rejected/{}'.format(
            self.id, str(user_id)
        )

        try:
            response = requests.post(
                url, headers=headers, data=payload)
        except Exception:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            LOGGER.debug('Reject User ' + str(user_id))
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def unreject_user(self, user_id):
        """ Unreject user
            :user_id id of the user to unreject
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="' + self.oauth + '"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/users/{}/rejected/{}'.format(
            self.id, str(user_id)
        )

        try:
            response = requests.delete(url, headers=headers)
        except Exception:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            LOGGER.debug('Unreject User ' + str(user_id))
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def reject_user_list(self, offset=0):
        """ Unreject user
            :user_id id of the user to unreject
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="' + self.oauth + '"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/users/{}/rejected/?offset={}'.format(
            self.id, offset
        )

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            return response.json()['data']
        else:
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_recommendations(self, limit=16, offset=0):
        """ Get recs from Happn server
            :param limit Number of reccomendations to recieve
            :param offset Offset index for reccomendation list
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json',
            'X-Happn-DID': self.device_id
        })

        query = {
            'types': '468',
            'limit': limit,
            'offset': offset,
            'fields': NOTIFIER_FIELDS
        }

        url = 'https://api.happn.fr/api/users/{}/notifications/' \
            '?query={}'.format(self.id, json.dumps(query))

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            data = json.loads(
                json.dumps(
                    response.json()['data'],
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))
            return data
        else:
            LOGGER.warning('Error:  %d', response.status_code)
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_new_happners(self, limit=16, offset=0):
        """ Get recs from Happn server
            :param limit Number of reccomendations to recieve
            :param offset Offset index for reccomendation list
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json',
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/suggested-users/' \
            '?limit={}&fields={}'.format(limit, USER_FIELDS)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')
        if response.status_code == 200:
            data = json.loads(
                json.dumps(
                    response.json()['data'],
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))
            return data
        else:
            LOGGER.warning('Error:  %d', response.status_code)
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_conversations(self, offset=0, limit=64):
        """ Get conversations with userID from Happn server
            :param userID User ID of target user.
            :param offset Offset of conversations to recieve
            :param limit Number of conversations to recieve
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/users/{}/conversations/' \
            '?fields={}&offset={}&limit={}'.format(
                self.id, CONVERSATION_FIELDS, offset, limit)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            data = json.loads(
                json.dumps(
                    response.json()['data'],
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))
            return data
        else:
            LOGGER.warning('Error: %d', response.status_code)
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_user_info(self, user_id):
        """ Get conversations with userID from Happn server
            :param userID User ID of target user.
            :param offset Offset of conversations to recieve
            :param limit Number of conversations to recieve
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/users/{}/?fields={}'.format(
            user_id, USER_FIELDS)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            data = json.loads(
                json.dumps(
                    response.json()['data'],
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))
            return data
        else:
            LOGGER.warning('Error: %s ', response.status_code)
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_my_info(self):
        """ Get conversations with userID from Happn server
            :param userID User ID of target user.
            :param offset Offset of conversations to recieve
            :param limit Number of conversations to recieve
        """

        headers = deepcopy(self.headers)
        headers.update({
            'Content-Type': 'application/json',
            'Authorization': 'OAuth="{}"'.format(self.oauth),
        })

        url = 'https://api.happn.fr/api/users/me/?fields={}'.format(
            USER_FIELDS)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')

        if response.status_code == 200:
            data = json.loads(
                json.dumps(
                    response.json()['data'],
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                ))
            return data
        else:
            LOGGER.warning('Error: %s ', response.status_code)
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def send_message(self, conversation_id, message):
        """Send new message"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json',
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/conversations/{}/messages'.format(
            conversation_id)

        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(message))
        except Exception as e:
            raise HTTPMethodError('Error Creating Device: {}'.format(e))

        if response.status_code == 200:
            return response.json()['data']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_messages(self, conversation_id):
        """Send new message"""

        headers = deepcopy(self.headers)
        headers.update({
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/json',
            'X-Happn-DID': self.device_id
        })

        url = 'https://api.happn.fr/api/conversations/{}/messages?fields={}'.format(
            conversation_id, MESSAGE_FIELDS)

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            raise HTTPMethodError('Error Creating Device: {}'.format(e))

        if response.status_code == 200:
            return response.json()['data']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_app_secret_proof(self):
        """Send new message"""

        headers = {
            'Authorization': 'OAuth="{}"'.format(self.oauth),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        payload = {
            'facebook_access_token': self.fbtoken
        }

        url = 'https://api.happn.fr/api/auth/proof'

        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            raise HTTPMethodError('Error Creating Device: {}'.format(e))

        if response.status_code == 200:
            return response.json()['data']['app_secret_proof']
        else:
            LOGGER.warning(
                'Server denied request for device set change: %d',
                response.status_code
            )
            raise HTTPMethodError(HTTP_CODES[response.status_code])

    def get_oauth(self):
        """Gets the OAuth tokens using Happn's API """

        headers = deepcopy(self.headers)
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '374'
        })

        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'assertion',
            'assertion_type': 'facebook_access_token',
            'assertion': self.fbtoken,
            'scope': 'mobile_app'
        }

        url = 'https://api.happn.fr/connect/oauth/token/'

        try:
            response = requests.post(
                url, headers=headers, data=payload)
        except Exception as e:
            LOGGER.exception('Error connecting to Facebook Server')
            raise HTTPMethodError('Error connecting to Facebook Server')
        else:
            data = response.json()
            status = response.status_code
            if response.ok:
                return data['access_token'], data['user_id']
            else:
                LOGGER.warning('Error: %d - %s', status, data)
                raise HTTPMethodError(data, status)
