from bot_const_and_resources.interesting_sources\
    import interesting_twitter_sources as sources
import requests
import datetime
from utils import helper_func
from bot_const_and_resources import constants


# this is the header that needed to be sent with the API request
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_urls_to_check_new_content():
    urls = {}
    tweet_time = (datetime.datetime.now() - datetime.timedelta(hours=3 * constants.NEW_TWEETS_FROM)).isoformat() + "Z"
    for source, screen_name in sources.items():
        url = "https://api.twitter.com/2/tweets/search/recent?query=from:{}&tweet.fields=author_id,created_at,text" \
              "&start_time={}".format(screen_name, tweet_time)
        urls[source] = url
    return urls


def connect_to_endpoint(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def check_new_content():
    resources = helper_func.get_from_resources('twitter', 'BEARER_TOKEN')
    bearer_token = resources[0]
    urls = create_urls_to_check_new_content()
    headers = create_headers(bearer_token)
    res = []
    for source, url in urls.items():
        res.append(source + ':')
        json_response = connect_to_endpoint(url, headers)
        if 'data' in json_response:
            for data in json_response['data']:
                date = datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
                res.append(str(date))
                res.append(data["text"])
                res.append("\n")
        else:
            res.append("no Tweets from last hour.")
    return "\n".join(res)
