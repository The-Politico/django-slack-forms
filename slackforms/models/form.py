import dateparser
import re
import requests
import json
import os
from django.db import models
from django.contrib.postgres.fields import JSONField
from jsonschema import validate, exceptions
from ..utils import schema_to_form, slack, is_float
from ..conf import Settings


class Form(models.Model):
    """
    A form to be displayed on Slack and will send a validated input to a
    specific endpoint.
    """

    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="The unique name of this form to serve as a unique key.",
    )
    webhook = models.URLField(
        blank=True,
        help_text="A URL to hit with the processed and validated form data.",
    )

    json_schema = JSONField(
        null=True, help_text="A schema for the form data. See docs."
    )
    ui_schema = JSONField(
        null=True, help_text="A schema for the form inputs. See docs."
    )
    data_source = models.URLField(
        blank=True,
        help_text="""
The source of data if an Id is supplied. Variable is passed through to
this template. Use "{id}" to crate the template.
""",
    )

    slash_command = models.CharField(
        max_length=40,
        unique=True,
        blank=True,
        null=True,
        help_text="The slash command for this form (don't include the slash).",
    )

    def __str__(self):
        return self.name

    def get_resonse_url(self):
        """
        Get the proper response_url callback for webhook request data.
        """
        return os.path.join(Settings.ROOT_URL, "callback/")

    def get_prop_attr(self, prop, attr):
        """
        Get a particular attribute of a particular form property.
        """
        return (
            self.json_schema.get("properties", {}).get(prop, {}).get(attr, "")
        )

    def is_prop_number(self, prop):
        """
        Get whether a property is of a number type.
        """
        return self.get_prop_attr(prop, "type") in ["number", "integer"]

    def get_form_data(self, id):
        """
        Get starting data from the form's data_source given a particular id.
        """
        if self.data_source or id == "":
            url = self.data_source.format(id=id)
            r = requests.get(url=url)
            return r.json()
        else:
            return {}

    def process(self, content):
        """
        Process data from a Slack form.
        """
        output = {}
        for prop, value in content.items():
            if value is not None:
                if self.is_prop_number(prop) and is_float(value):
                    output[prop] = int(value)
                elif isinstance(value, float):
                    output[prop] = float(value)
                elif self.get_prop_attr(prop, "format") == "date-time":
                    try:
                        date = dateparser.parse(value).isoformat()
                    except AttributeError:
                        date = ""
                    output[prop] = date
                else:
                    output[prop] = value

        return output

    def validate(self, content):
        """
        Validate form data based on a form's json schema and return errors
        in a Slack-friendly structure.
        """
        try:
            validate(content, self.json_schema)
        except exceptions.ValidationError as e:
            errorObj = {"name": "".join(e.path), "error": e.message}
            if errorObj["name"] == "":
                m = re.search("'(.*)' is a required property", e.message)
                errorObj["name"] = m.group(1)
            return errorObj

        return True

    def create_slack_form(self, data, data_id):
        """
        Create a Slack form dictionary from the record's json and ui schemas.
        """
        form = schema_to_form(
            self.name, self.json_schema, self.ui_schema, data
        )
        if data_id and not data_id == "":
            form["state"] = data_id

        return form

    def post_to_slack(self, trigger_id, data_id="", data={}):
        """
        Given starting data and/or an Id to get data from a data_source,
        trigger a new form to open in Slack.
        """
        source_data = self.get_form_data(data_id)
        form_data = {**source_data, **data}  # noqa: E999
        form = self.create_slack_form(form_data, data_id=data_id)
        slack("dialog.open", dialog=form, trigger_id=trigger_id)

    def post_to_webhook(self, processed_content, meta={}):
        """
        Send processed form data (along with some metadata) to the form's
        designated webhook.
        """
        data = processed_content
        meta_data = meta
        meta_data["response_url"] = self.get_resonse_url()
        meta_data["form_name"] = self.name
        data["slackform_meta_data"] = json.dumps(meta_data)
        if not self.webhook == "":
            if meta["data_id"] is None:
                requests.post(url=self.webhook, data=data)
            else:
                requests.put(url=self.webhook, data=data)
