from django.urls import path

from .views import Home, Callback, Message

urlpatterns = [
    path("", Home.as_view(), name="slackforms-home"),
    path("callback/", Callback.as_view(), name="slackforms-callback"),
    path("message/", Callback.as_view(), name="slackforms-message"),
]
