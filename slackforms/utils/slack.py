from slackclient import SlackClient
from slackforms.conf import settings


"""
Slack API methods commonly handled by bots rather than apps.
"""
BOT_METHODS = [
    "chat.postMessage",
    "chat.postEphemeral"
]


slack_api = SlackClient(settings.SLACK_API_TOKEN)
slack_bot = SlackClient(settings.SLACK_BOT_TOKEN)


def slack(method, *args, **kwargs):
    """
    Pass through to handle the different Slack tokens based on the API method
    being used.
    """
    if method in BOT_METHODS:
        return slack_bot.api_call(method, *args, **kwargs)
    else:
        return slack_api.api_call(method, *args, **kwargs)
