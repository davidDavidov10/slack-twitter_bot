# slack-twitter_bot
in order to run this program you should follow this steps:
1. clone the project to your computer
2. run pip install -r requirements.txt
3. now basically  you have two options:
  3.1 host this bot in your local server
  3.2 host this bot in a non local server

in either case, you should get a URL to your server, if you are on your local computer you can use "ngrok",
navigate to api.slack.com go to slash commands and then define 3 slash commands (that currently supported) /now, /functionality, /new-content
for each of those in the "Request URL" field you should enter your server URL followed by "/" and the name of the command for example"
http://server_url.com/now

4. create a channel named "content" and add this slack bot
5. you are ready to go! run the program.

