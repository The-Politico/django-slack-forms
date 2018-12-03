from django.apps import AppConfig


class SlackformsConfig(AppConfig):
    name = 'slackforms'

    def ready(self):
        from slackforms import signals  # noqa
