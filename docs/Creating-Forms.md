# Creating Slack Forms

Django Slack Forms uses a JSON and UI schema combination derived from the [JSONSchema](https://json-schema.org/understanding-json-schema/index.html) standard and [`react-jsonschema-form`](https://github.com/mozilla-services/react-jsonschema-form).

The JSON schema shapes what your data looks like. Is it a string or an integer? Does it have a maximum value or character length? Should it be one of a list of values? These are all questions that can be answered in your JSON Schema.

Alternatively, The UI Schema determines what the form looks like on Slack and is tied much more closely to the Slack API's options. Is that input a single row input or a larger text area? Does the input have a placeholder or default value? Is there any help text provided? These kinds of questions are answered in your UI Schema.

## The Django Admin

To make a new form, go to your Django admin and make a new `Form` under `Slackforms`. You'll need to fill out the following properties:

- `Name`: A unique name for your form.
- `Slash command`: The name of the slash command that should trigger this form. See [Setting Up Your Slack App: Step #4](Slack-App.md).
- `Json schema`: See [JSON Schema](#json-schema).
- `Ui schema`: See [UI Schema](#ui-schema).

These properties are optional and will be covered in subsequent sections:
- `Webhook`: See [Configuring An Endpoint](Configuring-An-Endpoint.md).
- `Data source:`: See [Configuring An API](Configuring-An-API.md).

### JSON Schema
This input is for mapping out what your data looks like. All official [JSON Schema](https://json-schema.org/understanding-json-schema/index.html) properties are included plus the following two custom properties:

- `enumNames`: An array of display names for the values provided in the object's `enum` property. See [here](https://github.com/mozilla-services/react-jsonschema-form#custom-labels-for-enum-fields) for more on the idea behind it.
- `source`: An alternative way of providing acceptable values. [See Configuring Source Data](Configuring-Source-Data.md) for more.

An added limitation imposed by Slack is a five-input limit. If you try to create a form with more than five properties, you will receive an error in the admin.

Because this standard is created and maintained by others, I recommend using the links provided above for more comprehensive help on creating JSON schemas.

#### Example

To get started, check out this simple example which defines five properties (two of which are required) with different data signatures:

```javascript
{
  "type": "object",
  "title": "Name of Your Form",
  "required": [
    "name",
    "title"
  ],
  "properties": {
    "name": {
      "type": "string",
      "title": "Name"
    },
    "title": {
      "type": "string",
      "title": "Job Title",
    },
    "age": {
      "type": "number",
      "title": "Age",
      "minimum": 21
    },
    "biography": {
      "type": "string",
      "title": "Bio",
      "maxLength": 300
    },
    "permissions": {
      "type": "string",
      "title": "Permissions",
      "enum": ["admin", "edit", "user"],
      "enumNames": ["Administrator", "Editor", "User"]
    }
  }
}
```

### UI Schema
This app takes inspiration from `react-jsonschema-form` but instead of rendering components, it renders an object that can be interpreted by Slack. It's formed by creating a dictionary with keys that match those in your JSON Schemas `properties`. Those dictionaries can then take the following options which help define what it's form input looks like. All of those properties have default values so none of them are required.


For those familiar with Slack's form schema, I've provided the corresponding Slack property each of these is mapped to.

| Property        | Description            | Required | Default  | Example     | Slack Prop               |
| --------------- | ---------------------- | -------- | -------- | ----------- | ------------------------ |
| `ui:widget`     | The type of form input | No       | `"text"` | `"select"`  | `type` & `subtype`       |
| `ui:placeholder`| Placeholder value      | No       | None     | `"Value"`   | `placeholder`            |
| `ui:value`      | Default value          | No       | None     | `"Value"`   | `value` & `submit_label` |
| `ui:help`       | Help text to display   | No       | None     | `"A number"`| `hint`                   |
| `ui:order`      | The place of the input relative to other inputs | No       | `999999` | `1`         | None                     |

The available widgets are: `text`, `textarea`, `select`, `email`\*, `number`\*, `tel`\*, and `url`\*. They must be spelled in all-lowercase. Also note that the `*` widgets are specialized text fields which control the keyboard on mobile devices. These subtypes don't come with any built in validation. For more on text subtypes, check out [the Slack docs](https://api.slack.com/dialogs#text_elements).

### The `submit` Key

The UI Schema can also take a special key called `submit`, which shouldn't match with any of the properties in your JSON Schema. It must be a dictionary which only takes a single key (`ui:value`) which allows you to customize the text of the submit button on Slack. This too is optional and will default to `Submit` if no value is provided.

#### Example
Here's an example for what a UI Schema might look like to match the example JSON Schema above:

```javascript
{
  "name": {
    "ui:widget": "text",
    "ui:placeholder": "Johny Appleseed",
    "ui:order": 1
  },
  "title": {
    "ui:widget": "select",
    "ui:order": 2
  },
  "age": {
    "ui:widget": "number",
    "ui:value": 21,
    "ui:order": 3
  },
  "biography": {
    "ui:widget": "textarea",
    "ui:help": "300 character limit",
    "ui:order": 4
  },
  "permissions": {
    "ui:widget": "select",
    "ui:order": 5
  },
  "submit": {
    "ui:value": "Save"
  }
}
```

Next up: [Configure an endpoint to receive your form data.](Configuring-An-Endpoint.md)
