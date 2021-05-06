from instagram_private_api import Client, ClientCompatPatch, MediaTypes
from PIL import Image

try:
    # python 2.x
    from urllib2 import urlopen
    import urllib2 as compat_urllib_request
except ImportError:
    # python 3.x
    from urllib.request import urlopen
    import urllib.request as compat_urllib_request
try:
    from urllib.parse import urlparse as compat_urllib_parse_urlparse
except ImportError:  # Python 2
    from urlparse import urlparse as compat_urllib_parse_urlparse

import json
import codecs
import datetime
import os.path
import logging
import argparse
import base64

###########################################
# Login
###########################################

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='login callback and save settings demo')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))

    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                args.username, args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                args.username, args.password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username, args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    # Call the api
    results = api.user_feed('2958144170')
    assert len(results.get('items', [])) > 0

    print('Login worked - All ok')
    
    ###########################################

    info = api.user_info(47082668829)

    #print(info)
    print("Hello")

    # im = Image.open("./photos/Komprimiert.jpg")
    # width, height = im.size
    # photo_size = (width, height)
    # print(photo_size)
    
    # with open("./photos/Komprimiert.jpg", "rb") as imageFile:
    #     photo_data = base64.b64encode(imageFile.read())

    # photo_caption = "Test Upload"

    # api.post_photo(photo_data, size=(1200, 1600), caption=photo_caption, upload_id=None, to_reel=False)


    # sample_url = 'https://c1.staticflickr.com/5/4103/5059663679_85a7ec3f63_b.jpg'
    # res = Image.open("./photos/Komprimiert.jpg")

    # with open("./photos/Komprimiert.jpg", "rb") as imageFile:
    #      enc = base64.b64encode(imageFile.read())

    # photo_data = enc

    # size = (1024, 683)
    # caption = 'Feathers'
    # results = api.post_photo(photo_data, size=size, caption=caption)
    # print(results)

class upload:
    @staticmethod
    def test_post_photo():
            sample_url = 'https://c1.staticflickr.com/5/4103/5059663679_85a7ec3f63_b.jpg'
            res = urlopen(sample_url)
            photo_data = res.read()
            size = (1024, 683)
            caption = 'Feathers'
            api.post_photo(photo_data, size=size, caption=caption)

upload.test_post_photo()