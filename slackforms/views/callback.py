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

        message_data = json.loads(data.get("payload", ""))
        resp = slack("chat.postMessage", **message_data)
        return JsonResponse(resp, status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
