from .base import InteractionBase


class MessageHandler(InteractionBase):
    """
    Handler for buttons and dropdown menus. Both come in using the same request
    type, but their arguments are found in different places. Button values are
    found in the "name" of the button while dropdown menus are found in the
    "value" of the first selected option.
    """
    def get_argument_prop(self):
        actions = self.data.get("actions", [{}])

        if len(actions) == 0:
            return ""

        if (
            "selected_options" in actions[0]
            and len(actions[0]["selected_options"]) > 0
        ):
            return actions[0]["selected_options"][0]["value"]

        if "name" in actions[0]:
            return actions[0]["name"]

        return ""
