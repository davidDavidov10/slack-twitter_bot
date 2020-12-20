from dotenv import load_dotenv
from pathlib import Path
import os
from bot_const_and_resources import commands
from datetime import datetime, timezone, timedelta


# this function created in order to initiate slack.py and twitter APIs environment variables
# The resources KEYS are returned in the order they were requested
def get_from_resources(resource, *args):
    resource_to_return = []
    env_path = Path('./config') / "{resource}.env".format(resource=resource)
    load_dotenv(dotenv_path=env_path)
    for required_res in args:
        resource_to_return.append(os.environ[required_res])
    return resource_to_return


def get_current_time(add_seconds):
    time = datetime.now(timezone.utc) + timedelta(seconds=add_seconds)
    return time.astimezone().strftime('%H:%M:%S')


def get_commands_description():
    commands_description = ""
    for command, description in commands.supported_commands.items():
        commands_description += command + ": " + description + "\n"
    return commands_description
