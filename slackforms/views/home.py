import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View

from slackforms.conf import settings

from ..handlers import (
    FormHandler,
    ActionHandler,
    MessageHandler,
    SlashHandler,
    ManualHandler,
)

"""
Mapping reequest types to valid handler functions.
"""
HANDLERS = {
    "dialog_submission": FormHandler().handle,
    "interactive_message": MessageHandler().handle,
    "message_action": ActionHandler().handle,
    "slash_command": SlashHandler().handle,
    "manual": ManualHandler().handle,
}


class Home(View):
    """
    Endpoint to receive all interactions from Slack (i.e. slash commands,
    dialog submissions, interactive messages, message actions, and even manual
    requests sent from other servers).
    """
    def get(self, request):
        """
        Server status.
        """
        return HttpResponse("OK", status=200)

    def post(self, request, format=None):
        """
        Validate request token and pass data to the appropriate handler.
        """
        if "payload" in request.POST:
            data = json.loads(request.POST.get("payload"))
        else:
            data = request.POST

        if data.get("token") != settings.SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid Verification Token.", status=403)

        type = data.get("type", "")
        if type == "" and "command" in data:
            type = "slash_command"

        if type not in HANDLERS:
            return HttpResponse(
                "No handler for {} request".format(type), status=400
            )

        handler = HANDLERS.get(type)
        return handler(data)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
