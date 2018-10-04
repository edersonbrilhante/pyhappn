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
from requests_html import HTMLSession

from .exceptions import HTTPMethodError

LOGGER = logging.getLogger(__file__)


class HappnEmail:

    def get_confirmation_page(self, url):

        session = HTMLSession()
        try:
            response = session.get(url)
        except Exception:
            LOGGER.exception('Error connecting to Happn\'s Server')
            raise HTTPMethodError('Error connecting to Happn\'s Server')
        else:
            csrfmiddlewaretoken = response.html.find('form input')[
                0].attrs['value']
            token = response.html.find('form input')[3].attrs['value']
            return csrfmiddlewaretoken, token, response.cookies.get_dict()

    def confirmation_account(self, url, cookies, csrfmiddlewaretoken, token, password):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-length': '639',
            'referer': url
        }

        payload = {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'password': password,
            'password_confirmation': password,
            'token': token
        }

        url = 'https://www.happn.com/create-account-confirmation'

        try:
            requests.post(url, headers=headers, data=payload, cookies=cookies)
        except Exception:
            LOGGER.exception('Error connecting to Happn\'s Server')
            raise HTTPMethodError('Error connecting to Happn\'s Server')
