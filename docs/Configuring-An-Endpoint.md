# Configuring An Endpoint

`django-slack-forms` handles all the form validation and processing for you, but it doesn't know what to do with that data. While configuring an endpoint isn't required, without one all the data has nowhere to go.

This is one of those points where the app's flexibility makes documentation difficult. The app will take any URL as a valid endpoint, which means you can set it up using your stack of choice (e.g. `Express`, `Flask`, `LAMP`, static files on S3, etc.). Since this is a pluggable Django app, the most obvious kind of endpoint is a [Django View](https://docs.djangoproject.com/en/2.1/topics/http/views/).

Each form you create (as in each individual schema) can have its own endpoint. When a Slack form of that type is submitted, validated, and processed, your designated endpoint will receive a request with the processed data and some extra metadata.

The data will be a JSON object with keys that match the `properties` you named in your JSON Schema. There will also be an extra key named `slackform_meta_data` which will be a stringified dictionary containing metadata. In order to use the metadata, you'll have to parse it (such as with `json.loads()` in Python or `JSON.parse()` in JavaScript).

`django-slack-forms` will send the request and forget about the form data. It doesn't care about the response status (or lack thereof). It's up to your endpoint to be available, do whatever you need it to, and log errors in a manner appropriate for you. The app does come with a way to provide feedback to users in Slack which is detailed in the advanced [Slack Feedback](Slack-Feedback.md) section.

## Registering An Endpoint

In order to verify that requests to your endpoint are coming from `django-slack-forms` endpoints must be registered in the Django admin. Doing this is standard Django affair. Give it a unique name and URL. Once you save it, you should see a token. This token will be sent to the endpoint whenever a form is completed.

### Example
Let's take a look at an example. Consider a form using the following abbreviated JSON Schema (See [Creating Forms](Creating-Forms.md) for more on JSON Schema):

```javascript
{
  "type": "object",
  "title": "Name of Your Form",
  "properties": {
    "name": { ... },
    "title": { ... },
    "age": { ... },
    "biography": { ... },
    "permissions": { ... }
  }
}
```

Your endpoint will receive the following POST request if I (Andrew Briz) were to fill out a form of this type:

```javascript
{
  "slackform_meta_data": { // this dictionary will be a serialized string
    "token": "3829AGBWI1923H2N194" // The token registered to this endpoint
    "data_id": "321231", // The ID of the model being updated or null in POST requests
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
    "form_name": "Test" // the unique name of the form that was filled out
  },
  "name": "Andrew Briz",
  "title": "apps-dev",
  "age": "22",
  "biography": "He's a developer on POLITICO's Interactives Team.",
  "permissions": "admin"
}
```

You might see some keys in the metadata that are unclear (`data_id` and `response_url`). Don't worry about them for now, I'll cover how to use them in the advanced sections. Remember though that the `slackform_meta_data` is actually a stringified dictionary so the request actually looks like this:

```javascript
{
  "name": "Andrew Briz",
  "title": "apps-dev",
  "age": "22",
  "biography": "He's a developer on POLITICO's Interactives Team.",
  "permissions": "admin",
  "slackform_meta_data": "{ ... }",
}
```

## Connecting An Endpoint
Once you've decided on an endpoint and have it hosted, you should have have a URL for it. Take that URL and save it as the form's `Endpoint` property in the Django admin of `django-slack-forms`.

Next up: check out one of the following advanced topics:

1. [External Source Data](Configuring-Source-Data.md)

2. [REST API Integration](Integrating-An-API.md)

3. [Custom Form Triggers](Custom-Form-Triggers.md)

4. [Posting Feedback In Slack](Slack-Feedback.md)
