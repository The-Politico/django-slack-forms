from .base import InteractionBase


class ActionHandler(InteractionBase):
    """
    Handler for message actions. The argument prop is found in the data's
    "text" property.
    """
    def get_argument_prop(self):
        return self.data.get("message", {}).get("text", "")
