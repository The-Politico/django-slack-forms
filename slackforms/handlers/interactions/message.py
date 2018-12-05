from .base import InteractionBase


class MessageHandler(InteractionBase):
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
