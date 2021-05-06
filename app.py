import os

from instauto.api.client import ApiClient
from instauto.api.actions.structs.profile import Info
from instauto.api import structs as st
from instauto.api.actions import post as ps

#login credentials
login_username = 'znicou'
login_password = 'KLÖwer21!'
image = 'photos/Square.jpg'
text = 'Test upload'

# login
if __name__ == '__main__':
    if os.path.isfile('./.instauto.save'):
        client = ApiClient.initiate_from_file('./.instauto.save')
    else:
        client = ApiClient(user_name=os.environ.get("INSTAUTO_USER") or login_username, password=os.environ.get("INSTAUTO_PASS") or login_password)
        client.login()
        client.save_to_disk('./.instauto.save')


#post album working
    posts = [
        ps.PostFeed(
            path='photoo/Square.jpg',
            caption='normal',
        ),
        ps.PostFeed(
            path='photoo/Square2.jpg',
            caption='turned',
        )
    ]

    resp = client.post_carousel(posts, "Caption", 80)
    print("Success: ", resp['configure_sidecar'].ok)