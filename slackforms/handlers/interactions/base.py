from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class InteractionBase:
    """
    Base class for interactive message triggered endpoints. Finds the right
    form from the callback_id and triggers it. Different interactions have
    different locations for their arguments which is coded in child classes.
    """
    def get_argument_prop(self):
        return ""

    def handle(self, data):
        self.data = data

        try:
            self.form = Form.objects.get(name=data.get("callback_id"))
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("callback_id")), status=404
            )

        self.form.post_to_slack(
            data.get("trigger_id"), data_id=self.get_argument_prop()
        )

        return HttpResponse(status=200)
