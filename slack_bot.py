from slackeventsapi import SlackEventAdapter
from flask import Flask, Response
from slack.errors import SlackApiError
from twitter import bot_msg_twitter_to_slack, twitter_new_content
from bot_const_and_resources import constants
import threading
import slack
from utils import helper_func
import time

# connect to slack, and falsk initialization
resources = helper_func.get_from_resources('slack', 'SLACK_TOKEN', 'SIGNING_SECRET')
app = Flask(__name__)
client = slack.WebClient(resources[0])
slack_event_adapter = SlackEventAdapter(resources[1], '/slack/events', app)
bot_command_description = helper_func.get_commands_description()


def send_scheduled_message():
    msg_to_send = "{current_time}: {msg}".format(current_time=helper_func.get_current_time(0), msg=constants.BOT_MSG)
    client.chat_postMessage(channel='content', text=msg_to_send)
    while True:
        msg = "{current_time}: {msg}".format(current_time=helper_func.get_current_time(constants.BOT_MSG_TIME),
                                             msg=constants.BOT_MSG)
        client.chat_scheduleMessage(channel='content', text=msg, post_at=time.time() + constants.BOT_MSG_TIME)
        time.sleep(constants.BOT_MSG_TIME)


def pull_msgs_and_send():
    try:
        client.chat_postMessage(channel='content', text=twitter_new_content.check_new_content())
    except SlackApiError as e:
        print("an error occur in pull_tweets: " + e)
        return Response(), 500


@app.route('/now', methods=["POST"])
def send_message_and_time():
    try:
        msg_to_send = "{current_time}: {msg}".format(current_time=helper_func.get_current_time(0), msg=constants.BOT_MSG)
        client.chat_postMessage(channel='content', text=msg_to_send)
        return Response(), 200
    except SlackApiError as e:
        print("an error occur in send_message_and_time: " + e)
        return Response(), 500


@app.route('/functionality', methods=["POST"])
def show_bot_functionality():
    try:
        msg_to_send = "{BOT_FUNCTIONALITY_MSG} {commands}".format(BOT_FUNCTIONALITY_MSG=constants.BOT_FUNCTIONALITY_MSG,
                                                                  commands=bot_command_description)
        client.chat_postMessage(channel='content', text=msg_to_send)

        return Response(), 200
    except SlackApiError as e:
        print("an error occur in show_bot_functionality: " + e)
        return Response(), 500


# all commands have to return status to slack within 3 sec otherwise slack show: timeout event.
# when /new-content executed, tweet_pull_thread will pull the new content and sent it through slack created.
@app.route('/new-content', methods=["POST"])
def pull_tweets():
    tweet_pull_thread = threading.Thread(target=pull_msgs_and_send)
    tweet_pull_thread.start()
    return Response(), 200


scheduler = threading.Thread(target=send_scheduled_message)
new_tweet_notifier = threading.Thread(target=bot_msg_twitter_to_slack.start_streaming, args=(client,))

if __name__ == "__main__":
    scheduler.start()
    new_tweet_notifier.start()
    app.run()
