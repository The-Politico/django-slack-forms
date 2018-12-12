### A Complete Example

For a complete example of what you're responsible for developing outside this app look at the [`exampleapp`](/example/exampleapp) directory. A form configuration exists in [`fixtures.json`](/example/exampleapp/fixtures.json) which can be loaded into your database as an example.

In its views you'll see an [`API`](/example/exampleapp/views/api.py) view which serves as the form's webhook and data source (providing data via GET, creating entries via POST, and updating those entries via PUT).

You'll also see that the `API` sends a POST request to the `response_url` provided with a feedback message meant to be sent to a pre-designated feedback channel (see [Line 12](/example/exampleapp/views/api.py#L12)).

You can also find examples of an endpoint with options for a select field in the [`TestOptions`](/example/exampleapp/views/test_options.py) view and of a manual form trigger via POST request in the [`TestManual`](/example/exampleapp/views/test_manual.py) view.
