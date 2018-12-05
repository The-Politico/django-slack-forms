from django.urls import path

from .views import Home, Callback

urlpatterns = [
    path("", Home.as_view(), name="slackforms-home"),
    path("callback/", Callback.as_view(), name="slackforms-callback"),
]
