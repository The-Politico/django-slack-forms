![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-slack-forms

*A utility to handle the creation and processing of Slack Dialogs.*

[Slack Dialogs](https://api.slack.com/dialogs) (forms) are a great and easy way to get data from members of your Slack team. They can be called in a number of ways, they're designed to work on desktop and mobile, and they're already on a familiar platform.

Unfortunately making and sending forms to your users can require an elaborate knowledge of the often-arcane Slack API. Furthermore, validation beyond required fields and character limit has to be handled programmatically by your server which more often than not means you just don't do it.

Django Slack Forms is here to solve these and more hurtles by using a popular [JSON Schema](https://json-schema.org/understanding-json-schema/index.html) to shape and validate your data. New forms can be created in a Django admin with a number of ways to connect it to outside data and webhooks. The app is designed to be as flexible as possible to accommodate your individual data needs and data structures.

At its most basic level, the app works like the chart below with you, the developer, being responsible for the third column (labeled `External`). Due to it's flexibility, this app is not plug-and-play, but hopefully this guide will help you install it into your current infrastructure in no time.

![Flowchart](/docs/media/forms5.jpg)

### Table of Contents
1. [Quickstart](#quickstart)
2. [Making Forms](#making-forms)
    * [JSON Schema](#json-schema)
    * [UI Schema](#ui-schema)
    * [Data Source And Webhook](#data-source-and-webhook)
3. [Setting Up Your Slack App](#setting-up-your-slack-app)
4. [How To Trigger A Form](#how-to-trigger-a-form)
5. [How To Respond With Feedback](#how-to-respond-with-feedback)
6. [A Complete Example](#a-complete-example)
7. [Developing This App](#developing-this-app)
    * [Running a Development Server](#running-a-development-server)
    * [Setting Up a PostgreSQL Database](#setting-up-a-postgresql-database)
    * [Routes Available In Development App](#routes-available-in-development-app)


### Quickstart

1. Install the app.

  ```
  $ pip install django-slack-forms
  ```

2. Add the app to your Django project and configure settings.

  ```python
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

### Making Forms

Django Slack Forms uses a JSON and UI schema combination derived from the [JSONSchema](https://json-schema.org/understanding-json-schema/index.html) standard and [`react-jsonschema-form`](https://github.com/mozilla-services/react-jsonschema-form).

To make a new form, go to your Django admin and make a new `Form` under `Slackforms`. You'll need to fill out the following properties:

- `Name`: A unique name for your form. This will be used to tell Slack which form you want to open. See [Setting Up Your Slack App: Step #3](#setting-up-your-slack-app).
- `Slash command`: The name of the slash command that should trigger this form. See [Setting Up Your Slack App: Step #4](#setting-up-your-slack-app).
- `Json schema`: See [JSON Schema](#json-schema).
- `Ui schema`: See [UI Schema](#ui-schema).
- `Webhook`: See [Data Source and Webhook](#data-source-and-webhook).
- `Data source:`: See [Data Source and Webhook](#data-source-and-webhook).

#### JSON Schema
This input is for mapping out what your data looks like. All official [JSON Schema](https://json-schema.org/understanding-json-schema/index.html) properties are included plus the following two custom properties:

- `enumNames`: An array of display names for the values provided in the object's `enum` property. See [here](https://github.com/mozilla-services/react-jsonschema-form#custom-labels-for-enum-fields) for more.
- `source`: An alternative way of providing acceptable values. It should be a valid URL which serves an array of JSON objects with at least `value` and `label` fields. You can also provide one of the following values to use Slack's dynamic content (`users`, `channels`, `conversations`). See [here](https://api.slack.com/dialogs#dynamic_select_elements) for more on dynamic options.

See an example [here](/EXAMPLES.md#json-schema).

#### UI Schema
This app takes inspiration from `react-jsonschema-form` but instead of rendering components, it renders an object that can be interpreted by Slack. For those familiar with Slack's form schema, I've provided the corresponding Slack property each of these is mapped to.

| Property        | Description            | Required | Default  | Example     | Slack Prop               |
| --------------- | ---------------------- | -------- | -------- | ----------- | ------------------------ |
| `ui:widget`     | The type of form input | No       | `"text"` | `"select"`  | `type` & `subtype`       |
| `ui:placeholder`| Placeholder value      | No       | None     | `"Value"`   | `placeholder`            |
| `ui:value`      | Default value          | No       | None     | `"Value"`   | `value` & `submit_label` |
| `ui:help`       | Help text to display   | No       | None     | `"A number"`| `hint`                   |
| `ui:order`      | The place of the input | No       | `999999` | `1`         | None                     |

See an example [here](/EXAMPLES.md#ui-schema).


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

###### Example
Let's take a look at an example.

You're making a new user form which adds/updates a `User` to your database. Your API is a standard one which looks and acts like this:
```
https://example.com/api/user/UNIQUE_ID/ <-- GET requests return the data of the record with that UNIQUE_ID
https://example.com/api/user/ <-- POST requests create a new record (request data has no ID)
https://example.com/api/user/ <-- PUT requests update a record (request data has ID)
```

To properly set up your form to use this setup you'd use the following values:
- Data Source: `https://example.com/api/user/{id}/`
- Webhook: `https://example.com/api/user/`

This app will fill the `{id}` in `https://example.com/api/user/{id}/` (if it exists) with the argument retrieved from the trigger and send a GET request to get starting data for the form.

Once processed, forms triggered without an ID will send POST requests to `https://example.com/api/user/` while forms triggered WITH an ID will send PUT requests to `https://example.com/api/user/` with the ID in it's `slackforms_meta_data` (see [this](/EXAMPLES.md#form-data-webhook) for an example of what that payload looks like).


### Setting Up Your Slack App
1. Go to the [Slack App Dashboard](https://api.slack.com/apps) and make a new App.

2. Under `Interactive Components`, paste the `SLACKFORMS_ROOT_URL` from your settings in `Request URL`.

3. Under `Bot Users`, click `Add a Bot User`. Give it a name and username.

4. If you want to use message actions to call new forms, click `Create New Action`. Give it a name and description, and paste the `Name` of your form (the one you made in the Django admin) in `Callback ID`.

5. If you want to call forms from slash commands go to `Slash Commands`. Name the command whatever you set the `Slash command` attribute to for your form in the Django admin. Set the `Request URL` to the `SLACKFORMS_ROOT_URL` from your settings.

6. Re-install the app by going to `Outh & Permissions` and clicking `Reinstall App`.

7. You'll find the `SLACKFORMS_SLACK_API_TOKEN` and `SLACKFORMS_SLACK_BOT_TOKEN` you'll need for the settings in `OAuth & Permissions` under `OAuth Access Token` and `Bot User OAuth Access Token` respectively.

8. You'll find the `SLACKFORMS_SLACK_VERIFICATION_TOKEN` in `Basic Information` under `Verification Token`.

### How To Trigger A Form

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

### How To Respond With Feedback
Once your webhook receives data and processes it accordingly, you may want to post a message in Slack to confirm it's success or indicate it's failure. That's what the `response_url` is for.

In the meta data for the request payload sent to your webhook is a URL. You can send a POST request to it in order to post a message in Slack. The meta data also comes with information about the channel the form was filled out in and the user who filled it out. This can be useful for creating a proper feedback message.

To post the message, send a POST request to the `request_url` with the `token` property set to the same value as `SLACKFORMS_SLACK_VERIFICATION_TOKEN`. It should also have a `payload` property which must be a serialized dictionary with the values you'd normally pass to a slack `chat.postMessage` request. You can see those properties [here](https://api.slack.com/methods/chat.postMessage) and use [this tool](https://api.slack.com/docs/messages/builder) to help you craft rich text messages with attachments.

Remember that the Slack account posting the message is actually the Slack Forms bot. You can use this to your advantage to allow for editing after a new record has been added since interactive message functionality is already pointing to Slack Form's handlers.

###### Example
Let's take a look at an example.

Just like before your `https://example.com/api/user/` endpoint takes POST requests that adds a new record. The endpoint can then respond with the following confirmation message:

```javascript
{
  "channel": "[CHANNEL_ID]",
  "text": "[USER] created a new [MODEL].",
  "attachments": [
      {
          "fallback": "Edit N/A",
          "callback_id": "[FORM_NAME]",
          "actions": [
              {
                "name": "[NEW_RECORD_ID]",
                "text": "Edit",
                "type": "button"
              }
          ],
      }
  ]
}
```

Since Slack Forms is the one making the message, simply by including the right `callback_id` and `name` you can easily make an edit button which calls the same form, but this time with some data pre-filled and with an internal state that will tell Slack Form to send a PUT request next time.

This example isn't the whole payload. For a complete take on what that should look see [this example](/EXAMPLES.md#callbacks-to-create-messages).

### A Complete Example

For a complete example of what you're responsible for developing outside this app look at the [`exampleapp`](/example/exampleapp) directory. A form configuration exists in [`fixtures.json`](/example/exampleapp/fixtures.json) which can be loaded into your database as an example.

In its views you'll see an [`API`](/example/exampleapp/views/api.py) view which serves as the form's webhook and data source (providing data via GET, creating entries via POST, and updating those entries via PUT).

You'll also see that the `API` sends a POST request to the `response_url` provided with a feedback message meant to be sent to a pre-designated feedback channel (see [Line 12](/example/exampleapp/views/api.py#L12)).

You can also find examples of an endpoint with options for a select field in the [`TestOptions`](/example/exampleapp/views/test_options.py) view and of a manual form trigger via POST request in the [`TestManual`](/example/exampleapp/views/test_manual.py) view.

### Developing This App

##### Running a Development Server

1. Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

2. In a separate terminal, start an ngrok tunnel. (If you're using the free version of ngrok don't include the `subdomain` argument.)
  ```
  $ ngrok http [YOUR_PORT_NUMBER] --subdomain=[YOUR_NGROK_SUBDOMAIN]
  ```

3. If there isn't one already, set up an app on Slack (See [Setting Up Your Slack App](/setting-up-your-slack-app)). Set the interactive `request_url` and slash command URLs to your ngrok HTTPS tunnel URL displayed in your terminal. It should be `https://[YOUR_NGROK_SUBDOMAIN].ngrok.io`.

4. If you want to develop the manual form trigger make a new slash command and set the URL to `https://[YOUR_NGROK_SUBDOMAIN].ngrok.io/test-manual/`.

##### Setting Up a PostgreSQL Database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/slackforms"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
4. Load the fixture form into your database (optional).
  ```
  $ pipenv run python manage.py loaddata exampleapp/fixtures.json
  ```

##### Routes Available In Development App
- `/`: The root of Slack Forms. Used as the URL provided to Slack as the `request_url` and the URL for every slash command.
- `/callback/`: The callback route for Slack Forms. Used as a `response_url` for POST requests sent to webhooks in order to provide feedback.
- `/admin/`: The Django admin.
- `/api/test/`: A test API endpoint for GET, POST, and PUT requests used in the example form found in the `fixtures.json`.
- `/api/options/`: A test set of options for a field used in the example form found in the `fixtures.json`.
- `/test-manual/`: A test endpoint that triggers a manual form trigger if connected to a slash command.
