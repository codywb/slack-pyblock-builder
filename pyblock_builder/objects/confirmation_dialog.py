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
    title: PlainText | None = None
    text: PlainText | None = None
    confirm_label: PlainText | None = None
    deny_label: PlainText | None = None
    style: str | None = None

    def set_title(self, title_text: PlainText) -> Self:
        if not isinstance(title_text, PlainText):
            raise IncorrectTypeError(self, method="set_title", compatible_types=PlainText, incompatible_type=title_text)
        if not 1 <= len(title_text.text) <= 100:
            raise TextLengthError(self, field="title_text", min_length=1, max_length=100)
        self.title = title_text
        return self

    def set_text(self, text: PlainText) -> Self:
        if not isinstance(text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=text)
        if not 1 <= len(text.text) <= 300:
            raise TextLengthError(self, field="text", min_length=1, max_length=300)
        self.text = text
        return self

    def set_confirm_label(self, label_text: PlainText) -> Self:
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_confirm_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 30:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=30)
        self.confirm_label = label_text
        return self

    def set_deny_label(self, label_text: PlainText) -> Self:
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_deny_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 30:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=30)
        self.deny_label = label_text
        return self

    def set_style(self, style: Literal["danger", "primary"]) -> Self:
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

# class ConfirmationDialog:
#     """
#     A Python class representing a Confirmation dialog object from the Slack BlockKit UI framework\n
#     """
#
#     def __init__(self):
#         self._title = {}
#         self._text = {}
#         self._confirm_text = {}
#         self._deny_text = {}
#         self._style = None
#         self.json = {
#             "title": self._title,
#             "text": self._text,
#             "confirm": self._confirm_text,
#             "deny": self._deny_text
#         }
#
#     def set_title(self, title_text: str) -> Self:
#         """
#         Sets the title text for the Confirmation dialog
#         :param title_text: String; max 100 chars
#         :return: self
#         """
#         self._title = Text().set_text(title_text)
#         self.json["title"] = self._title.json
#         return self
#
#     def set_text(self, text: str) -> Self:
#         """
#         Sets the explanatory text that appears in the Confirmation dialog
#         :param text: String; max 300 chars
#         :return: self
#         """
#         self._text = Text().set_text(text)
#         self.json["text"]= self._text.json
#         return self
#
#     def set_confirm_label(self, label_text: str) -> Self:
#         """
#         Sets the label for the button that confirms the action
#         :param label_text: String; max 30 chars
#         :return: self
#         """
#         self._confirm_text = Text().set_text(label_text)
#         self.json["confirm"]= self._confirm_text.json
#         return self
#
#     def set_deny_label(self, label_text: str) -> Self:
#         """
#         Sets the label for the button that cancels the action
#         :param label_text: String; max 30 chars
#         :return: self
#         """
#         self._deny_text = Text().set_text(label_text)
#         self.json["deny"] = self._deny_text.json
#         return self
#
#     def set_style(self, style: str) -> Self:
#         """
#         (Optional) Sets the style for the button to decorate with alternative visual color schemes. If unset, defaults
#         to "primary".
#         :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
#         :return: self
#         """
#         self._style = style
#         self.json["style"] = self._style
#         return self
#
#     def primary(self) -> Self:
#         """
#         (Optional) Sets the style of the button to "primary", decorating it with a green background.
#         :return: self
#         """
#         self._style = "primary"
#         self.json["style"] = self._style
#         return self
#
#     def danger(self) -> Self:
#         """
#         (Optional) Sets the style of the button to "danger", decorating it with a red background.
#         :return: self
#         """
#         self._style = "danger"
#         self.json["style"] = self._style
#         return self
