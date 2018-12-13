# How To Trigger A Form

*Note: This is an advanced section. It's expected that you have an understanding of the app outlined in the basic sections of these docs before reading this page.*

The introduction docs assumed that new forms would be triggered through slash commands, but that's only one way to trigger forms in `django-slack-forms`. The five ways to trigger a form are:
  - [Slash Commands](https://api.slack.com/slash-commands)
  - [Message Buttons](https://api.slack.com/docs/message-buttons)
  - [Message Menus](https://api.slack.com/docs/message-menus)
  - [Message Actions](https://api.slack.com/actions)
  - Manually via endpoint*

<em>\*Manual form triggers must be the result of a user action on Slack (i.e. one of the other four types of triggers). See [The Slack trigger_id](#the-slack-trigger_id) for more.</em>

## Triggers From Slack

`django-slack-forms` comes with a number of ways to trigger forms from user actions on Slack. When a form is triggered it can either start with empty data or with data from an API (for more on setting up that API see [Integrating A REST API](Integrating-An-API.md)).

However in order to start with data from your API, `django-slack-forms` needs an ID for the record being edited. And each method passes that ID differently. You can see each of those way in the table below:

| Method                                                 | Location                   | Example                                                         |
| ------------------------------------------------------ | -------------------------- | --------------------------------------------------------------- |
| Slash Commands | The text after the command | `/my-command [ID]`                                        |
| Message Actions | The text of the message    | `[ID]`                                                    |
| Message Buttons | The stringified `value` of the button   | `{"name": "name", "text": "My Button", "type": "button", "value": "{\"method\": \"PUT\", \"data_id\": \"[ID]\", \"form\": \"ticket\"}"` |
| Message Menus |  The stringified `value` of the option | `{"text": "My Option", "value": "{\"method\": \"PUT\", \"data_id\": \"[ID]\", \"form\": \"ticket\"}"}`                  |


### Slash Commands
For help setting up slash commands see [Setting Up Your Slack App](Slack-App.md) step #4.

### Message Actions
Create a new message action by going to `Interactive Components` in the [Slack API Dashboard](https://api.slack.com/apps/) for your app. Click `Create New Action`. Give the action a name and set the `Callback ID` to the unique `name` of the form you want to trigger.

If you don't see the action appear in your message's context menu, try reinstalling the Slack app by going to `Outh & Permissions` and clicking `Reinstall App`.

### Message Buttons & Message Menus
Using the tokens of the same Slack App as `django-slack-forms`, you can create messages using the `chat.postMessage` method. Check out the [Slack API GitHub page](https://github.com/slackapi) for more on using the API to post messages.

For help creating a Slack button see [the official docs](https://api.slack.com/docs/message-buttons).
The value of the button or option must be a stringified dictionary (such as with `json.dumps()`) which contains the following properties:

| Property    | Description                                               | Required           |
| ------------| ----------------------                                    | ------------------ |
| `method`    | `POST` to trigger a new form or `PUT` to trigger an edit. | Yes                |
| `form`      | The unique `name` of the form you want to trigger.        | Yes                |
| `data_id`   | The ID of the record to edit.                             | If method is `PUT` |


##### IMPORTANT
In order to trigger forms, buttons and menus must come from the same Slack App that is processing forms. Read more about using this app to create custom messages with buttons in [Posting Feedback In Slack](Slack-Feedback.md).

## Manual Triggers

Manual triggers exist in `django-slack-forms` as a catch-all system for custom behavior. Maybe you want to intercept a slash command and run some code before triggering the form. If you're familiar with Slack and want to handle triggering on your own, there's a couple ways to do that.

### The Slack `trigger_id`
First, a quick word about the `trigger_id`.

In order to know which user to serve a form to, Slack requires a special ID known as a `trigger_id` which the API provides as the result of certain user actions (e.g. slash commands, button clicks, etc.). `django-slack-forms` handles passing this `trigger_id` along from its list of available form triggers, but in order to manually trigger one you'll need to acquire one and pass it through the request.

For more on `trigger_id`s and where to get them, check out the [official docs](https://api.slack.com/docs/triggers).

### Trigger Via Webook
The first way to manually trigger a form is to send a POST request to the root of `django-slack-forms` (whatever you set `SLACKFORMS_ROOT_URL` to in your Django settings). The request data MUST have a single key named `payload` which is a stringified JSON object. That payload should have the following properties:

| Property     | Description                                                      | Required |
| -------------| ---------------------------------------------------------------- | -------- |
| `type`       | Must be set to `manual`                                          | Yes      |
| `form`       | The unique `name` of the form to trigger                         | Yes      |
| `token`      | The token registered in the Django admin                         | Yes      |
| `trigger_id` | The `trigger_id` created by a user action in Slack               | Yes      |
| `data`       | A dictionary with overriding data values                         | No       |
| `data_id`    | The Id of the data to be retrieved form the form's `data_source` | No       |

In the end, the payload should look like this with those options inside:

```javascript
{
  "payload": "{ ... }"
}
```

### Trigger Via Python
If `django-slack-forms` is installed in the app you're trying to trigger the form from, you have access to its `Form` model. You can trigger a form with a `Form` object's `trigger` function and pass the `trigger_id` as the first argument as well as optionally some kwargs:

| Property     | Description                                                    | Default  |
| ----------| ----------------------------------------------------------------- | -------- |
| `method`  | `POST` to trigger a new form or `PUT` to trigger an edit          | `"POST"` |
| `data`    | A dictionary with overriding data values                          | `{}`     |
| `data_id` | The Id of the data to be retrieved form the form's `data_source`  | `""`     |

It would look something like this:

```python
from slackforms.models import Form

f = Form.objects.get(name="NAME_OF_FORM")
f.trigger(
  "TRIGGER_ID",
  method="POST",
  data_id="12345",
  data={"prop": "value"}
)
```

### One Final Note About Overriding Data
Both methods of manual form triggers come with a way to supply `data` and `data_id` arguments. If both are provided the two data sources will be merged. Data properties provided explicitly through the `data` argument will override source data retrieved from the `data_source` endpoint designated with `data_id` if that particular property exists in both.
