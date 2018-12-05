from slackclient import SlackClient
from slackforms.conf import settings


slack_api = SlackClient(settings.SLACK_API_TOKEN)
slack_bot = SlackClient(settings.SLACK_BOT_TOKEN)


def slack(method, *args, **kwargs):
    if method == "chat.postMessage" or method == "chat.postEphemeral":
        return slack_bot.api_call(method, *args, **kwargs)
    else:
        return slack_api.api_call(method, *args, **kwargs)
