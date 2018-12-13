from django.urls import path
from .views import API, Options


urlpatterns = [
    path("test/", API.as_view(), name="slackforms-test-api"),
    path("options/", Options.as_view(), name="slackforms-test-options"),
]
