from django.http import HttpResponse
from django.views import View

from slackforms.utils import slack


class TestMessage(View):
    def get(self, request):
        channel = "CEK26NZM2"

        text = "A message to test forms..."

        attachments = [
            {
                "text": "Select a name.",
                "fallback": "Fallback",
                "callback_id": "Test",
                "actions": [
                    {"name": "new", "text": "New", "type": "button"},
                    {"name": "12345", "text": "Andrew Briz", "type": "button"},
                    {"name": "86422", "text": "Jon McClure", "type": "button"},
                    {
                        "name": "other_names",
                        "text": "Someone else...",
                        "type": "select",
                        "options": [
                            {"text": "Tyler Fisher", "value": "null"},
                            {"text": "Lily Mihalik", "value": "43113"},
                            {"text": "Beatrice Jin", "value": "64213"},
                        ],
                    },
                ],
            }
        ]

        slack(
            "chat.postMessage",
            channel=channel,
            text=text,
            attachments=attachments,
        )

        return HttpResponse("OK", status=200)
