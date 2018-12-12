import json
from .base import InteractionBase


class MessageHandler(InteractionBase):
    """
    Handler for buttons and dropdown menus. Both come in using the same request
    type, but their arguments are found in different places. Button values are
    found in the "name" of the button while dropdown menus are found in the
    "value" of the first selected option.
    """

    def menuOrButton(self, actions):
        if "selected_options" in actions[0]:
            return "menu"
        elif "name" in actions[0]:
            return "button"
        else:
            return None

    def get_method(self):
        default = super().get_method()
        actions = self.data.get("actions", [{}])

        if len(actions) == 0:
            return default

        value = {}
        if self.menuOrButton(actions) == "menu":
            value = json.loads(actions[0]["selected_options"][0]["value"])
        elif self.menuOrButton(actions) == "button":
            value = json.loads(actions[0]["value"])

        return value.get("method", default)

    def get_id(self):
        default = super().get_id()
        actions = self.data.get("actions", [{}])

        if len(actions) == 0:
            return default

        value = {}
        if self.menuOrButton(actions) == "menu":
            value = json.loads(actions[0]["selected_options"][0]["value"])
        elif self.menuOrButton(actions) == "button":
            value = json.loads(actions[0]["value"])

        return value.get("data_id", default)
