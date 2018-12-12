from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class SlashHandler:
    """
    Handler for slash commands. Finds the right form from the name of the
    command being called in the request data and triggers it.
    """

    def handle(self, data):
        try:
            form = Form.objects.get(slash_command=data.get("command")[1:])
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("callback_id")), status=404
            )

        meta = {
            "data_id": data.get("text"),
            "team": {"id": data.get("team_id")},
            "channel": {"id": data.get("channel_id")},
            "user": {"id": data.get("user_id")},
        }

        method = "POST" if data.get("text") == "" else "PUT"

        form.trigger(
            data.get("trigger_id"),
            method=method,
            data_id=data.get("text"),
            meta=meta,
        )

        return HttpResponse(status=200)
