"""Instagram views"""

# Django
from django.http import HttpResponse
from instagram.models import Instagram
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
# Utilities
import json
import requests


@csrf_exempt
def scrap_profile(request):
    
    """Get json representation ig user data"""
    if request.method == 'POST':
        json_data = json.loads(request.body)
    
    user_list = json_data['users']
    id_inserted_list = list()
    id_not_inserted_list = list()
    status = "OK"
    for user in user_list:

        url = f"https://www.instagram.com/{user}/?__a=1"

        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "+
            "(KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
        }

        response = requests.get(url,headers=headers)
        response = response.json()
        data = {}
        graphql = response['graphql']['user']

        data['ig_id'] = graphql['id']
        data['name'] = graphql['full_name']
        data['following'] = graphql['edge_follow']['count']
        data['followers'] = graphql['edge_followed_by']['count']
        posts = graphql['edge_owner_to_timeline_media']['edges']

        posts_data = []
        
        for post in posts:        

            posts_data.append(_get_post_data(post))
        data['post_data'] = posts_data

        try:
            new_profile = Instagram.objects.create(**data)
            id_inserted_list.append(new_profile.ig_id)

        except IntegrityError as e:
            status = e
            
    response = {
        'status': str(status),
        'instagram_id_inserted': id_inserted_list
    }
    
    return HttpResponse(json.dumps(response),content_type='application/json')


def _download_file(url, name=None):
        """Download video if exists save it in a file then returns path"""
        downloaded_video = []
        path="./"
        
        if name:
            filename = name
        else:
            filename = url.split('/')[-1]

        r = requests.get(url, stream=True)
        
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)

        path+=filename
        return path


def _get_post_data(post):
    """Return post data"""
    post_data = {}
    post = post['node']
    post_type = post['__typename'].lower()
    post_data['id'] = post['id']
    post_data['date'] = post['taken_at_timestamp']
    post_data['texto'] = post['edge_media_to_caption']['edges'][0]['node']['text']
    post_data['media'] = _download_file(post['display_url'],post_data['id']+'.jpg') if 'image' in post_type else _download_file(post['video_url'],post_data['id']+'.mp4')
    post_data['likes'] = post['edge_liked_by']['count']
    post_data['comments'] = post['edge_media_to_comment']['count']

    return post_data