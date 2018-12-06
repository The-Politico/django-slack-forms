from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from slackforms.models import Form


class FormHandler:
    """
    Handler for dialog submissions. Validates data based on the callback_id
    and returns errors. If no errors, it calls the form's webhook.
    """
    def handle(self, data):
        try:
            form = Form.objects.get(name=data.get("callback_id"))
        except ObjectDoesNotExist:
            return HttpResponse(
                "Form {} not found".format(data.get("callback_id")), status=404
            )

        processed = form.process(data.get("submission"))
        validation = form.validate(processed)

        if validation is True:
            meta = {
                "data_id": None
                if data.get("state") == ""
                else data.get("state"),
                "team": data.get("team"),
                "channel": data.get("channel"),
                "user": data.get("user"),
            }
            form.post_to_webhook(processed, meta=meta)
            return HttpResponse(status=200)
        else:
            errors = [validation]
            return JsonResponse({"errors": errors}, safe=False)
