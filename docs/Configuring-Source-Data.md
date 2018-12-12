# External Source Data

*Note: This is an advanced section. It's expected that you have an understanding of the app outlined in the basic sections of these docs before reading this page.*

It's quite common for dropdown menus to have many options that come from an external source. Maybe a dropdown is to select a member of the senate. Having to shape all 100 names into the `enum` and `enumNames` format described in earlier sections of these docs every time the list changed would be a hassle. Not to mention the troubles of maintaining a JSON Schema that large.

For this reason, `django-slack-forms` comes with a way to connect form inputs to external data sources using the `source` key in options for each property in your JSON Schema's `properties`. It should be set to a valid URL which (upon a GET request) serves an array of JSON objects with at least `value` and `label` fields. Slack also limits this array to only 100 options (which you shouldn't go past for usability anyway).

### Example
Let's take a look at an example for an input with a list of senators.

The first thing you'd have to do is set up a data source. We'll use a JSON file located at `http://example.com/data/senators.json` which looks like this (note that it could be a live API endpoint as well):

```javascript
[
  {
    "label": "Tammy Baldwin (D - WI)",
    "value": "baldwin-tammy"
  },
  {
    "label": "John Barrasso (R - WY)",
    "value": "barrasso-john "
  },
  {
    "label": "Sherrod Brown (D - OH)",
    "value": "brown-sherrod"
  },
  {
    "label": "Maria Cantwell (D - WA)",
    "value": "cantwell-maria "
  },

  ...

]
```

Then you'll need a form which creates the dropdown menu with these senators. In you Django admin you'd set up your JSON Schema and UI Schema like this:

**JSON Schema**

```javascript
{
  "type": "object",
  "title": "Senators",
  "required": [
    "senator"
  ],
  "properties": {
    "senator": {
      "type": "string",
      "title": "Senator",
      "source": "http://example.com/data/senators.json"
    }
  }
}
```

**UI Schema**

```javascript
{
  "senator": {
    "ui:widget": "select"
  }
}
```

Now when your form is called in Slack, there will be a dropdown menu with all 100 senators. If a user picks `Sherrod Brown (D - OH)` and submits the form, the Webhook will receive the following POST request:

```javascript
{
  "slackform_meta_data": " ... ",
  "senator": "brown-sherrod"
}
```

Note that only the value is provided, not the original label.

## Other Dynamic Sources

If your form has something to do with your Slack team, you can also take advantage of Slack's built-in external data sources. Rather than provide a URL as a `source` you can use one of the following strings: `users`, `channels`, `conversations`. To learn more about these dynamic sources you can check out the [official Slack docs](https://api.slack.com/dialogs#dynamic_select_elements).

You can also use Slack's external data source if you care to by providing the value of `external` as your property's `source`. Since one of this app's functions is meant to provide a better alternative to Slack's built in external source system  mention, I only bring it up to say that it's supported and point you to the [official docs](https://api.slack.com/dialogs#dynamic_select_elements) for more.
