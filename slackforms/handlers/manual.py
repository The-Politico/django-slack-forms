from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class ManualHandler:
    """
    Handler for manual form triggers. Finds the right form from the form
    property in the request data and triggers the appropriate form using the
    trigger_id in the request data.
    """
    def handle(self, data):
        try:
            form = Form.objects.get(name=data.get("form"))
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("form")), status=404
            )

        kwargs = {}
        if "data" in data:
            kwargs["data"] = data.get("data")
        if "data_id" in data:
            kwargs["data_id"] = data.get("data_id")

        form.post_to_slack(data.get("trigger_id"), **kwargs)

        return HttpResponse("OK", status=200)
