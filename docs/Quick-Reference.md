# Quick Reference Guide

Here are examples for the various schemas and payloads you'll have to work with in this app.

## Table of Contents

- [Configuration](#Configuration)
  - [JSON Schema](#json-schema)
  - [UI Schema](#ui-schema)
- [Endpoint Payloads](#endpoint-payloads)
  - [POST](#post)
  - [PUT](#put)
  - [DELETE](#delete)
- [Payloads Received By Slack Forms](#payloads-received-by-slack-forms)
  - [Data Sources](#data-sources)
  - [Manual Form Triggers](#manual-form-triggers)
  - [Callbacks To Create Messages](#callbacks-to-create-messages)
  - [Callbacks To Create Messages (custom)](#callbacks-to-create-messages-custom)
  - [Button/Option Values For Custom Messages](#buttonoption-values-for-custom-messages)


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

## Endpoint Payloads

This app also produces payloads of it's own which it sends to various endpoints you might be developing.

In order to allow for `slackform_meta_data` to be a multi-layer dictionary, it will need to be  de-stringified (such as with `json.loads()`). In reality when you see this in the payload examples below:

```JavaScript
{
  "slackform_meta_data": {
    "token": "3829AGBWI1923H2N194" // The token registered to this form
    "data_id": null

    ...

  }

  ...
}

```

It really looks like this:

```JavaScript
{
  "slackform_meta_data": "{ ... }",

  ...
}
```



### POST

After a form for a new record is submitted, validated, and processed the form data will be sent to the configured endpoint (as configured in the Django admin).

```javascript
{
  "slackform_meta_data": { // this dictionary will be a serialized string
    "token": "3829AGBWI1923H2N194" // The token registered to this form
    "data_id": null,
    "team": { // the team the form was finished in
      "id": "TEMGAT2Z",
      "domain": "your-team"
    },
    "channel": { // the channel the form was finished in
      "id": "C8LAQNJ",
      "name": "general"
    },
    "user": { // the user who finished the form
      "id": "UELJYGUAJ",
      "name": "briz.andrew"
    },
    "response_url": "https://example.com/forms/callback/",
    "form": "Test" // the unique name of the form that was filled out
  },
  "name": "Andrew Briz", // property in the form
  "title": "apps-dev", // property in the form
  "age": "22", // property in the form
  "biography": "He's a developer on POLITICO's Interactives Team.", // property in the form
  "permissions": "admin" // property in the form
}
```

### PUT

After a form for an existing record is submitted, validated, and processed the form data will be sent to the configured endpoint (as configured in the Django admin).

```javascript
{
  "slackform_meta_data": { // this dictionary will be a serialized string
    "token": "3829AGBWI1923H2N194" // The token registered to this form
    "data_id": "321231", // The ID of the record being updated
    "team": { // the team the form was finished in
      "id": "TEMGAT2Z",
      "domain": "your-team"
    },
    "channel": { // the channel the form was finished in
      "id": "C8LAQNJ",
      "name": "general"
    },
    "user": { // the user who finished the form
      "id": "UELJYGUAJ",
      "name": "briz.andrew"
    },
    "response_url": "https://example.com/forms/callback/",
    "form": "Test" // the unique name of the form that was filled out
  },
  "name": "Andrew Briz", // property in the form
  "title": "apps-dev", // property in the form
  "age": "22", // property in the form
  "biography": "He's a developer on POLITICO's Interactives Team.", // property in the form
  "permissions": "admin" // property in the form
}
```

### DELETE

If a form delete button is clicked in a feedback message, metadata will be sent to the configured endpoint (as configured in the Django admin).

```javascript
{
  "slackform_meta_data": { // this dictionary will be a serialized string
    "token": "3829AGBWI1923H2N194" // The token registered to this form
    "data_id": "321231", // The ID of the record to be deleted
    "team": { // the team the button was clicked in
      "id": "TEMGAT2Z",
      "domain": "your-team"
    },
    "channel": { // the channel the button was clicked in
      "id": "C8LAQNJ",
      "name": "general"
    },
    "user": { // the user who clicked the button
      "id": "UELJYGUAJ",
      "name": "briz.andrew"
    },
    "response_url": "https://example.com/forms/callback/",
    "form": "Test" // the unique name of the form that was filled out
  }
}
```

## Payloads Received By Slack Forms

Various payloads that this app will ingest for the purposes of creating and handling forms.

### Data Sources
This app's JSON Schema properties can have a `source` property of their own which points to an endpoint. This is an example of one of those endpoints.

```javascript
[
  {
    "label": "News Apps Editor",
    "value": "apps-editor"
  },
  {
    "label": "Senior News Apps Developer",
    "value": "apps-dev-senior"
  },
  {
    "label": "News Apps Developer",
    "value": "apps-dev"
  },
  {
    "label": "Graphics Editor",
    "value": "graphics-editor"
  },
  {
    "label": "Graphics Reporter",
    "value": "graphics-reporter"
  }
]
```

### Manual Form Triggers
Forms can be triggered manually by hitting the root of the app with a proper payload.

```javascript
{
  "payload": {
    "type": "manual",
    "form": "Test",
    "token": "S3C639pZqXvR2toPwcng", // The token registered to an endpoint or the Slack verification token
    "trigger_id": "32fneo2043",  // sent to your App from Slack via a user action
    "data_id": "321231",  // optional
    "method": "POST" // optional (either "POST" or "PUT")
    "data": {  // optional
      "name": "Andrew Briz Override"
    },
  }
}
```

In order to properly parse the request, the `payload` dictionary should be stringified (such as with `json.dumps()`) so that the request data actually looks like this in the end:

```javascript
{
  "payload": "{ ... }"
}
```

### Callbacks To Create Messages
Once a message has been processed, message feedback can be sent to a the `/callback/` endpoint to post messages in a given channel as the Slack Forms bot.

```javascript
{
  "token": "S3C639pZqXvR2toPwcng", // The token registered to an endpoint or the Slack verification token
  "channel": "C8LAQNJ",
  "text": "Success!", // optional
  "new": "New", // optional
  "delete": "Delete", // optional
  "edit": "Edit", // optional
  "data_id": "5", // required if "edit" or "delete" is used
  "form": "ticket", // required if "new", "edit", or "delete" is used
}
```


### Callbacks To Create Messages (Custom)
Once a message has been processed, custom messages can be sent to a the `/message/` endpoint to post messages in a given channel as the Slack Forms bot. This method is for creating custom messages and taking full advantage of the Slack API. For a simpler version see previous section.

```javascript
{
  "token": "S3C639pZqXvR2toPwcng", // The token registered to an endpoint or the Slack verification token
  "payload": {
    "channel": "C8LAQNJ",
    "message": {
      "text": "Success!"
    }
  }
}
```

In order to properly parse the request, the `payload` dictionary should be stringified (such as with `json.dumps()`) so that the request data actually looks like this in the end:

```javascript
{
  "token": "S3C639pZqXvR2toPwcng",
  "payload": "{ ... }"
}
```

The data in `payload` can be any of the arguments of the [`postMessage`](https://api.slack.com/methods/chat.postMessage) Slack API method (except `token` which is handled by Slack Forms).

### Button/Option Values For Custom Messages
If you're using a custom message for feedback (i.e. using the `/message/` endpoint), you might want to include buttons or drop down menus that create, edit, or delete new forms. In order to do that the `value` of the button/option should be a stringified dictionary that looks like this:

```javascript
{
  "method": "PUT", // POST, PUT, or DELETE for new, edit, or delete respectively
  "data_id": "321231", // The ID of the record to edit or delete
  "form": "ticket" // The unique name of the form to edit
}
```
