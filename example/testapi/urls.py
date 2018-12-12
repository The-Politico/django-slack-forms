from django.urls import path
from .views import API, TestOptions


urlpatterns = [
    path("test/", API.as_view(), name="slackforms-test-api"),
    path("options/", TestOptions.as_view(), name="slackforms-test-options"),
]
