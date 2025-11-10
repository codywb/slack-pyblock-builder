import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError)
from pyblock_builder.objects.text import PlainText
from pyblock_builder.objects import ConfirmationDialog

@dataclass
class IconButton:
    """
    Defines an icon button to perform actions.\n
    Can be added to: ContextActions\n
    Works on: Message
    """
    type: Literal["icon_button"] = "icon_button"
    icon: str | None = None
    text: PlainText | None = None
    action_id: str | None = None
    value: str | None = None
    confirm: ConfirmationDialog | None = None
    accessibility_label: str | None = None
    visible_to_user_ids: list[str] | None = None

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

    def set_icon(self, icon: str) -> Self:
        """
        Sets the name of the icon to display on the button
        :param icon: String; e.g. "trash"
        :return: self
        """
        if not isinstance(icon, str):
            raise IncorrectTypeError(self, method="set_icon", compatible_types=str, incompatible_type=icon)
        self.icon = icon
        return  self

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

    def visible_to(self, user_ids: list[str] | str) -> Self:
        """
        Specifies the ids of users to whom the icon button is visible. If not used, the button is visible to all users.
        :param user_ids: List of valid public Slack user IDs as strings
        :return: self
        """
        if not isinstance(user_ids, list):
            raise IncorrectTypeError(self, method="visible_to", compatible_types=list[str], incompatible_type=user_ids)
        if isinstance(user_ids, list):
            for user_id in user_ids:
                if not isinstance(user_id, str):
                    raise TypeError("Non-string value included in user_ids list passed as argument to the 'visible_to' method of IconButton")
        self.visible_to_user_ids = user_ids
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.text, self.icon]]):
            raise RequiredFieldsError(self, missing_field_names=["text", "icon"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "text": json.loads(self.text.build_to_json()),
            "icon": self.icon
        }
        if self.action_id:
            data["action_id"] = self.action_id
        if self.visible_to_user_ids:
            data["visible_to_user_ids"] = self.visible_to_user_ids
        if self.value:
            data["value"] = self.value
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.accessibility_label:
            data["accessibility_label"] = self.accessibility_label

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a IconButton instance from its JSON representation
        :param json: a JSON representation of a IconButton element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.text = PlainText().build_from_json(json["text"])
        self.icon = json["icon"]
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "visible_to_user_ids" in json.keys() and json["visible_to_user_ids"] is not None:
            self.visible_to_user_ids = json["visible_to_user_ids"]
        if "accessibility_label" in json.keys() and json["accessibility_label"] is not None:
            self.accessibility_label = json["accessibility_label"]
        if "value" in json.keys() and json["value"] is not None:
            self.value = json["value"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self