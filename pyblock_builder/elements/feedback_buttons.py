import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError)
from pyblock_builder.objects.text import PlainText

@dataclass
class FeedbackButtons:
    """
    Defines buttons to indicate positive and negative feedback.\n
    Can be added to: ContextActions\n
    Works on: Message
    """
    type: Literal["feedback_buttons"] = "feedback_buttons"
    action_id: str | None = None
    positive_button: dict[Literal["text", "value", "accessibility_label"], PlainText | str] | None = None
    negative_button: dict[Literal["text", "value", "accessibility_label"], PlainText | str] | None = None

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

    def set_positive_button(self, text: PlainText, value: str, accessibility_label: str = None) -> Self:
        """
        Defines a button to indicate positive feedback.
        :param text: PlainText object; max 75 characters
        :param value: str; max 2,000 characters
        :param accessibility_label: str; max 75 characters
        :return: self
        """
        if text:
            if not isinstance(text, PlainText):
                raise IncorrectTypeError(self, method="set_positive_button", compatible_types=PlainText, incompatible_type=text)
            if not 1 <= len(text.text) <= 75:
                raise TextLengthError(self, field="text", min_length=1, max_length=75)
        if value:
            if not isinstance(value, str):
                raise IncorrectTypeError(self, method="set_positive_button", compatible_types=str, incompatible_type=value)
            if not 1 <= len(value) <= 75:
                raise TextLengthError(self, field="value", min_length=1, max_length=2000)
        self.positive_button = {
            "text": json.loads(text.build_to_json()),
            "value": value,
        }
        if accessibility_label:
            if not isinstance(accessibility_label, str):
                raise IncorrectTypeError(self, method="set_positive_button", compatible_types=str, incompatible_type=accessibility_label)
            if not 1 <= len(accessibility_label) <= 75:
                raise TextLengthError(self, field="accessibility_label", min_length=1, max_length=75)
            self.positive_button["accessibility_label"] = accessibility_label

        return self

    def set_negative_button(self, text: PlainText, value: str, accessibility_label: str = None) -> Self:
        """
        Defines a button to indicate negative feedback.
        :param text: PlainText object; max 75 characters
        :param value: str; max 2,000 characters
        :param accessibility_label: str; max 75 characters
        :return: self
        """
        if text:
            if not isinstance(text, PlainText):
                raise IncorrectTypeError(self, method="set_negative_button", compatible_types=PlainText, incompatible_type=text)
            if not 1 <= len(text.text) <= 75:
                raise TextLengthError(self, field="text", min_length=1, max_length=75)
        if value:
            if not isinstance(value, str):
                raise IncorrectTypeError(self, method="set_negative_button", compatible_types=str, incompatible_type=value)
            if not 1 <= len(value) <= 75:
                raise TextLengthError(self, field="value", min_length=1, max_length=2000)
        self.negative_button = {
            "text": json.loads(text.build_to_json()),
            "value": value,
        }
        if accessibility_label:
            if not isinstance(accessibility_label, str):
                raise IncorrectTypeError(self, method="set_negative_button", compatible_types=str, incompatible_type=accessibility_label)
            if not 1 <= len(accessibility_label) <= 75:
                raise TextLengthError(self, field="accessibility_label", min_length=1, max_length=75)
            self.negative_button["accessibility_label"] = accessibility_label

        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.positive_button, self.negative_button]]):
            raise RequiredFieldsError(self, missing_field_names=["positive_button", "negative_button"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "positive_button": self.positive_button,
            "negative_button": self.negative_button
        }
        if self.action_id:
            data["action_id"] = self.action_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a FeedbackButtons instance from its JSON representation
        :param json: a JSON representation of a FeedbackButtons element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.positive_button = json["positive_button"]
        self.negative_button = json["negative_button"]
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        return self
