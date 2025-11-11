import sys
if sys.version_info >= (3, 11):
    from typing import Self, Any, Literal, Sequence
else:
    from typing_extensions import Self, Any, Sequence
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.objects import Text, PlainText, MrkdwnText
from pyblock_builder.elements import (Button, Checkboxes, DatePicker, Image, MultiSelectMenu, OverflowMenu,
                                      RadioButtons, SelectMenu, TimePicker, WorkflowButton, MultiChannelsSelectMenu,
                                      MultiUsersSelectMenu, MultiStaticSelectMenu, MultiConversationsSelectMenu,
                                      StaticSelectMenu, UsersSelectMenu, ChannelsSelectMenu, ConversationsSelectMenu)


@dataclass
class Section:
    """
    Displays text, possibly alongside block elements.\n
    Works on: Modal, Message, AppHome
    Compatible with: Button, Checkboxes, Date picker, Image, Multi-select menus, Overflow menu, Radio button,
    Select menus, Time picker, Workflow buttons
    """
    type: Literal["section"] = "section"
    block_id: str | None = None
    text: Text | None = None
    fields: list[Text] | None = None
    accessory: (Button | Checkboxes | DatePicker | Image | MultiSelectMenu | OverflowMenu | RadioButtons | SelectMenu | TimePicker | WorkflowButton) | None = None
    expands: bool | None = False

    def set_text(self, text: PlainText | MrkdwnText) -> Self:
        """
        (Preferred) Sets the text for the block. Not required if using the set_fields method.
        :param text: a MrkdwnText or PlainText object; must be between 1 and 3,000 characters
        :return: self
        """
        if not isinstance(text, Text):
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
        if not isinstance(block_id, str):
            raise IncorrectTypeError(self, method="set_block_id", compatible_types=str, incompatible_type=block_id)
        if not 1 <= len(block_id) <= 255:
            raise TextLengthError(self, field="block_id", min_length=1, max_length=255)
        self.block_id = block_id
        return self

    def set_fields(self, *fields: PlainText | MrkdwnText | Sequence[PlainText | MrkdwnText]) -> Self:
        """
        Required if self.text not set. Any text included will be rendered in a compact format allowing for 2columns of
        side-by-side text.
        :param fields: one or more Text objects or a list/tuple of Text objects; max of 10 objects, max 2,000 chars per object
        :return: self
        """
        flattened_fields = []
        for field in fields:
            if isinstance(field, (list, tuple)):
                flattened_fields.extend(field)
            else:
                flattened_fields.append(field)

        if not 1 <= len(flattened_fields) <= 10:
            raise ItemLengthError(self, field="fields", min_length=1, max_length=10)

        for field in flattened_fields:
            if not isinstance(field, Text):
                raise IncorrectTypeError(self, method="set_fields", compatible_types=[PlainText, MrkdwnText], incompatible_type=field)
            self.fields.append(field)
        return self

    def add_accessory(self, accessory: Button | Checkboxes | DatePicker | Image | MultiSelectMenu | OverflowMenu |
                                       RadioButtons | SelectMenu | TimePicker | WorkflowButton) -> Self:
        """
        (Optional) Can be used to add an element block to a section.
        :param accessory: One of the available element objects
        :return: Nothing
        """
        compatible_elements = [
            Button, Checkboxes, DatePicker, Image, MultiSelectMenu, OverflowMenu, RadioButtons, SelectMenu, TimePicker,
            WorkflowButton
        ]
        if not isinstance(accessory, tuple(compatible_elements)):
            raise IncorrectTypeError(self, method="add_accessory", compatible_types=compatible_elements, incompatible_type=accessory)
        self.accessory = accessory
        return self

    def expand(self):
        """
        Indicates Whether this section block's text should always expand when rendered. If false or not provided,
        it may be rendered with a 'see more' option to expand and show the full text.
        :return: self
        """
        self.expands = True
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
        if self.expands:
            data["expand"] = self.expands

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Section instance from its JSON representation
        :param json: a JSON representation of a Section block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "block_id" in json.keys() and json["block_id"] is not None:
            self.block_id = json["block_id"]
        if "text" in json.keys() and json["text"] is not None:
            if json["text"]["type"] == "plain_text":
                self.text = PlainText().build_from_json(json["text"])
            else:
                self.text = MrkdwnText().build_from_json(json["text"])
        if "fields" in json.keys() and json["fields"] is not None:
            self.fields = [PlainText().build_from_json(text) if text["type"] == "plain_text" else MrkdwnText().build_from_json(text) for text in json["fields"]]
        if "accessory" in json.keys() and json["accessory"] is not None:
            compatible_types = {
                "button": Button,
                "checkboxes": Checkboxes,
                "datepicker": DatePicker,
                "image": Image,
                "multi_static_select_menu": MultiStaticSelectMenu,
                "multi_users_select_menu": MultiUsersSelectMenu,
                "multi_channels_select_menu": MultiChannelsSelectMenu,
                "multi_conversations_select_menu": MultiConversationsSelectMenu,
                "overflow_menu": OverflowMenu,
                "radio_buttons": RadioButtons,
                "static_select_menu": StaticSelectMenu,
                "users_select_menu": UsersSelectMenu,
                "channels_select_menu": ChannelsSelectMenu,
                "conversations_select_menu": ConversationsSelectMenu,
                "time_picker": TimePicker,
                "workflow_button": WorkflowButton
            }
            self.accessory = compatible_types[json["accessory"]["type"]]().build_from_json(json["accessory"])
        if "expand" in json.keys():
            self.expands = json["expand"]
        return self
