from base64 import urlsafe_b64decode

from gmail_api_wrapper.crud.modify import GmailAPIModifyWrapper
from gmail_api_wrapper.crud.read import GmailAPIReadWrapper


class Mail(object):

    def __init__(self):
        self.gapi_rd = GmailAPIReadWrapper()
        self.gapi_md = GmailAPIModifyWrapper()

    def get_url_confirm(self, email):
        messages = self.gapi_rd.get_unread_messages()
        for message in messages:
            msg_id = messages[0].get('id')
            message = self.gapi_rd.get_message(msg_id)
            fb_msg = 'Welcome to happn!'
            if fb_msg in message['snippet'] and \
                    message['payload']['headers'][0]['value'] == email:
                data = message['payload']['parts'][0]['body']['data']
                msg = urlsafe_b64decode(data).decode('utf-8')
                link = msg.split('[')[1].split(']')[0]
                self.gapi_md.mark_as_read(msg_id)
                return link
        else:
            return None
