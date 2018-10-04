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
import fire
import names

from pyhappn.exceptions import HTTPMethodError
from pyhappn.happn import Relations
from pyhappn.happn import User
from pyhappn.happn_email import HappnEmail
from pyhappn.mail import Mail
from pyhappn.settings import EMAIL
from pyhappn.settings import PASSWORD
from pyhappn.settings import TOKEN
from pyhappn.utils import generate_gmail


class HappnCli(object):
    """Cli Happn."""

    def like_all(self):
        """Like all"""

        user_inst = User(TOKEN)
        device_list = user_inst.get_device_list()
        user_inst.set_device_id(device_list[0]['id'])
        limit = 100

        for i in range(int(9800 / limit)):
            recs = user_inst.get_recommendations(limit, (i * limit))
            if recs:
                for rec in recs:
                    relation = int(rec.get('notifier').get('my_relation'))
                    if relation == Relations.none:
                        user_inst.like_user(rec['notifier']['id'])
                        print('Like {}'.format(rec['notifier']['id']))
            else:
                break

    def like_all_new_happners(self):
        """Like all new happners"""

        user_inst = User(TOKEN)
        device_list = user_inst.get_device_list()
        user_inst.set_device_id(device_list[0]['id'])
        limit = 100

        for i in range(int(9800 / limit)):
            recs = user_inst.get_new_happners(limit)
            if recs:
                for rec in recs:
                    user_inst.like_user(rec['id'])
                    print('Like {}'.format(rec['id']))
            else:
                break

    def hidden_all(self):
        """Hidden all"""

        user_inst = User(TOKEN)
        device_list = user_inst.get_device_list()
        user_inst.set_device_id(device_list[0]['id'])

        while True:
            recs = user_inst.get_recommendations(100)
            if not recs:
                break
            for rec in recs:
                relation = int(rec.get('notifier').get('my_relation'))
                if (relation != Relations.none):
                    user_inst.reject_user(rec['notifier']['id'])
                    print('Hidden {}'.format(rec['notifier']['id']))

    def send_message_all_new(self, message):
        """Send message for all new crush"""

        user_inst = User(TOKEN)
        device_list = user_inst.get_device_list()
        user_inst.set_device_id(device_list[0]['id'])
        limit = 20
        idx = 0

        while True:
            offset = idx * limit
            idx += 1
            recs = user_inst.get_conversations(offset, limit)
            if not recs:
                break
            for rec in recs:
                if not rec.get('messages'):
                    msg = {'message': message}
                    user_inst.send_message(rec['id'], msg)

    def send_message_all(self, message):
        """Send message for all"""

        user_inst = User(TOKEN)
        device_list = user_inst.get_device_list()
        user_inst.set_device_id(device_list[0]['id'])
        limit = 20
        idx = 70

        messages_sent = {}

        while True:
            offset = idx * limit
            idx += 1
            recs = user_inst.get_conversations(offset, limit)
            if not recs:
                break
            for rec in recs:
                if not messages_sent.get(rec['id']):
                    msg = {'message': message}
                    user_inst.send_message(rec['id'], msg)
                    messages_sent.update({rec['id']: 1})

    def create_account(self, number):
        """Create new account"""

        user_inst = User(TOKEN)
        gen_email = generate_gmail(EMAIL)
        first_name = names.get_first_name(gender='male')
        try:
            count = len(open('email.txt').readlines())
        except OSError:
            count = 0
        for _ in range(0, count):
            next(gen_email)
        for _ in range(number):
            email = next(gen_email)
            try:
                user_inst.create_account(
                    first_name, 'MALE', '1980-02-02', email, False, True)
            except HTTPMethodError as err:
                print('Temporary block in cloudflare')
                break
            else:
                mail = Mail()
                url = None
                while not url:
                    url = mail.get_url_confirm(email)
                happn_email = HappnEmail()
                csrfmiddlewaretoken, token, cookies = happn_email.get_confirmation_page(
                    url)
                happn_email.confirmation_account(
                    url, cookies, csrfmiddlewaretoken, token, PASSWORD)
                with open('email.txt', 'a') as myfile:
                    myfile.write(email + '\n')


if __name__ == '__main__':
    fire.Fire(HappnCli)
