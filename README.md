![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-slack-forms

*A utility to handle the creation and processing of Slack Dialogs.*

[Slack Dialogs](https://api.slack.com/dialogs) (forms) are a great and easy way to get data from members of your Slack team. They can be called in a number of ways, they're designed to work on desktop and mobile, and they're already on a familiar platform.

Unfortunately making and sending forms to your users can require an elaborate knowledge of the often-arcane Slack API. Furthermore, validation beyond required fields and character limit has to be handled programmatically by your server which more often than not means you just don't do it.

Django Slack Forms is here to solve these and more hurtles by using a popular [JSON Schema](https://json-schema.org/understanding-json-schema/index.html) to shape and validate your data. New forms can be created in a Django admin with a number of ways to connect it to outside data and webhooks. The app is designed to be as flexible as possible to accommodate your individual data needs and data structures.

At its most basic level, the app works like the flowchart below with you, the developer, being responsible for installation, and all of the optional steps in the third column (labeled `External`). Due to it's flexibility, this app is not plug-and-play, but hopefully this guide will help you install it into your current infrastructure in no time.

In order to get `django-slack-forms` up and running you'll have to complete the following tasks:

1. [Create a Slack App on the Slack API Dashboard.](docs/Slack-App.md)

2. [Install this app into your Django application.](docs/Installation.md)

3. [Create a form in your Django admin.](docs/Creating-Forms.md)

4. [Configure an endpoint to receive your form data.](docs/Configuring-An-Endpoint.md)

Once you have the basics down, you can move on to more advanced topics like:

1. [Configure external source data.](docs/Configuring-Source-Data.md)

2. [Integrate with a REST API.](docs/Integrating-An-API.md)

3. [Set up custom form triggers.](docs/Custom-Form-Triggers.md)

4. [Post feedback to Slack channels.](docs/Slack-Feedback.md)

If you're already familiar with this app and you're looking for a quick reminder check out the [Quick Reference](docs/Quick-Reference.md) guide.

If you're looking to develop this app you can check out the [development docs](docs/Developing-This-App.md).

***

*How `django-slack-forms` works...*

![Flowchart](/docs/media/forms5.jpg)
