import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.elements import (Button, Checkboxes, DatePicker, DatetimePicker, MultiSelectMenu, SelectMenu,
                                      RadioButtons, RichTextInput, TimePicker, OverflowMenu, WorkflowButton,
                                      MultiChannelsSelectMenu, MultiConversationsSelectMenu, MultiStaticSelectMenu,
                                      MultiUsersSelectMenu, ChannelsSelectMenu, StaticSelectMenu, UsersSelectMenu,
                                      ConversationsSelectMenu)

@dataclass
class Actions:
    """
    Holds multiple interactive elements.
    Works on: Modal, Message, AppHome
    Compatible with: Button, Checkboxes, Date picker, Datetime picker, Multi-select menus, Overflow menu, Radio button,
    Rich text input, Select menus, Time picker, Workflow buttons
    """
    type: Literal["actions"] = "actions"
    block_id: str | None = None
    elements: list[Button | Checkboxes | DatePicker | DatetimePicker | MultiSelectMenu | SelectMenu |
                   OverflowMenu | RadioButtons | RichTextInput | TimePicker | WorkflowButton] = field(default_factory=list)

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

    def add_elements(self, *elements: Button | Checkboxes | DatePicker | DatetimePicker | MultiSelectMenu |
                                      SelectMenu | OverflowMenu | RadioButtons | RichTextInput | TimePicker | WorkflowButton |
                                      Sequence[Button | Checkboxes | DatePicker | DatetimePicker | MultiSelectMenu |
                                               SelectMenu | OverflowMenu | RadioButtons | RichTextInput |
                                               TimePicker | WorkflowButton]) -> Self:
        """
        Used to add one or more interactive elements to the block.
        :param elements: One or more element objects (buttons, select menus, overflow menus, date pickers, etc.);
        maximum of 25 elements per block
        :return: self
        """
        compatible_elements = [Button, Checkboxes, DatePicker, DatetimePicker, MultiSelectMenu, SelectMenu,
                               OverflowMenu, RadioButtons, RichTextInput, TimePicker, WorkflowButton]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        if not 1 <= len(flattened_elements) <= 25:
            raise ItemLengthError(self, field="elements", min_length=1, max_length=25)

        for element in flattened_elements:
            if not isinstance(element, tuple(compatible_elements)):
                raise IncorrectTypeError(self, method="add_elements", compatible_types=compatible_elements, incompatible_type=element)
            self.elements.append(element)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.elements:
            raise RequiredFieldError(self, missing_field_names="elements")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "elements": [json.loads(element.build_to_json()) for element in self.elements],
        }
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates an Actions instance from its JSON representation
        :param json: a JSON representation of an Actions block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "block_id" in json.keys() and json["block_id"] is not None:
            self.block_id = json["block_id"]
        compatible_types = {
            "button": Button,
            "checkboxes": Checkboxes,
            "datepicker": DatePicker,
            "datetimepicker": DatetimePicker,
            "multi_static_select": MultiStaticSelectMenu,
            "multi_users_select": MultiUsersSelectMenu,
            "multi_channels_select": MultiChannelsSelectMenu,
            "multi_conversations_select": MultiConversationsSelectMenu,
            "static_select": StaticSelectMenu,
            "users_select": UsersSelectMenu,
            "channels_select": ChannelsSelectMenu,
            "conversations_select": ConversationsSelectMenu,
            "overflow_menu": OverflowMenu,
            "radio_buttons": RadioButtons,
            "rich_text_input": RichTextInput,
            "time_picker": TimePicker,
            "workflow_button": WorkflowButton
        }
        self.elements = [compatible_types[element["type"]]().build_from_json(element) for element in json["elements"]]
        return self
