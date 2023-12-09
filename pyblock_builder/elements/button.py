import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Button:
    """
    A Python class representing a Button element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "button"
        self._action_id = ""
        self._text = {}
        self._url = None
        self._value = ""
        self._style = None
        self._confirm = None
        self._accessibility_label = None
        self.json = {
            "type": self._type,
            "text": self._text,
            "value": self._value,
            "action_id": self._action_id
        }

    def set_action_id(self, action_id: str) -> Self:
        """
        Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        self._action_id = action_id
        self.json["action_id"] = self._action_id
        return self

    def set_label(self, label_text: str) -> Self:
        """
        (Required) Sets the text to be displayed on the button
        :param label_text: String; max 75 chars, may truncate from 30 chars
        :return: self
        """
        self._text = Text().set_text(label_text)
        self.json["text"] = self._text.json
        return self

    def set_value(self, value: str) -> Self:
        """
        (Optional) Sets the value to be sent along with the interaction payload
        :param value: String; max 2,000 chars
        :return: self
        """
        self._value = value
        self.json["value"] = self._value
        return self

    def set_url(self, target_url: str) -> Self:
        """
        (Optional) Sets the url to be opened when a user clicks the button
        :param target_url: String; max 3,000 chars, still requires an ack() response to the Slack API
        :return: self
        """
        self._url = target_url
        self.json["url"] = self._url
        return self

    def set_style(self, style: str) -> Self:
        """
        (Optional) Sets the style for the button to decorate with alternative visual color schemes. Can alternatively be
        set using the primary() and danger() methods.
        :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
        :return: self
        """
        self._style = style
        self.json["style"] = self._style
        return self

    def primary(self) -> Self:
        """
        (Optional) Sets the style of the button to "primary", decorating it with a green background.
        :return: self
        """
        self._style = "primary"
        self.json["style"] = self._style
        return self

    def danger(self) -> Self:
        """
        (Optional) Sets the style of the button to "danger", decorating it with a red background.
        :return: self
        """
        self._style = "danger"
        self.json["style"] = self._style
        return self

    def set_confirm_dialog(self, confirm_dialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after a button is clicked.
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        self._confirm = confirm_dialog
        self.json["confirm"] = self._confirm.json
        return self

    def set_accessibility_label(self, label_text: str) -> Self:
        """
        (Optional) Sets a label for longer descriptive text about a button that is read aloud by a screen reader
        instead of the text used in the button label
        :param label_text: String; max 75 chars
        :return: self
        """
        self._accessibility_label = label_text
        self.json["accessibility_label"] = self._accessibility_label
        return self
