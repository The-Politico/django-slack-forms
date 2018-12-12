import json
import requests
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from ..models import Test

from django.conf import settings

CHANNEL = "general"


class API(View):
    def get(self, request):
        # process the request data
        id = request.GET.get("id", None)

        # handle the API logic
        try:
            t = Test.objects.get(pk=id)
            t_data = model_to_dict(t)
            return JsonResponse(t_data)
        except Test.DoesNotExist:
            return HttpResponse("Test not found.", status=404)

    def put(self, request):
        # process the request data
        request_data = QueryDict(request.body)
        meta = json.loads(request_data.get("slackform_meta_data"))
        response_url = meta["response_url"]
        data_id = meta["data_id"]
        username = meta["user"]["name"]
        form_name = meta["form"]
        token = meta["token"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Test.objects.get(pk=data_id)
        if "age" in request_data:
            t.age = request_data["age"]

        if "date" in request_data:
            t.date = request_data["date"].split("T")[0]

        if "name" in request_data:
            t.name = request_data["name"]

        if "title" in request_data:
            t.title = request_data["title"]

        if "permissions" in request_data:
            t.permissions = request_data["permissions"]
        t.save()

        # create feedback message
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "channel": CHANNEL,
            "form": form_name,
            "text": "`{}` edited `{}` entry: {}(`{}`)".format(
                username, form_name, t.name, t.pk
            ),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    def post(self, request):
        # process the request data
        request_data = request.POST
        meta_data = request_data.get("slackform_meta_data")
        meta = json.loads(meta_data)
        response_url = meta["response_url"]
        username = meta["user"]["name"]
        form_name = meta["form"]
        token = meta["token"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Test()
        if "age" in request_data:
            t.age = request_data["age"]

        if "date" in request_data:
            t.date = request_data["date"].split("T")[0]

        if "name" in request_data:
            t.name = request_data["name"]

        if "title" in request_data:
            t.title = request_data["title"]

        if "permissions" in request_data:
            t.permissions = request_data["permissions"]
        t.save()

        # create feedback message
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "channel": CHANNEL,
            "data_id": t.pk,
            "form": form_name,
            "text": "`{}` created a new `{}` entry: {}(`{}`).".format(
                username, form_name, t.name, t.pk
            ),
            "new": "New",
            "delete": "Delete",
            "edit": "Edit",
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    def delete(self, request):
        # process the request data
        request_data = QueryDict(request.body)
        meta_data = request_data.get("slackform_meta_data")
        meta = json.loads(meta_data)
        data_id = meta["data_id"]
        response_url = meta["response_url"]
        username = meta["user"]["name"]
        form_name = meta["form"]
        token = meta["token"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Test.objects.get(pk=data_id)
        name = t.name
        t.delete()

        # create feedback message
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "channel": CHANNEL,
            "form": form_name,
            "text": "`{}` deleted `{}` entry: {}(`{}`)".format(
                username, form_name, name, data_id
            ),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
