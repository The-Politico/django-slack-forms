from django.http import JsonResponse
from django.views import View


class Options(View):
    def get(self, request):
        data = [
            {"label": "News Apps Editor", "value": "apps-editor"},
            {
                "label": "Senior News Apps Developer",
                "value": "apps-dev-senior",
            },
            {"label": "News Apps Developer", "value": "apps-dev"},
            {"label": "Graphics Editor", "value": "graphics-editor"},
            {"label": "Graphics Reporter", "value": "graphics-reporter"},
        ]
        return JsonResponse(data, safe=False)
