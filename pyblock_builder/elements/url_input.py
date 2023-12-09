import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class UrlInput:
    """
    A Python class representing a URL Input element from the Slack BlockKit UI framework\n
    Can be added to: Input
    Works on: Modal
    """
    def __init__(self):
        self._type = "url_text_input"
        self._action_id = ""
        self._initial_value = ""
        self._dispatch_action_config = None
        self._focus_on_load = False
        self._placeholder = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id
        }

    def set_action_id(self, action_id: str) -> Self:
        """
        (Optional) Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        self._action_id = action_id
        self.json["action_id"] = self._action_id
        return self

    def set_initial_value(self, value: str) -> Self:
        """
        (Optional) Sets the initial value in the URL input when it loads
        :param value: String
        :return: self
        """
        self._initial_value = value
        self.json["initial_value"] = self._initial_value
        return self

    def focus_on_load(self) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self._focus_on_load = True
        self.json["focus_on_load"] = self._focus_on_load
        return self

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        (Optional) Sets the placeholder text shown in the URL input
        :param placeholder_text: String; max 150 chars
        :return: self
        """
        self._placeholder = Text().set_text(placeholder_text)
        self.json["placeholder"] = self._placeholder.json
        return self

    def set_dispatch_action_config(self, config) -> Self:
        """
        (Optional) Determines when during text input the element returns a block_actions payload
        :param config: A DispatchActionConfig object
        :return: self
        """
        self._dispatch_action_config = config
        self.json["dispatch_action_config"] = self._dispatch_action_config.json
        return self

