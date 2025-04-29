import sys

from pyblock_builder.objects import ConfirmationDialog

if sys.version_info >= (3, 11):
    from typing import Self, Literal
else:
    from typing_extensions import Self, Literal
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError,
                                              IncorrectValueError)
from pyblock_builder.objects.text import PlainText

@dataclass
class Button:
    """
    Allows users a direct path to performing basic actions.\n
    Can be added to: Section, Actions\n
    Works on: Modal, Message, AppHome
    """
    type: str = Literal["button"]
    action_id: str | None = None
    text: PlainText | None = None
    url: str | None = None
    value: str | None = None
    style: Literal["danger", "primary"] | None = None
    confirm: ConfirmationDialog | None = None
    accessibility_label: str | None = None

    def set_action_id(self, action_id: str) -> Self:
        """
        Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        if not isinstance(action_id, str):
            raise IncorrectTypeError(self, method="set_action_id", compatible_types=str, incompatible_type=action_id)
        if not 1 <= len(action_id) <= 255:
            raise TextLengthError(self, field="action_id", min_length=1, max_length=255)
        self.action_id = action_id
        return  self

    def set_text(self, label_text: PlainText) -> Self:
        """
        Sets the text to be displayed on the button
        :param label_text: PlainText; max 75 chars, may truncate after 30 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 75:
            raise TextLengthError(self, field="text", min_length=1, max_length=75)
        self.text = label_text
        return self

    def set_value(self, value: str) -> Self:
        """
        (Optional) Sets the value to be sent along with the interaction payload
        :param value: String; max 2,000 chars
        :return: self
        """
        if not isinstance(value, str):
            raise IncorrectTypeError(self, method="set_value", compatible_types=str, incompatible_type=value)
        if not 1 <= len(value) <= 2000:
            raise TextLengthError(self, field="value", min_length=1, max_length=2000)
        self.value = value
        return  self

    def set_url(self, url: str) -> Self:
        """
        (Optional) Sets the url to be opened when a user clicks the button
        :param target_url: String; max 3,000 chars, still requires an ack() response to the Slack API
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_url", compatible_types=str, incompatible_type=url)
        if not 1 <= len(url) <= 3000:
            raise TextLengthError(self, field="url", min_length=1, max_length=3000)
        self.url = url
        return  self

    def set_style(self, style: Literal["danger", "primary"]) -> Self:
        """
        (Optional) Sets the style for the button to decorate with alternative visual color schemes. Can alternatively be
        set using the primary() and danger() methods.
        :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
        :return: self
        """
        if style not in ("danger", "primary"):
            raise IncorrectValueError(self, method="set_style", acceptable_values=["danger", "primary"],
                                      unacceptable_value=style)
        self.style = style
        return self

    def set_confirm_dialog(self, confirm_dialog: ConfirmationDialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after a button is clicked.
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
        return self

    def set_accessibility_label(self, label_text: str) -> Self:
        """
        (Optional) Sets a label for longer descriptive text about a button that is read aloud by a screen reader
        instead of the text used in the button label
        :param label_text: String; max 75 chars
        :return: self
        """
        if not isinstance(label_text, str):
            raise IncorrectTypeError(self, method="set_accessibility_label", compatible_types=str, incompatible_type=label_text)
        if not 1 <= len(label_text) <= 75:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=75)
        self.accessibility_label = label_text
        return  self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if self.text is None:
            raise RequiredFieldsError(self, missing_field_names=["text"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {
            "type": self.type,
            "text": json.loads(self.text.build_to_json()),
        }
        if self.action_id:
            data["action_id"] = self.action_id
        if self.url:
            data["url"] = self.url
        if self.value:
            data["value"] = self.value
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.style:
            data["style"] = self.style
        if self.accessibility_label:
            data["accessibility_label"] = self.accessibility_label

        return json.dumps(data)
