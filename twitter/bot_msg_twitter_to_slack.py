import json
import requests
from utils import helper_func
from bot_const_and_resources import constants


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# get the existing rules
def get_rules(headers):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


# deleting the existing rules
def delete_all_rules(headers, rules):
    if rules is None or "data" not in rules:
        return None
    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # print(json.dumps(response.json()))
    return "rules deleted"


def set_rules(headers):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "from: {bot_screen_name}".format(bot_screen_name=constants.BOT_SCREEN_NAME)},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))


def get_stream(headers, client):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    if response.status_code == 200:
        print("streaming OK")
    else:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            client.chat_postMessage(channel='content', text="I just Tweeted:\n {tweet}"
                                    .format(tweet=json_response['data']['text']))


# step 1: get the BEARER_TOKEN from twitter.env
# step 2: create the relevant header
# step 3: start an HTTP (persistent) connection- on this connection, the tweets will be received
def start_streaming(client):
    resources = helper_func.get_from_resources('twitter', 'BEARER_TOKEN')
    headers = create_headers(resources[0])
    set_rules(headers)
    get_stream(headers, client)
