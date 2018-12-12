import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..conf import settings
from ..utils import slack


class Callback(View):
    """
    Endpoint that posts messages in Slack channels. Designed to provide
    in-channel feedback after a successful form process. Returns the response
    data received from Slack.
    """

    def get(self, request):
        return HttpResponse("OK", status=200)

    def post(self, request, format=None):
        data = request.POST

        if data.get("token") != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid Verification Token.", status=403)

        data_id = request.POST.get("data_id", None)
        channel = request.POST.get("channel", None)
        form = request.POST.get("form", None)

        for param in [data_id, channel, form]:
            if param is None:
                return HttpResponse(
                    'No "{}" provided.'.format(param), status=400
                )

        message = {}
        message["channel"] = channel
        message["text"] = request.POST.get("text", "")

        message["attachments"] = json.loads(request.POST.get("new", "[]"))
        new = request.POST.get("new", None)
        edit = request.POST.get("edit", None)
        delete = request.POST.get("delete", None)

        base_button_data = {"data_id": data_id, "form": form}
        if new is not None:
            button_data = {"method": "POST", **base_button_data}  # noqa
            button = {
                "name": "new",
                "text": new,
                "type": "button",
                "value": json.dumps(button_data),
            }
            message["attachments"].append(button)

        if edit is not None:
            button_data = {"method": "PUT", **base_button_data}  # noqa
            button = {
                "name": "edit",
                "text": edit,
                "type": "button",
                "value": json.dumps(button_data),
            }
            message["attachments"].append(button)

        if delete is not None:
            button_data = {"method": "DELETE", **base_button_data}  # noqa
            button = {
                "name": "delete",
                "text": edit,
                "type": "button",
                "value": json.dumps(button_data),
                "style": "danger",
                "confirm": {
                    "title": "Are you sure?",
                    "text": "Do you want to delete the {} {} {}?".format(
                        form, "with an ID of", data_id
                    ),
                    "ok_text": "Yes",
                    "dismiss_text": "No",
                },
            }
            message["attachments"].append(button)

        resp = slack("chat.postMessage", **message)
        return JsonResponse(resp, status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
