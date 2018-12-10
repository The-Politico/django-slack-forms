# Installation

1. Install the app.

  ```
  $ pip install django-slack-forms
  ```

2. Add the app to your Django project and configure settings.

  ```python
  # yourapp/settings.py

  INSTALLED_APPS = [
      # ...
      'slackforms',
  ]

  #########################
  # slackforms settings

  SLACKFORMS_SLACK_VERIFICATION_TOKEN = ""  # See Setting Up Your Slack App
  SLACKFORMS_SLACK_API_TOKEN = ""  # See Setting Up Your Slack App
  SLACKFORMS_SLACK_BOT_TOKEN = "" # See Setting Up Your Slack App
  SLACKFORMS_ROOT_URL = ""  # Root URL of where this app will be installed
  ```
