import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Input:
    """
    A Python class representing an Input block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "input"
        self._block_id = ""
        self._label = ""
        self._element = {}
        self._dispatch_action = False
        self._hint = None
        self._optional = False
        self.block = {
            "type": self._type
        }

    def set_block_id(self, block_id: str) -> Self:
        """
        (Optional) Sets a unique identifier for a block which can be used when receiving an interaction payload to
        identify the source of an action. If not set, will be auto-generated.
        :param block_id: String; max 255 chars, should be unique for each message and each subsequent iteration thereof. If a message is updated, use a new block_id.
        :return: self
        """
        self._block_id = block_id
        self.block["block_id"] = self._block_id
        return self

    def set_label(self, label_text: str) -> Self:
        """
        Sets the label that appears above an input element
        :param label_text: String; max 2,000 chars
        :return: self
        """
        self._label = Text().set_text(label_text)
        self.block["label"] = self._label.json
        return self

    def add_element(self, element) -> Self:
        """
        Used to add one interactive elements to the block
        :param element: A PlainTextInput, Checkboxes, RadioButtons, SelectMenu, MultiSelectMenu, or DatePicker element
        :return: self
        """
        self._element = element.json
        self.block["element"] = self._element
        return self

    def set_dispatch_action(self, value: bool) -> Self:
        """
        (Optional) Indicates whether the use of elements in this block should dispatch a block_actions payload
        :param value: Boolean; defaults to False
        :return: self
        """
        self._dispatch_action = value
        self.block["dispatch_action"] = self._dispatch_action
        return self

    def set_hint(self, hint_text: str) -> Self:
        """
        (Optional) Sets an optional hint that appears below an input element in a lighter grey
        :param hint_text: String; max 2,000 chars
        :return: self
        """
        self._hint = Text().set_text(hint_text)
        self.block["hint"] = self._hint.json
        return self

    def set_optional(self, value: bool) -> Self:
        """
        (Optional) Indicates whether the input element may be empty when a user submits the modal
        :param value: Boolean; defaults to False
        :return: self
        """
        self._optional = value
        self.block["optional"] = self._optional
        return self

