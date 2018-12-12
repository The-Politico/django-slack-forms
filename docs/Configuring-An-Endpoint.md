# Configuring An Endpoint

`django-slack-forms` handles all the form validation and processing for you, but it doesn't know what to do with that data. While configuring an endpoint isn't required, without one all the data has nowhere to go.

This is one of those points where the app's flexibility makes documentation difficult. The app will take any URL as a valid endpoint, which means you can set it up using your stack of choice (e.g. `Express`, `Flask`, `LAMP`, static files on S3, you could even spam `http://example.com` with POST requests if you really want to). Since this is a pluggable Django app, the most obvious kind of endpoint is a [Django View](https://docs.djangoproject.com/en/2.1/topics/http/views/).

Each form you create (as in each individual schema) can have its own endpoint. When a Slack form of that type is submitted, validated, and processed, your designated endpoint will receive a POST request with the processed data and some extra metadata.

The data will be a JSON object with keys that match the `properties` you named in your JSON Schema. There will also be an extra key named `slackforms_meta_data` which will be a stringified dictionary containing metadata. In order to use the metadata, you'll have to parse it (such as with `json.loads()` in Python or `JSON.parse()` in JavaScript).

`django-slack-forms` will send the request and forget about the form data. It doesn't care about the response status (or lack thereof). It's up to your endpoint to be available, do whatever you need it to, and log errors in a manner appropriate for you. The app does come with a way to provide feedback to users in Slack which is detailed in the advanced [Slack Feedback](Slack-Feedback.md) section.

### Example
Let's take a look at an example given that your form is using the following abbreviated JSON Schema (See [Creating Forms](Creating-Forms.md) for more on JSON Schema):

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

Your endpoint will receive the following POST request if I (Andrew Briz) were to fill it out:

```javascript
{
  "slackforms_meta_data": { // this dictionary will be a serialized string
    "token": "3829AGBWI1923H2N194" // Slack verification token
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

You might see some keys in the metadata that are unclear (`data_id` and `response_url`). Don't worry about them for now, I'll cover how to use them in the advanced sections. Remember though that the `slackforms_meta_data` is actually a stringified dictionary so the request actually looks like this:

```javascript
{
  "name": "Andrew Briz",
  "title": "apps-dev",
  "age": "22",
  "biography": "He's a developer on POLITICO's Interactives Team.",
  "permissions": "admin",
  "slackforms_meta_data": "{ ... }",
}
```

## Securing An Endpoint

You probably shouldn't have an open endpoint that will allow any user with the URL to send successful POST requests to your endpoint.

One simple way to verify that the request is coming from `django-slack-forms` is to check the `token` inside of `slackforms_meta_data`. This token will be the same `SLACK_VERIFICATION_TOKEN` you set in your settings which you can also find in your Slack App Dashboard.

## Connecting An Endpoint
Once you've decided on an endpoint and have it hosted, you should have have a URL for it. Take that URL and save it as the form's `Webhook` property in the Django admin of `django-slack-forms`.

Next up: check out one of the following advanced topics:

Once you have the basics down, you can move on to more advanced topics like:

1. [External Source Data](docs/Configuring-Source-Data.md)

2. [REST API Integration](docs/Integrating-An-API.md)

3. [Custom Form Triggers](docs/Custom-Form-Triggers.md)

4. [Posting Feedback In Slack](docs/Slack-Feedback.md)
