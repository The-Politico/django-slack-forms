# Integrating A REST API

*Note: This is an advanced section. It's expected that you have an understanding of the app outlined in the basic sections of these docs before reading this page.*

`django-slack-forms` was designed to easily hook into REST APIs to manage the flow of data. In order to take advantage of this feature, you'll need to configure your API to handle the following kinds of requests:

  - POST requests to add new records
  - GET requests to return records
  - PUT requests to update existing records

This guide will assume you already know the basics of creating an API in your stack of choice and handling requests appropriately. Explaining the complexities of the REST system is beyond the scope of these docs.

As an example, these docs will use a standard Django View located at `https://example.com/api/` to handle these three kinds of requests, but you can use any stack you'd like. For a fully functioning example API check out the [Test API](../example/testapi/) in this repo's example directory.

## POST

POST requests to your API should be treated as requests to create new records in the database. Your form should set it's `Webhook` field to this API endpoint. It will receive the endpoint payload (see [Configuring An Endpoint](Configuring-An-Endpoint.md)) and should verify the request and add the record accordingly.

#### Example

Consider a Django application that handles support tickets. A POST request to the URL `https://example.com/api/ticket/` should add a new ticket to the database.

```python
from django.http import HttpResponse
from django.views import View
from django.conf import settings

from myapp.models import Ticket

class TicketAPI(View):
    def post(self, request):
        # process the request data
        data = request.POST.copy()
        meta = json.loads(data.pop("slackform_meta_data"))
        token = meta["token"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Ticket()
        if "field1" in request_data:
            t.field1 = request_data["field1"]

        if "field2" in request_data:
            t.field2 = request_data["field2"]

        if "field3" in request_data:
            t.field3 = request_data["field3"]
        t.save()

        return HttpResponse(status=200)
```

## GET

Once your database has records in it, you might want to edit them. In order to do that properly, your form will need to be pre-filled with the data from your database. This is done by sending a GET request to your form's `Data source` (set in the Django admin) if an ID was provided to your form trigger. You can read more about where IDs come from in [Custom Form Triggers](Custom-Form-Triggers.md).

GET requests to your API should return the data for a record with a particular ID. Your form's `Data source` field should be set to this endpoint.

In order to handle API's with both direct path endpoint and query parameter endpoint (`https://example.com/api/[MODEL]/[ID]/` vs `https://example.com/api/[MODEL]/?id=[ID]`), `Data source` can actually be provided with a Python template string which receives `id` as an argument. If your API endpoint takes the form of `https://example.com/api/[MODEL]/[ID]/` then your `Data source` value for a model named `ticket` should be `https://example.com/api/ticket/{id}/`.

#### IMPORTANT
If no record exists in your database your API should return a 404 response in plain text with an error message. This error will be passed to your users in Slack if they attempt to trigger an edit form that couldn't retrieve source data.

#### Example

Consider a Django application that handles support tickets. A GET request to the URL  `https://example.com/api/ticket/?id=[ID]/` should return the information for a ticket with the id of `[ID]`.

First, set the `Data source` of the form in the Django admin to:

```python
# Django Admin: Ticket Form: Data Source
"https://example.com/api/ticket/?id={id}/"
```

Then set up your endpoint to accept the ID and return the data if it exists:

```python
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.conf import settings

from myapp.models import Ticket

class TicketAPI(View):
    def get(self, request):
        # process the request data
        id = request.GET.get("id", "")

        # handle the API logic
        try:
          t = Ticket.objects.get(pk=id)
          t_data = model_to_dict(t)
          return JsonResponse(t_data)
        except Ticket.DoesNotExist:
          return HttpResponse("Ticket not found.", status=404)


```

## PUT

PUT requests to your API should be treated as requests to update an existing record in the database. Your form should have it's `Webhook` field set to this API endpoint. It will receive the endpoint payload (see [Configuring An Endpoint](Configuring-An-Endpoint.md)) and should verify the request and update the record accordingly. PUT requests also have the Id of the record that should be updated in the `data_id` property of the `slackform_meta_data` dictionary.

#### Example

Consider a Django application that handles support tickets. A PUT request to the URL `https://example.com/api/ticket/` should update a particular ticket in the database.

```python
from django.http import HttpResponse
from django.views import View
from django.conf import settings

from myapp.models import Ticket

class TicketAPI(View):
    def post(self, request):
        # process the request data
        data = request.POST.copy()
        meta = json.loads(data.pop("slackform_meta_data"))
        token = meta["token"]
        id = meta["data_id"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Ticket.objects.get(pk=id)
        if "field1" in request_data:
            t.field1 = request_data["field1"]

        if "field2" in request_data:
            t.field2 = request_data["field2"]

        if "field3" in request_data:
            t.field3 = request_data["field3"]
        t.save()

        return HttpResponse(status=200)
```

## DELETE

DELETE requests to your API should be treated as requests to delete an existing record in the database. Your form should have it's `Webhook` field set to this API endpoint. It will receive the endpoint payload with only a `slackform_meta_data` property (see [Configuring An Endpoint](Configuring-An-Endpoint.md)) and should verify the request and delete the record accordingly. DELETE requests have the Id of the record that should be deleted in the `data_id` property of the `slackform_meta_data` dictionary.

#### Example

Consider a Django application that handles support tickets. A DELETE request to the URL `https://example.com/api/ticket/` should delete a particular ticket in the database.

```python
from django.http import HttpResponse
from django.views import View
from django.conf import settings

from myapp.models import Ticket

class TicketAPI(View):
    def post(self, request):
        # process the request data
        data = request.POST.copy()
        meta = json.loads(data.pop("slackform_meta_data"))
        token = meta["token"]
        id = meta["data_id"]

        # authenticate the request
        if token != settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN:
            return HttpResponse("Invalid auth token.", status=403)

        # handle the API logic
        t = Test.objects.get(pk=data_id)
        t.delete()

        return HttpResponse(status=200)
```
