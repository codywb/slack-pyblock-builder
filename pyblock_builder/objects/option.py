import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from dataclasses import dataclass
import json
from _errors import FieldLengthError, RequiredFieldError
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText


@dataclass
class Option:
    _text: Text | None = None
    _value: str | None = None
    _description: Text | None = None
    _url: str | None = None

    def set_text(self, text: Text) -> Self:
        if not isinstance(text, (PlainText, MrkdwnText)):
            raise TypeError(f"text must be a PlainText or MrkdwnText object, not {type(text).__name__}")
        if not 1 <= len(text._text) <= 75:
            raise FieldLengthError(self, "text", min_length=1, max_length=75)
        self._text = text
        return self

    def set_value(self, value: str) -> Self:
        if not 1 <= len(value) <= 150:
            raise FieldLengthError(self, "value", min_length=1, max_length=150)
        self._value = value
        return self

    def set_url(self, target_url: str) -> Self:
        if not 1 <= len(target_url) <= 3000:
            raise FieldLengthError(self, "url", min_length=1, max_length=3000)
        self._url = target_url
        return self

    def set_description(self, descriptive_text: Text) -> Self:
        if not isinstance(descriptive_text, (PlainText, MrkdwnText)):
            raise TypeError(f"text must be a PlainText or MrkdwnText object, not {type(descriptive_text).__name__}")
        if not 1 <= len(descriptive_text._text) <= 75:
            raise FieldLengthError(self, "description", min_length=1, max_length=75)
        self._description = descriptive_text
        return self

    def build_to_json(self) -> str:
        if self._text is None:
            raise RequiredFieldError(self, "text")
        if self._value is None:
            raise RequiredFieldError(self, "value")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {
            "text": json.loads(self._text.build_to_json()),
            "value": self._value
        }
        if self._description:
            data["description"] = json.loads(self._description.build_to_json())
        if self._url:
            data["url"] = self._url

        return json.dumps(data)

#
# class Option:
#     """
#     A Python class representing an Option object from the Slack BlockKit UI framework
#     """
#     def __init__(self):
#         self._text = {}
#         self._value = ""
#         self._description = None
#         self._url = None
#         self.json = {
#             "text": self._text,
#             "value": self._value
#         }
#
#     def set_text(self, text: str, mrkdwn=False) -> Self:
#         """
#         (Required) Sets the text shown in the option on the menu
#         :param text: String, max 75 chars
#         :param mrkdwn: Boolean; defaults to False -- must be False for Overflow, Select, and Multi-Select Menus, can be True for Radio Buttons and Checkboxes
#         :return: self
#         """
#         if not mrkdwn:
#             self._text = Text().set_text(text)
#         else:
#             self._text = Text().set_text(text).as_mrkdwn()
#         self.json["text"] = self._text.json
#         return self
#
#     def set_value(self, value: str) -> Self:
#         """
#         (Required) Sets the value to be passed to your app when the option is chosen
#         :param value: String; max 75 chars
#         :return: self
#         """
#         self._value = value
#         self.json["value"] = self._value
#         return self
#
#     def set_url(self, target_url: str) -> Self:
#         """
#         (Optional) Sets the url to be opened when a user clicks the option. Only available in overflow menus!
#         :param target_url: String; max 3,000 chars, still requires an ack() response to the Slack API
#         :return: self
#         """
#         self._url = target_url
#         self.json["url"] = self._url
#         return self
#
#     def set_description(self, descriptive_text: str) -> Self:
#         """
#         (Optional) Sets the text to be shown below the Option's text beside a radio button
#         :param descriptive_text: String; max 75 chars
#         :return: self
#         """
#         self._description = Text().set_text(descriptive_text)
#         self.json["description"] = self._description.json
#         return self
