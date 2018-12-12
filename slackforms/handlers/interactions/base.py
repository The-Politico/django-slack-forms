from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class InteractionBase:
    """
    Base class for interactive message triggered endpoints. Finds the right
    form from the callback_id and triggers it. Different interactions have
    different locations for their arguments which is coded in child classes.
    """

    def get_id(self):
        return ""

    def get_method(self):
        if self.get_id() == "":
            return "POST"
        else:
            return "PUT"

    def handle(self, data):
        self.data = data

        try:
            self.form = Form.objects.get(name=data.get("callback_id"))
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("callback_id")), status=404
            )

        meta = {
            "data_id": self.get_id(),
            "team": data.get("team"),
            "channel": data.get("channel"),
            "user": data.get("user"),
        }

        self.form.trigger(
            data.get("trigger_id"),
            method=self.get_method(),
            data_id=self.get_id(),
            meta=meta,
        )

        return HttpResponse(status=200)
