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
