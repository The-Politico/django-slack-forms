# Schema Examples

Here are examples for the various schemas and payloads you'll have to work with in this app.

## Configuration

Schemas used to create forms in the Django Admin.

### JSON Schema

Used to create the structure of the data.

```javascript
{
  "type": "object",
  "title": "Name of Your Form",
  "required": [
    "name",
    "title"
  ],
  // Slack only allows for 5 inputs per form, any more will be truncated
  "properties": {
    "name": {
      "type": "string",
      "title": "Name"
    },
    "title": {
      "type": "string",
      "title": "Job Title",
      "source": "https://example.com/api/titles.json"  // custom schema keyword for this app
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
      "enumNames": ["Administrator", "Editor", "User"]  // custom schema keyword for this app
    }
  }
}
```

### UI Schema

Used to create the look and functionality of the form.

```javascript
{
  "name": { // key names should match the keys in JSON Schema properties
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
  "submit": { // custom key for submit button
    "ui:value": "Save"
  }
}
```

## Payloads Received By Slack Forms

Various payloads that this app will ingest for the purposes of creating and handling forms.

### Sources for Properties
This app's JSON Schema properties can have a `source` property of their own which points to an endpoint. This is an example of one of those endpoints.
```javascript
[
  {
    "label": "One",
    "value": 1
  },
  {
    "label": "Two",
    "value": 2
  },
  {
    "label": "Three",
    "value": 3
  },
  {
    "label": "Four",
    "value": 4
  },
  {
    "label": "Five",
    "value": 5
  }
]
```

### 
