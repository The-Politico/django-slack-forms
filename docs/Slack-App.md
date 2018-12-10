# Setting Up Your Slack App

1. Go to the [Slack App Dashboard](https://api.slack.com/apps) and make a new App.

2. Under `Interactive Components`, paste the `SLACKFORMS_ROOT_URL` from your settings in `Request URL`.

3. Under `Bot Users`, click `Add a Bot User`. Give it a name and username.

4. If you want to use message actions to call new forms, click `Create New Action`. Give it a name and description, and paste the `Name` of your form (the one you made in the Django admin) in `Callback ID`.

5. If you want to call forms from slash commands go to `Slash Commands`. Name the command whatever you set the `Slash command` attribute to for your form in the Django admin. Set the `Request URL` to the `SLACKFORMS_ROOT_URL` from your settings.

6. Re-install the app by going to `Outh & Permissions` and clicking `Reinstall App`.

7. You'll find the `SLACKFORMS_SLACK_API_TOKEN` and `SLACKFORMS_SLACK_BOT_TOKEN` you'll need for the settings in `OAuth & Permissions` under `OAuth Access Token` and `Bot User OAuth Access Token` respectively.

8. You'll find the `SLACKFORMS_SLACK_VERIFICATION_TOKEN` in `Basic Information` under `Verification Token`.
