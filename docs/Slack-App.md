# Setting Up Your Slack App

In order to get `django-slack-forms` working, you'll need to have a custom app installed in your Slack workspace.

1. Go to the [Slack App Dashboard](https://api.slack.com/apps) and make a new App.

2. Under `Interactive Components`, paste the `SLACKFORMS_ROOT_URL` from your settings in `Request URL`.

3. Under `Bot Users`, click `Add a Bot User`. Give it a name and username.

4. Create a new slash command by going to `Slash Commands`. Give the command a name and set the `Request URL` to the location of the root of `django-slack-forms` in your Django app (if you're not sure about the URL, you can come back to this step after you install the app in the next section).

5. Re-install the app by going to `Outh & Permissions` and clicking `Reinstall App`.

6. You'll find the `SLACKFORMS_SLACK_API_TOKEN` and `SLACKFORMS_SLACK_BOT_TOKEN` you'll need for the settings in `OAuth & Permissions` under `OAuth Access Token` and `Bot User OAuth Access Token` respectively.

7. You'll find the `SLACKFORMS_SLACK_VERIFICATION_TOKEN` in `Basic Information` under `Verification Token`.

With those three tokens ready to go, you can install `django-slack-forms` in your Django app.

Next up: [install this app into your Django application.](Installation.md).
