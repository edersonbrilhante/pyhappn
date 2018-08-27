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

from pyhappn.happn import Relations
from pyhappn.happn import User
from pyhappn.settings import TOKEN


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
            for rec in recs:
                relation = int(rec.get('notifier').get('my_relation'))
                if relation == Relations.none:
                    user_inst.like_user(rec['notifier']['id'])
                    print('Like {}'.format(rec['notifier']['id']))

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


if __name__ == '__main__':
    fire.Fire(HappnCli)
