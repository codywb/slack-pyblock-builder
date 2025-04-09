import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import TextLengthError, RequiredFieldError, IncorrectTypeError
from pyblock_builder.base_blocks import Element
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText
from pyblock_builder.elements import *


@dataclass
class Section:
    type: str | None = "section"
    block_id: str | None = None
    text: Text | None = None
    fields: list[Text] | None = None
    accessory: Element | None = None

    def set_text(self, text: Text) -> Self:
        if not isinstance(text, (PlainText, MrkdwnText)):
            raise IncorrectTypeError(self, method="set_text", compatible_types=[PlainText, MrkdwnText], incompatible_type=text)
        if not 1 <= len(text.text) <= 3000:
            raise TextLengthError(self, field="text", min_length=1, max_length=3000)
        self.text = text
        return self

    def set_block_id(self, block_id: str) -> Self:
        if not 1 <= len(block_id) <= 255:
            raise TextLengthError(self, field="block_id", min_length=1, max_length=255)
        self.block_id = block_id
        return self

    def set_fields(self, fields: list[Text]) -> Self:
        if not isinstance(fields, list):
            raise IncorrectTypeError(self, method="set_fields", compatible_types=list, incompatible_type=fields)
        for field in fields:
            if not isinstance(field, (PlainText, MrkdwnText)):
                raise TypeError(f"All items in list of fields provided to {self.__class__.__name__} object must be PlainText or MrkdwnText objects")
        self.fields = fields
        return self

    def add_accessory(self, accessory: Element) -> Self:
        # if isinstance(accessory, DatetimePicker | EmailInput | NumberInput | PlainTextInput | UrlInput):
        compatible_elements = [
            Button, Checkboxes, DatePicker, Image, MultiUsersSelect, MultiStaticSelect, MultiChannelsSelect,
            MultiConversationsSelect, OverflowMenu, RadioButtons, StaticSelectMenu, ChannelsSelectMenu,
            ConversationsSelectMenu, UsersSelectMenu
        ]
        for element in compatible_elements:
            if not isinstance(type(accessory), element):
                raise IncorrectTypeError(self, method="add_accessory", compatible_types=compatible_elements, incompatible_type=accessory)
        self.accessory = accessory
        return self

    def build_to_json(self):
        # raise error if neither text nor fields are set
        if not any([self.fields, self.text]):
            raise RequiredFieldError(self, missing_field_names=["text", "fields"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {
            "type": self.type,
        }
        if self.text:
            data["text"] = json.loads(self.text.build_to_json())
        if self.block_id:
            data["block_id"] = self.block_id
        if self.fields:
            data["fields"] = [json.loads(text_obj.build_to_json()) for text_obj in self.fields]
        if self.accessory:
            data["accessory"] = json.loads(self.accessory.build_to_json())

        return json.dumps(data)

# class Section:
#     """
#     A Python class representing a Section block from the Slack BlockKit UI framework\n
#     Works on: Modal, Message, AppHome
#     """
#     def __init__(self):
#         self._type = "section"
#         self._block_id = ""
#         self._text = ""
#         self._fields = None
#         self._accessory = None
#         self.block = {
#             "type": self._type
#         }
#
#     def set_block_id(self, block_id: str) -> Self:
#         """
#         (Optional) Sets a unique identifier for a block which can be used when receiving an interaction payload to
#         identify the source of an action. If not set, will be auto-generated.
#         :param block_id: String; max 255 chars, should be unique for each message and each subsequent iteration thereof. If a message is updated, use a new block_id.
#         :return: self
#         """
#         self._block_id = block_id
#         self.block["block_id"] = self._block_id
#         return self
#
#     def set_text(self, text, mrkdwn=True) -> Self:
#         """
#         (Preferred) Sets the text for the block. Not required if a list of fields objects is provided.
#         :param text: String or Text object; max 3,000 chars
#         :param mrkdwn: Boolean; defaults to True
#         :return: self
#         """
#         if not mrkdwn:
#             if not isinstance(text, str):
#                 self._text = text
#             else:
#                 self._text = Text().set_text(text)
#         else:
#             if not isinstance(text, str):
#                 if text._type == "mrkdwn":
#                     self._text = text
#                 else:
#                     self._text = text.as_mrkdwn()
#             else:
#                 self._text = Text().set_text(text).as_mrkdwn()
#         self.block["text"] = self._text.json
#         return self
#
#     def set_fields(self, fields_obj) -> Self:
#         """
#         (Maybe) Required if self.text not set. Any text included will be rendered in a compact format allowing for 2
#         columns of side-by-side text.
#         :param fields_obj: Fields object; max number of fields is 10, max chars per field is 2,000
#         :return: self
#         """
#         self._fields = fields_obj.fields
#         self.block["fields"] = self._fields
#         return self
#
#     def add_accessory(self, accessory) -> Self:
#         """
#         (Optional) Can be used to add an element block to a section.
#         :param accessory: One of the available element objects
#         :return: Nothing
#         """
#         self._accessory = accessory
#         self.block["accessory"] = self._accessory.json
#         return self
