from django.contrib import admin
from django.urls import include, path
from .views import TestManual


urlpatterns = [
    path("admin/", admin.site.urls),
    path("test-manual/", TestManual.as_view(), name="slackforms-test-manual"),
    path("", include("slackforms.urls")),
    path("api/", include("testapi.urls")),
]
