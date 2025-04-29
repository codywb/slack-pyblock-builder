import sys
if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import TextLengthError, RequiredFieldError, IncorrectTypeError
from pyblock_builder.base_blocks import Element
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText
from pyblock_builder.elements import *


@dataclass
class Section:
    """
    Displays text, possibly alongside block elements.\n
    A section can be used as a text block, in combination with text fields, or side-by-side with certain block elements.\n
    Works on: Modal, Message, AppHome
    """
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
        """
        (Optional) Sets a unique identifier for a block which can be used when receiving an interaction payload to
        identify the source of an action. If not set, will be auto-generated.
        :param block_id: String; max 255 chars, should be unique for each message and each subsequent iteration thereof.
         If a message is updated, use a new block_id.
        :return: self
        """
        if not 1 <= len(block_id) <= 255:
            raise TextLengthError(self, field="block_id", min_length=1, max_length=255)
        self.block_id = block_id
        return self

    def set_fields(self, fields: list[Text]) -> Self:
        """
        Required if self.text not set. Any text included will be rendered in a compact format allowing for 2
        columns of side-by-side text.
        :param fields: List of Text objects; max number of fields is 10, max chars per field is 2,000
        :return: self
        """
        if not isinstance(fields, list):
            raise IncorrectTypeError(self, method="set_fields", compatible_types=list, incompatible_type=fields)
        for field in fields:
            if not isinstance(field, (PlainText, MrkdwnText)):
                raise TypeError(f"All items in list of fields provided to {self.__class__.__name__} object must be PlainText or MrkdwnText objects")
        self.fields = fields
        return self

    def add_accessory(self, accessory: Element) -> Self:
        """
        (Optional) Can be used to add an element block to a section.
        :param accessory: One of the available element objects
        :return: Nothing
        """
        compatible_elements = [
            Button, Checkboxes, DatePicker, Image, MultiUsersSelect, MultiStaticSelect, MultiChannelsSelect,
            MultiConversationsSelect, OverflowMenu, RadioButtons, StaticSelectMenu, ChannelsSelectMenu,
            ConversationsSelectMenu, UsersSelectMenu
        ]
        if type(accessory) not in compatible_elements:
            raise IncorrectTypeError(self, method="add_accessory", compatible_types=compatible_elements, incompatible_type=accessory)
        self.accessory = accessory
        return self

    def build_to_json(self):
        # raise error if neither text nor fields are set
        if not any([self.fields, self.text]):
            raise RequiredFieldError(self, missing_field_names=["text", "fields"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
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
