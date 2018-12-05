from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class SlashHandler:
    def handle(self, data):
        try:
            form = Form.objects.get(slash_command=data.get("command")[1:])
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("callback_id")), status=404
            )

        form.post_to_slack(data.get("trigger_id"), data_id=data.get("text"))

        return HttpResponse(status=200)
