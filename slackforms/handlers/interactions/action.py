from .base import InteractionBase


class ActionHandler(InteractionBase):
    def get_argument_prop(self):
        return self.data.get("message", {}).get("text", "")
