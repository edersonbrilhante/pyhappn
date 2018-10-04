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
import string
from random import choice
from uuid import uuid4

HTTP_CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status',
    208: 'Already Reported',
    226: 'IM Used',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Payload Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: 'I\'m a teapot',
    421: 'Misdirected Request',
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    444: 'Connection Closed Without Response',
    451: 'Unavailable For Legal Reasons',
    499: 'Client Closed Request',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates',
    507: 'Insufficient Storage',
    508: 'Loop Detected',
    510: 'Not Extended',
    511: 'Network Authentication Required',
    599: 'Network Connect Timeout Error',
}

DEFAULT_HEADERS = {
    'User-Agent': 'Happn/19.1.0 AndroidSDK/19',
    'http.useragent': 'Happn/19.1.0 AndroidSDK/19',
    'Host': 'api.happn.fr',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def generate_settings():
    settings = {
        'app_build': choice(APP_BUILD_LIST),
        'country_id': 'BR',
        'language_id': 'pt',
        'gps_adid': str(uuid4()),
        'idfa': uuid4().hex,
        'os_version': '19',
        'gps_token': generate_gps_token(),
        'type': 'android',
    }

    return settings


def generate_gps_token():
    num_string = [14, 3, 7, 16]
    complete_string_list = []
    for num in num_string:
        string_val = ''.join(choice(string.printable) for i in range(num))
        complete_string_list.append(string_val)
    complete_string = '_'.join(complete_string_list)
    return complete_string


def generate_gmail(email):
    if len(email) <= 1:
        yield email
    else:
        head, tail = email[0], email[1:]
        for item in generate_gmail(tail):
            yield head + item
            yield head + '.' + item


APP_BUILD_LIST = [
    '21.2.0',
    '20.48.0',
    '20.46.1',
    '20.45.0'
]  # TODO: make dynamic way


NOTIFIER_FIELDS = (
    'id,modification_date,notification_type,nb_times,'
    'notifier.fields(id,type,job,fb_id,is_accepted,workplace,my_relation,'
    'social_synchronization.fields(instagram.fields(username),facebook),'
    'distance,gender,is_charmed,nb_photos,first_name,age,already_charmed,'
    'has_charmed_me,availability,is_invited,last_invite_received,'
    'profiles.mode(1).width(360).height(640).fields(id,mode,url,width,height))'
)

CONVERSATION_FIELDS = (
    'creation_date,participants.fields(user.fields'
    '(social_synchronization.fields(instagram,facebook),fb_id,'
    'picture.fields(id,url,is_default).height(120).mode(0).width(120),age,'
    'clickable_message_link,id,first_name,is_moderator)),modification_date,'
    'id,messages.fields(sender.fields(id,first_name),creation_date,message,'
    'id).offset(0).limit(3),is_read'
)

USER_FIELDS = (
    'credits,referal,matching_preferences,about,achievements,'
    'availability,clickable_message_link,stats,subscription,'
    'unread_notifications,unread_conversations,renewable_credits,'
    'last_tos_version_accepted,birth_date,last_position_update,'
    'last_meet_position,id,modification_date,job,is_accepted,workplace,'
    'matching_preferences,register_date,segments,fb_id,social_synchronization.'
    'fields(instagram),job,my_relation,distance,gender,modification_date,'
    'is_charmed,nb_photos,first_name,age,already_charmed,has_charmed_me,'
    'availability,is_invited,school,last_invite_received,profiles.mode(1)'
    '.width(92).height(92).fields(id,mode,url,width,height)'
)


FB_USER_FIELDS = (
    'family,albums,work,devices,friends,photos,likes,accounts,'
    'gender,first_name,favorite_teams,birthday,age_range,name,cover,'
    'address,about,picture.width(80).fields(url,cache_key).height(80),'
    'context.fields(mutual_likes.fields(summary.fields(total_count),name,'
    'picture.width(80).fields(url).height(80)),all_mutual_friends.'
    'fields(summary.fields(total_count),picture.width(80).'
    'fields(url,cache_key).height(80),name))'
)

MESSAGE_FIELDS = (
    'sender.fields(id,first_name),creation_date,message,id'
)
