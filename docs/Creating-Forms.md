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
