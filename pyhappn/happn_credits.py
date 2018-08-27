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
import time
from random import choice

from splinter import Browser

from .email import tempmailaddress


LOGGER = logging.getLogger(__file__)


class HappnCredits(object):

    def __init__(self, name, lastname, password, sponsorship):
        self.name = name
        self.lastname = lastname
        self.password = password
        self.sponsorship = sponsorship
        self.email = None
        with Browser('chrome') as fb:
            self.fb_browser = fb
            self.get_new_email()
            self.fb()
            self.confirm_email_fb()
            self.happn()
        self.fb_browser.quit()

    def fb(self):
        LOGGER.info('Starting Facebook')

        url = 'https://www.facebook.com'

        LOGGER.info('Visiting https://www.facebook.com')
        self.fb_browser.visit(url)
        time.sleep(5)

        field = self.fb_browser.find_by_name('firstname')
        if field:
            LOGGER.info('Filling Name')
            field.fill(self.name)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('lastname')
        if field:
            LOGGER.info('Filling lastname')
            field.fill(self.lastname)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('reg_email__')
        if field:
            LOGGER.info('Filling email')
            field.type(self.email)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('reg_email_confirmation__')
        if field:
            LOGGER.info('Filling confirm email')
            field.type(self.email)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('reg_passwd__')
        if field:
            LOGGER.info('Filling password')
            field.fill(self.password)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('birthday_day')
        if field:
            LOGGER.info('Set Bday')
            day = choice(range(1, 20))
            self.fb_browser.select('birthday_day', day)
            time.sleep(1)
        else:
            raise Exception('Error')

        field = self.fb_browser.find_by_name('sex')
        if field:
            LOGGER.info('Set Sex')
            self.fb_browser.choose('sex', '1')
            time.sleep(1)
        else:
            raise Exception('Error')

        button = self.fb_browser.find_by_name('websubmit')
        if button:
            LOGGER.info('Send command')
            button.first.click()
            time.sleep(10)
        else:
            raise Exception('Error')

    def happn(self):

        LOGGER.info('Starting happn')
        url = 'https://www.happn.com/invite/{}'.format(self.sponsorship)

        LOGGER.info('Visiting www.happn.com/invite')
        self.fb_browser.visit(url)
        time.sleep(1)

        LOGGER.info('Accepting cookie')
        self.fb_browser.find_by_css('#cookie-button')[0].click()

        LOGGER.info('Registering')
        self.fb_browser.find_by_css('.button-register')[0].click()
        time.sleep(5)

        happn_window = self.fb_browser.windows.current
        self.fb_browser.windows.current = self.fb_browser.windows.current.next

        time.sleep(2)
        LOGGER.info('Confirming')
        self.fb_browser.find_by_name('__CONFIRM__')[0].click()

        self.fb_browser.windows.current = happn_window
        time.sleep(2)

        self.fb_browser.find_by_css('.submit')[0].click()
        LOGGER.info('Downloading happn')

        LOGGER.info('Finishing happn')
        time.sleep(10)

    def get_new_email(self):
        tempmailaddress.get_new_email(self)

    def confirm_email_fb(self):
        tempmailaddress.confirm_email_fb(self)
