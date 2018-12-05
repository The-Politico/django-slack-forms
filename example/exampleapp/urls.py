from django.contrib import admin
from django.urls import include, path
from .views import API, TestMessage, TestManual, TestOptions


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", API.as_view(), name="slackforms-test-api"),
    path(
        "api/options/", TestOptions.as_view(), name="slackforms-test-options"
    ),
    path(
        "test-message/", TestMessage.as_view(), name="slackforms-test-message"
    ),
    path("test-manual/", TestManual.as_view(), name="slackforms-test-manual"),
    path("", include("slackforms.urls")),
]
