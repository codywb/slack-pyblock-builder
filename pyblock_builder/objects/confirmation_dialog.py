import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal
else:
    from typing_extensions import Self
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError,
                                              IncorrectValueError)
from pyblock_builder.objects.text import PlainText

@dataclass
class ConfirmationDialog:
    """
    Defines a dialog that adds a confirmation step to interactive elements.
    """
    title: PlainText | None = None
    text: PlainText | None = None
    confirm_label: PlainText | None = None
    deny_label: PlainText | None = None
    style: Literal["danger", "primary"] | None = None

    def set_title(self, title_text: PlainText) -> Self:
        """
        Sets the title text for the Confirmation dialog
        :param title_text: String; max 100 chars
        :return: self
        """
        if not isinstance(title_text, PlainText):
            raise IncorrectTypeError(self, method="set_title", compatible_types=PlainText, incompatible_type=title_text)
        if not 1 <= len(title_text.text) <= 100:
            raise TextLengthError(self, field="title_text", min_length=1, max_length=100)
        self.title = title_text
        return self

    def set_text(self, text: PlainText) -> Self:
        """
        Sets the explanatory text that appears in the Confirmation dialog
        :param text: String; max 300 chars
        :return: self
        """
        if not isinstance(text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=text)
        if not 1 <= len(text.text) <= 300:
            raise TextLengthError(self, field="text", min_length=1, max_length=300)
        self.text = text
        return self

    def set_confirm_label(self, label_text: PlainText) -> Self:
        """
        Sets the label for the button that confirms the action
        :param label_text: String; max 30 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_confirm_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 30:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=30)
        self.confirm_label = label_text
        return self

    def set_deny_label(self, label_text: PlainText) -> Self:
        """
        Sets the label for the button that cancels the action
        :param label_text: String; max 30 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_deny_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 30:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=30)
        self.deny_label = label_text
        return self

    def set_style(self, style: Literal["danger", "primary"]) -> Self:
        """
        (Optional) Sets the style for the button to decorate with alternative visual color schemes. If unset, defaults
        to "primary".
        :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
        :return: self
        """
        if style not in ("danger", "primary"):
            raise IncorrectValueError(self, method="set_style", acceptable_values=["danger", "primary"], unacceptable_value=style)
        self.style = style
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if None in (self.title, self.text, self.confirm_label, self.deny_label):
            raise RequiredFieldsError(self, missing_field_names=["title", "text", "confirm_label", "deny_label"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {
            "title": json.loads(self.title.build_to_json()),
            "text": json.loads(self.text.build_to_json()),
            "confirm": json.loads(self.confirm_label.build_to_json()),
            "deny": json.loads(self.deny_label.build_to_json()),
        }
        if self.style:
            data["style"] = self.style

        return json.dumps(data)