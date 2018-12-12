# How To Trigger A Form

#### Data Source And Webhook
In many cases you'll want to edit an existing record as well as create new ones. In order to connect your form to a data source, you'll need to configure an API endpoint for the form, and to do that the user action that triggers that form needs to have a ID associated with it.

Luckily, every form trigger (see [How To Trigger A Form](#how-to-trigger-a-form)) comes with a single argument (see table below). Once the argument is parsed from the trigger it will be passed to your form's `data_source` template as an `id` variable which you can you use when creating a Python template string.

Once you have data in your form, you can send the processed and validated form data to a `Webhook` which is also configured in the admin.

| Method                                                 | Location                   | Example                                                         |
| ------------------------------------------------------ | -------------------------- | --------------------------------------------------------------- |
| [Slash Commands](https://api.slack.com/slash-commands) | The text after the command | `/my-command [ARGUMENT]`                                        |
| [Buttons](https://api.slack.com/docs/message-buttons)  | The `name` of the button   | `{"name": "[ARGUMENT]", "text": "My Button", "type": "button"}` |
| [Menus](https://api.slack.com/docs/message-menus)      | The  `value` of the option | `{"text": "My Option", "value": "[ARGUMENT]"}`                  |
| [Actions](https://api.slack.com/actions)               | The text of the message    | `[ARGUMENT]`                                                    |

4. If you want to use message actions to call new forms, click `Create New Action`. Give it a name and description, and paste the `Name` of your form (the one you made in the Django admin) in `Callback ID`.

Slack Forms comes with a number of ways to trigger a form, but each one requires a `trigger_id` provided by Slack. As of 2018, the following Slack features provide `trigger_id`s:
- [Slash Commands](https://api.slack.com/slash-commands)
- [Message Buttons](https://api.slack.com/docs/message-buttons)
- [Message Menus (dropdowns)](https://api.slack.com/docs/message-menus)
- [Message Actions](https://api.slack.com/actions)

This app is built to handle each of these by default if they're set up properly in your Slack App dashboard (see [Setting Up Your Slack App](#setting-up-your-slack-app)). Forms can also be triggered in two manual ways, but they still require a `trigger_id`. You might want to do this if you want to intercept a user action (e.g. a slash command), do something, and then trigger the form.

The first way to manually trigger a form is to send a POST request to the `SLACKFORMS_ROOT_URL`. The request data MUST have a single key named `payload` which is a serialized JSON object. That payload should have the following properties:

| Property        | Description                                                   | Required |
| --------------- | ----------------------                                        | -------- |
| `type`       | Must be set to `manual`.                                         | Yes      |
| `form`       | The unique `name` of the form to trigger.                        | Yes      |
| `token`      | The Slack verification token found in your Slack App Dashboard.  | Yes      |
| `trigger_id` | The `trigger_id` created by a user action in Slack.              | Yes      |
| `data`       | A dictionary with overriding data values.                        | No       |
| `data_id`    | The Id of the data to be retrieved form the form's `data_source`.| No       |

See [this](/EXAMPLES.md#manual-form-triggers) for an example of what that payload should look like.

If this app is installed in the app you're trying to trigger the form from, you can also trigger the form from within your Python code using the model's `post_to_slack` function and passing the `trigger_id` as the first argument as well as optionally passing the `data` and `data_id` kwargs to the function like so:

```python
form = Form.objects.get(name="NAME_OF_FORM")
form.post_to_slack("TRIGGER_ID", data_id="12345", data={"prop": "value"})
```

In both cases if both `data` and `data_id` are provided the two data sources will be merged. Data properties provided explicitly through the `data` argument will override source data retrieved from the `data_source` endpoint designated with `data_id` if the key exists in both.
