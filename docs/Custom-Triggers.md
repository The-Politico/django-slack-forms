# How To Trigger A Form

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
