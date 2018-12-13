# Posting Feedback In Slack

*Note: This is an advanced section. It's expected that you have an understanding of the app outlined in the basic sections of these docs before reading this page.*

Once your endpoint receives data and processes it accordingly, you may want to post a message in Slack to confirm it's success or indicate it's failure.

`django-slack-forms` handles posting messages like it does most things: through endpoints. It includes two different endpoints located at `/callback/` and `/message/` (relative to the root of the app) which offer variable levels of flexibility and therefore complexity.

## Posting Callback Messages (`/callback/`)
In the meta data for the request payload sent to your endpoint is a URL under the key of `response_url`. You can send it a POST request to post a message in Slack. The metadata also comes with information about the channel the form was filled out in and the user who filled it out. This can be useful for creating a rich feedback message.

The POST request for this endpoint should include the following properties:

| Property      | Description                                          | Required                     |
| ------------- | ---------------------------------------------------- | ---------------------------- |
| `token`       | The token registered in the Django admin             | Yes                          |
| `channel`     | The channel to post the message in (ID or name)      | Yes                          |
| `text`        | The main text of the message                         | No                           |
| `attachments` | A list of [Slack attachments](https://api.slack.com/docs/message-attachments) to include                        | No                           |
| `new`         | The text of a button to trigger a new form*          | No                           |
| `edit`        | The text of a button to edit a record via form*      | No                           |
| `delete`      | The text of a button to delete a record via form*    | No                           |
| `data_id`     | The ID of the record to edit/delete                  | If `edit` or `delete`        |
| `form`        | The unique `name` of the form to trigger a change in | If `new`, `edit` or `delete` |

<em>* New, edit, and delete buttons will only appear if a value is provided.</em>

#### Example

Consider the Django application that handles support tickets created in [Integrating A REST API](Integrating-An-API.md). When a new instance has been saved, a message should appear in Slack with the ability to edit and delete it.

For a quick refresher take a look at the metadata sent to this endpoint (remember this is a stringified dictionary found in the request data's `slackform_meta_data` key.). Some of this might be useful for creating a rich feedback message.

```javascript
{
  "token": "3829AGBWI1923H2N194"
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
  "form": "Ticket" // the unique name of the form that was filled out
}
```


```python
# imports....

from django.conf import settings

class TicketAPI(View):
    def post(self, request):
        # process the request data...

        # authenticate the request...

        # handle the API logic...
        # t is created to represent the new object


        # process metadata
        meta_data = request.POST.get("slackform_meta_data")
        meta = json.loads(meta_data)
        response_url = meta["response_url"]
        username = meta["user"]["name"]
        channel = meta["channel"]["name"]
        form = meta["form"]
        token = meta["token"]


        # create feedback message
        callback_data = {
            "token": ENDPOINT_TOKEN,
            "channel": channel,
            "data_id": t.pk,
            "form": form,
            "text": "`{}` created a new `{}` entry: {}(`{}`).".format(  # brizandrew created a new Ticket entry: Bug Report(3)
                username, form, t.name, t.pk
            ),
            "delete": "Delete",
            "edit": "Edit",
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)
```

## Posting Custom Messages (`/messages/`)

This endpoint is the most flexible and once verified will simply post a message. For more on creating messages you can check out [the official Slack docs](https://api.slack.com/docs/messages) and use their [message builder utility](https://api.slack.com/docs/messages/builder).

The message data must be a stringified dictionary that is sent through with the POST request under the key of `payload`. You must also send the Slack verification token for your app or a registered token. That request should look like this:

```javascript
{
  "token": "S3C639pZqXvR2toPwcng",
  "payload": "{ ... }"
}
```
