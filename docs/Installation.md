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

3. Set up the root URL for the app.

  ```python
  # yourapp/urls.py
  urlpatterns += [path(
      "", # The URL path to django-slack-forms from the root of your app
      include("slackforms.urls")
  )]
  ```

The root of this app is important to understand as it will be used in a setting and in the setup for your Slack app. For clarity, let's take a look at an example.

Your Django app is hosted on `http://example.com` and you want your `django-slack-forms` root to be located at `http://example.com/slack-forms/`.

To do that set the URL path in your `urls.py` to `slack-forms/`. Then set your `SLACKFORMS_ROOT_URL` in your `settings.py` to `http://example.com/slack-forms/`.

Finally, go back to your Slack App Dashboard and set all the `Request URL`s to `http://example.com/slack-forms/` too.

Next up: [create a form in your Django admin.](docs/Creating-Forms.md)
