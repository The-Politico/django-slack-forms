import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models import Token
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
        # process the request data
        data = request.POST
        token = data.get("token", None)
        data_id = data.get("data_id", None)
        channel = data.get("channel", None)
        form = data.get("form", None)
        new = data.get("new", None)
        edit = data.get("edit", None)
        delete = data.get("delete", None)

        # authenticate the request
        token = data.get("token")
        if token is not None and token != settings.SLACK_VERIFICATION_TOKEN:
            if token not in [tok.token for tok in Token.objects.all()]:
                return HttpResponse("Invalid Verification Token.", status=403)

        # validate the request data
        # required fields
        for param in [("channel", channel), ("form", form)]:
            if param[1] is None:
                return HttpResponse(
                    'No "{}" provided.'.format(param[0]), status=400
                )

        # data_id is required if edit or delete buttons are being used
        if data_id is None:
            for param in [("edit", edit), ("delete", delete)]:
                if param[1] is not None:
                    return HttpResponse(
                        'No "data_id" provided with a "{}".'.format(param[0]),
                        status=400,
                    )

        # form is required if buttons are being used
        if form is None:
            for param in [("new", new), ("edit", edit), ("delete", delete)]:
                if param[1] is not None:
                    return HttpResponse(
                        'No "form" provided with a "{}".'.format(param[0]),
                        status=400,
                    )

        message = {}
        message["channel"] = channel
        message["text"] = request.POST.get("text", "")

        actions = []
        if new is not None:
            button_data = {"method": "POST", "form": form}
            button = {
                "name": "new",
                "text": new,
                "type": "button",
                "value": json.dumps(button_data),
            }
            actions.append(button)

        if edit is not None:
            button_data = {"method": "PUT", "data_id": data_id, "form": form}
            button = {
                "name": "edit",
                "text": edit,
                "type": "button",
                "value": json.dumps(button_data),
            }
            actions.append(button)

        if delete is not None:
            button_data = {
                "method": "DELETE",
                "data_id": data_id,
                "form": form,
            }
            button = {
                "name": "delete",
                "text": delete,
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
            actions.append(button)
        buttons_attatchment = {
            "fallback": "",
            "callback_id": form,
            "actions": actions,
        }
        message["attachments"] = json.loads(
            request.POST.get("attachments", "[]")
        ) + [buttons_attatchment]

        resp = slack("chat.postMessage", **message)
        return JsonResponse(resp, status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
