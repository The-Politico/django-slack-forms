"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.SECRET_KEY = getattr(
    project_settings, "SLACKFORMS_SECRET_KEY", "a-bad-secret-key"
)

Settings.SLACK_VERIFICATION_TOKEN = getattr(
    project_settings, "SLACKFORMS_SLACK_VERIFICATION_TOKEN", ""
)

Settings.SLACK_BOT_TOKEN = getattr(
    project_settings, "SLACKFORMS_SLACK_BOT_TOKEN", ""
)

Settings.SLACK_API_TOKEN = getattr(
    project_settings, "SLACKFORMS_SLACK_API_TOKEN", ""
)

Settings.ROOT_URL = getattr(project_settings, "SLACKFORMS_ROOT_URL", "")

settings = Settings
