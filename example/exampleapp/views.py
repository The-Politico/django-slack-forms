import requests
import json
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from slackforms.conf import settings


class TestManual(View):
    def get(self, request):
        return HttpResponse("OK", status=200)

    def post(self, request):
        data = request.POST

        if data.get("token") != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid Verification Token.", status=403)

        payload = {
            "type": "manual",
            "form": "Test",
            "token": "4c001abee28a4bc18581abfb210f05",
            "trigger_id": data.get("trigger_id"),
            "method": "PUT",
            # "data_id": "17",
            "data": {"name": "Andrew Briz Override"},
        }

        requests.post(
            url=settings.ROOT_URL, data={"payload": json.dumps(payload)}
        )
        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
