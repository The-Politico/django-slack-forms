import json
import requests
import random
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

FIELDS = ["name", "age", "title", "date", "permissions"]
DATABASE = {}  # Fake external database
CHANNEL = "CEMH4MAEN"


class API(View):
    def get(self, request):
        resp = DATABASE.get(request.GET.get("id", ""), {})
        return JsonResponse(resp)

    def put(self, request):
        # process the request data
        request_data = QueryDict(request.body)
        meta = json.loads(request_data.get("slackform_meta_data"))
        response_url = meta["response_url"]
        data_id = meta["data_id"]
        username = meta["user"]["name"]
        form_name = meta["form_name"]

        # handle the API logic
        if data_id in DATABASE:
            for field in FIELDS:
                if field in request_data:
                    DATABASE[data_id][field] = request_data[field]

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` edited `{}` entry: `{}`.".format(
            username, form_name, data_id
        )
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    def post(self, request):
        # process the request data
        meta = json.loads(request.POST.get("slackform_meta_data"))
        response_url = meta["response_url"]
        username = meta["user"]["name"]
        form_name = meta["form_name"]

        # handle the API logic
        data_id = "%032x" % random.getrandbits(128)
        DATABASE[data_id] = {}
        for field in FIELDS:
            DATABASE[data_id][field] = request.POST.get(field, "")

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` created a new `{}` entry: {}.".format(
            username, form_name, data_id
        )
        message["attachments"] = [
            {
                "fallback": "Edit N/A",
                "callback_id": form_name,
                "actions": [
                    {"name": data_id, "text": "Edit", "type": "button"}
                ],
            }
        ]
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
