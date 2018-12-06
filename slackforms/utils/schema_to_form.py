import requests

"""
Default values to fall back on for required fields.
"""
DEFAULTS = {
    "title": "Form",
    "submit_label": "Submit",
    "element": {"label": "Field", "type": "text", "options": []},
    "ui:order": 999999,
}

"""
Input types that are actually subtypes of "text".
"""
TEXT_INPUTS = ["email", "number", "tel", "url"]

"""
Special Slack data sources for dynamic lists.
"""
SELECT_EXTERNAL_SOURCES = ["users", "channels", "conversations"]


def schema_to_form(name, json, ui, data={}):
    """
    Generate a Slack form dictionary from a schema and data.
    """
    form = {
        # title --> title (or default)
        "title": json.get("title", DEFAULTS["title"]),
        # name of form --> callback_id (or default)
        "callback_id": name,
        # ui.submit.value --> submit_label (or default)
        "submit_label": ui.get("submit", {}).get(
            "ui:value", DEFAULTS["submit_label"]
        ),
        # to be filled with prop_to_input
        "elements": [],
    }

    element_count = 0
    for prop in json.get("properties", {}).keys():
        # Limit elements to five, truncate after
        if element_count == 5:
            break
        element_count += 1

        form["elements"].append(
            prop_to_input(
                prop,
                json["properties"][prop],
                ui.get(prop, {}),
                data.get(prop, None),
                json.get("required", []),
            )
        )

    form["elements"] = sorted(
        form["elements"],
        key=lambda k: k["order"] if "order" in k else DEFAULTS["ui:order"]
    )

    return form


def prop_to_input(name, json, ui, data, required):
    """
    Generate a Slack form element dictionary from a schema and data.
    """
    input = {}

    # key of prop --> name
    input["name"] = name

    # order --> order (if exists)
    if "ui:order" in ui:
        input["order"] = ui["ui:order"]

    # title --> label (or default)
    input["label"] = json.get("title", DEFAULTS["element"]["label"])

    # widget --> type (or default)
    input["type"] = ui.get("ui:widget", DEFAULTS["element"]["type"])

    # If widget is a subtype of "text"...
    if input["type"] in TEXT_INPUTS:
        # "text" --> type
        input["type"] = "text"
        # widget --> subtype
        input["subtype"] = ui["ui:widget"]

    # placeholder --> placeholder (if exists)
    if "ui:placeholder" in ui:
        input["placeholder"] = ui["ui:placeholder"]

    # help --> hint (if exists)
    if "ui:help" in ui:
        input["hint"] = ui["ui:help"]

    # data --> value (if exists)
    if data:
        input["value"] = data
    # value --> value (if exists and no data)
    elif "ui:value" in ui:
        input["value"] = ui["ui:value"]

    # If not required, it's optional
    input["optional"] = name not in required

    # Char length validation on applies to text fields in text inputs
    isTextField = json.get("type", "") == "string"
    isTextInput = input["type"] == "text" or input["type"] == "textarea"
    if isTextField and isTextInput:
        # maxLength --> max_length (if exists)
        if "maxLength" in json:
            input["max_length"] = json["maxLength"]

        # minLength --> min_length (if exists)
        if "minLength" in json:
            input["min_length"] = json["minLength"]

    # Creating options array for select inputs
    if input["type"] == "select":
        if "source" in json:
            if json["source"] in SELECT_EXTERNAL_SOURCES:
                # source --> data_source (if a Slack source keyword)
                input["data_source"] = json["source"]
            else:
                # options --> external feed (if URL provided as source)
                r = requests.get(url=json["source"])
                input["options"] = r.json()

        elif "enum" in json:
            # Default labels to value names if no "enunNames"
            names = json["enumNames"] if "enumNames" in json else json["enum"]

            # Create options array out of explicity stated options
            input["options"] = [
                {"value": val, "label": names[idx]}
                for idx, val in enumerate(json["enum"])
            ]
        else:
            # If no "source" or "enum" use default choices
            input["options"] = DEFAULTS["element"]["options"]

    # Handle data overrides...
    if data:
        if isTextInput:
            input["value"] = data
        elif input["type"] == "select":
            pass

    return input
