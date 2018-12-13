from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form
from slackforms.utils import slack


class SlashHandler:
    """
    Handler for slash commands. Finds the right form from the name of the
    command being called in the request data and triggers it.
    """

    def handle(self, data):
        try:
            form = Form.objects.get(slash_command=data.get("command")[1:])
        except ObjectDoesNotExist:
            slack(
                "chat.postEphemeral",
                user=data.get("user_id", ""),
                channel=data.get("channel_id", ""),
                text="Form not found for command: `{}`.".format(
                    data.get("command")
                ),
            )
            return HttpResponse(
                "Form {} not found".format(data.get("command")), status=404
            )

        meta = {
            "data_id": data.get("text"),
            "team": {"id": data.get("team_id")},
            "channel": {"id": data.get("channel_id")},
            "user": {"id": data.get("user_id")},
        }

        text = data.get("text")
        method = "POST" if text == "" else "PUT"

        form.trigger(
            data.get("trigger_id"), method=method, data_id=text, meta=meta
        )

        return HttpResponse(status=200)
