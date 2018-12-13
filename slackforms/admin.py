import re
import uuid
from .models import Form, Token
from django.contrib import admin
from django import forms
from slackforms.utils.schema_to_form import (
    SELECT_EXTERNAL_SOURCES,
    TEXT_INPUTS,
)


url_pattern = (
    r"(?i)\b(?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.]"
    r"[a-z]{2,4}/)(?:[^\s()<>\|]+|\([^\s()<>\|]+|\([^\s()<>\|]+\)*\))+(?:\([^"
    r"""\s()<>\|]+|\([^\s()<>\|]+\)*\)|[^\s`!()\[\]{};:'".,<>\|?«»“”‘’])"""
)

CUSTOM_UI_SCHEMA_KEYS = ["submit"]
UI_SCHEMA_WIDGETS = ["text", "textarea", "select"] + TEXT_INPUTS


class FormForm(forms.ModelForm):
    def validate_json_schema(self):
        schema = self.cleaned_data.get("json_schema", {})
        errors = []

        if len(schema.get("required", [1, 2, 3])) == 0:
            errors.append('Remove "required" field if no props are required.')

        props = schema.get("properties", {})

        if len(props.keys()) > 5:
            errors.append("More than five properties included.")

        for prop in props:
            for attr in props[prop]:
                if attr == "source":
                    if props[prop][
                        attr
                    ] not in SELECT_EXTERNAL_SOURCES and not re.match(
                        url_pattern, props[prop][attr]
                    ):
                        errors.append(
                            "%s: source not one of %s or a valid URL."
                            % (prop, SELECT_EXTERNAL_SOURCES)
                        )
                if attr == "enumNames":
                    if len(props[prop]["enum"]) != len(
                        props[prop]["enumNames"]
                    ):
                        errors.append(
                            "%s: length of enum (%s) != enumNames(%s.)"
                            % (
                                prop,
                                props[prop]["enum"],
                                props[prop]["enumNames"],
                            )
                        )

        return None if len(errors) == 0 else errors

    def validate_ui_schema(self):
        schema = self.cleaned_data.get("ui_schema", None)
        if schema is None:
            return None

        json_schema = self.cleaned_data.get("json_schema", {})

        errors = []

        json_props = json_schema.get("properties", {}).keys()
        json_props = json_props if len(json_props) > 0 else None
        for prop in schema:
            if (
                json_props is not None
                and prop not in json_props
                and prop not in CUSTOM_UI_SCHEMA_KEYS
            ):
                errors.append(
                    "%s is not a property in the json schema." % (prop)
                )

            if schema[prop].get("ui:widget", "text") not in UI_SCHEMA_WIDGETS:
                errors.append(
                    "%s ui:widget: %s not one of %s."
                    % (prop, schema[prop].get("ui:widget"), UI_SCHEMA_WIDGETS)
                )

        return None if len(errors) == 0 else errors

    def clean(self):
        json_errors = self.validate_json_schema()
        ui_errors = self.validate_ui_schema()

        errors = {}
        if json_errors is not None:
            errors["json_schema"] = json_errors

        if ui_errors is not None:
            errors["ui_schema"] = ui_errors

        if len(errors.keys()) > 0:
            raise forms.ValidationError(errors)

        return self.cleaned_data

    class Meta:
        model = Form
        fields = [
            "name",
            "json_schema",
            "ui_schema",
            "token",
            "endpoint",
            "data_source",
            "slash_command",
        ]


class FormAdmin(admin.ModelAdmin):
    form = FormForm
    list_display = (
        "name",
        "json_schema",
        "endpoint",
    )


admin.site.register(Form, FormAdmin)


def regenerate_token(modeladmin, request, queryset):
    for token in queryset:
        token.token = uuid.uuid4().hex[:30]
        token.save()


regenerate_token.short_description = 'Regenerate endpoint token'


class TokenAdmin(admin.ModelAdmin):
    list_display = ("name", "token")
    readonly_fields = ('token',)
    actions = (regenerate_token,)


admin.site.register(Token, TokenAdmin)
