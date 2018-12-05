![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-slack-forms

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

  SLACKFORMS_SLACK_VERIFICATION_TOKEN = ""  # From Slack API Dashboard
  SLACKFORMS_SLACK_API_TOKEN = ""  # From Slack API Dashboard
  SLACKFORMS_ROOT_URL = ""  # Root URL of where this app will be installed
  ```

### Making Forms

Django Slack Forms uses a JSON and UI schema combination derived from the [JSONSchema](https://json-schema.org/understanding-json-schema/index.html) standard and [`react-jsonschema-form`](https://github.com/mozilla-services/react-jsonschema-form).

To make a new form, go to your Django admin and make a new `Form` under `Slackforms`. You'll need to fill out the following properties:

- `Name`: A unique name for your form. This will be used to tell Slack which form you want to open. See [Setting Up Your Slack App: Step #3](/#setting-up-your-slack-app).
- `Slash command`: The name of the slash command that should trigger this form. See [Setting Up Your Slack App: Step #4](/#setting-up-your-slack-app).
- `Webhook`: See [Data Source and Webhook](/#data-source-and-webhook).
- `Json schema`: See [JSON Schema](/#json-schema).
- `Ui schema`: See [UI Schema](/#ui-schema).
- `Data source:`: See [Data Source and Webhook](/#data-source-and-webhook).

#### JSON Schema
This input is for mapping out what your data looks like. All official JSON Schema properties are included plus the following two custom properties:

- `enumNames`: An array of display names for the values provided in the object's `enum` property. See [here](https://github.com/mozilla-services/react-jsonschema-form#custom-labels-for-enum-fields) for more.
- `source`: An alternative way of providing acceptable values. It should be a valid URL which serves an array of JSON objects with at least `value` and `label` fields. You can also provide one of the following values to use Slack's dynamic content (`users`, `channels`, `conversations`). See [here](https://api.slack.com/dialogs#dynamic_select_elements) for more on dynamic options.

Here's an example of a JSON Schema:

#### UI Schema
This app takes inspiration from `react-jsonschema-form` but instead of rendering components, it renders an object that can be interpreted by Slack. For those familiar with Slack's form schema, I've provided the corresponding Slack property each of these is mapped to.

| Property        | Description            | Required  | Example     | Slack Prop               |
| --------------- | ---------------------- | --------- | ----------- | ------------------------ |
| `ui:widget`     | The type of form input | Yes       | `"text"`    | `type` & `subtype`       |
| `ui:placeholder`| Placeholder value      | No        | `"Value"`   | `placeholder`            |
| `ui:value`      | Default value          | No        | `"Value"`   | `value` & `submit_label` |
| `ui:help`       | Help text to display   | No        | `"A number"`| `hint`                   |
| `ui:order`      | The place of the input | No        | `1`         | None                     |

Here's an example UI Schema:


#### Data Source And Webhook
In many cases you'll want to edit a model as much as you want to create a new one. In order to connect your form to a data source, you'll need to configure an API endpoint for the form. Every form trigger (see [How To Trigger A Form](/#how-to-trigger-a-form)) which comes with a single argument (see table below). Once the argument is parsed from the trigger it will be passed to your form's `data_source` template as an `id` variable which you can you use when creating a python template string.

Once you have data in your form, you can send the processed and validated form data to a `Webhook` which is also configured in the admin.

| Method          | Location                   | Example  |
| --------------- | -------------------------- | --------- |
| Slash Commands  | The text after the command | `/my-command [ARGUMENT]`                                        |
| Buttons         | The `name` of the button   | `{"name": "[ARGUMENT]", "text": "My Button", "type": "button"}` |
| Menus           | The  `value` of the option | `{"text": "My Option", "value": "[ARGUMENT]"}`                  |
| Actions         | The text of the message    | `[ARGUMENT]`                                                    |

Let's take a look at an example.

You're making a new user form which adds/updates a `User` to your database. Your API is a standard one which looks and acts like this:
```
https://example.com/api/user/UNIQUE_ID/ <-- GET requests return the data of the entry with that UNIQUE_ID
https://example.com/api/user/ <-- POST requests create a new entry (request data has no ID)
https://example.com/api/user/ <-- PUT requests update an entry (request data has ID)
```

To properly set up your form to use this setup you'd use the following values:
- Data Source: `https://example.com/api/user/{id}/`
- Webhook: `https://example.com/api/user/`

This app will fill the `{id}` in `https://example.com/api/user/{id}/` with the argument retrieved from the trigger and send a GET request to get starting data for the form. Once processed, forms triggered without an ID will send POST requests to `https://example.com/api/user/` while forms triggered WITH an ID will send PUT requests to `https://example.com/api/user/` with the ID in it's `slackforms_meta_data` (see [Example Payloads](/#example-payloads) to see what that looks like).


### Setting Up Your Slack App
1. Go to the [Slack App Dashboard](https://api.slack.com/apps) and make a new App.

2. Under `Interactive Components`, paste the `SLACKFORMS_ROOT_URL` from your settings in `Request URL`.

3. If you want to use message actions to call new forms, click `Create New Action`. Give it a name and description, and paste the `name` of your form (the one you made in the Django admin) in `Callback ID`.

4. If you want to call forms from slash commands go to `Slash Commands`. Name the command whatever you set the `Slash command` attribute to for your form in the Django admin. Set the `Request URL` to the `SLACKFORMS_ROOT_URL` from your settings.

5. Re-install the app by going to `Outh & Permissions` and clicking `Reinstall App`.

### How To Trigger A Form

Slack Forms comes with a number of ways to trigger a form, but each one requires a `trigger_id` provided by Slack. As of 2018, the following Slack features provide `trigger_id`s:
- [Slash Commands](https://api.slack.com/slash-commands)
- [Message Buttons](https://api.slack.com/docs/message-buttons)
- [Message Menus (dropdowns)](https://api.slack.com/docs/message-buttons)
- [Message Actions](https://api.slack.com/actions)

This app is built to handle each of these by default if they're set up properly in your Slack App dashboard (see [Setting Up Your Slack App](/#setting-up-your-slack-app)). Forms can also be triggered in two manual ways, but they still require a `trigger_id`. You might want to do this if you want to intercept a user action (e.g. a slash command), do something, and then trigger the form.

The first way to manually trigger a form is to send a POST request to the `SLACKFORMS_ROOT_URL`. The request data must have a single key named `payload` which is a serialized JSON object. That payload MUST have the following properties:

| Property        | Description                                                   | Required |
| --------------- | ----------------------                                        | -------- |
| `type`       | Must be set to `manual`.                                         | Yes      |
| `form`       | The unique name of the form to trigger.                          | Yes      |
| `token`      | The Slack verification token found in your Slack App Dashboard.  | Yes      |
| `trigger_id` | The `trigger_id` created by a user action in Slack.              | Yes      |
| `data`       | A dictionary with overriding data values.                        | No       |
| `data_id`    | The Id of the data to be retrieved form the form's `data_source`.| No       |

If this app is installed in the app you're trying to trigger the form from, you can also trigger the form from within your Python code using the model's `post_to_slack` function and passing the `trigger_id` as the first argument as well as optionally passing the `data` and `data_id` named arguments to the function.

In both cases if both `data` and `data_id` are provided the two data sources will be merged. Data properties provided explicitly through the `data` argument will override source data retrieved from the `data_source` endpoint designated with `data_id` if they exist in both.


### Developing

##### Running a development server

Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

##### Setting up a PostgreSQL database

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
