import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError)
from pyblock_builder.objects import PlainText
from pyblock_builder.elements import (Checkboxes, DatePicker, DateTimePicker, EmailInput, FileInput, MultiSelectMenu,
                                      NumberInput, PlainTextInput, RadioButtons, RichTextInput, SelectMenu, TimePicker,
                                      UrlInput)

@dataclass
class Input:
    """
    Collects information from users via elements.\n
    Works on: Modal, Message, AppHome
    Compatible with: Checkboxes, Date picker, Datetime picker, Email input, File input, Multi-select menus, Number input,
    Plain-text input, Radio button, Rich text input, Select menu, Time picker, URL input
    """
    type: Literal["input"] = "input"
    label: PlainText | None = None
    element: (Checkboxes | DatePicker | DateTimePicker | EmailInput | FileInput | MultiSelectMenu | NumberInput |
              PlainTextInput | RadioButtons | RichTextInput | SelectMenu | TimePicker | UrlInput) | None = None
    dispatches_action: bool | None = False
    block_id: str | None = None
    hint: PlainText | None = None
    is_optional: bool | None = False

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

    def set_label(self, label_text: PlainText) -> Self:
        """
        Sets the label that appears above an input element.
        :param label_text: PlainText; max 2,000 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 2000:
            raise TextLengthError(self, field="label", min_length=1, max_length=2000)
        self.label = label_text
        return self

    def add_element(self, element: Checkboxes | DatePicker | DateTimePicker | EmailInput | FileInput | MultiSelectMenu | NumberInput |
              PlainTextInput | RadioButtons | RichTextInput | SelectMenu | TimePicker | UrlInput) -> Self:
        """
        Used to add an interactive element to the block
        :param element: One of Checkboxes, DatePicker, DateTimePicker, EmailInput, FileInput, MultiSelectMenu,
        NumberInput. PlainTextInput, RadioButtons, RichTextInput, SelectMenu, TimePicker, UrlInput
        :return: self
        """
        compatible_elements = [Checkboxes, DatePicker, DateTimePicker, EmailInput, FileInput, MultiSelectMenu,
                              NumberInput, PlainTextInput, RadioButtons, RichTextInput, SelectMenu, TimePicker,
                              UrlInput]
        if not isinstance(element, tuple(compatible_elements)):
            raise IncorrectTypeError(self, method="add_element", compatible_types=compatible_elements, incompatible_type=element)
        self.element = element
        return self

    def dispatch_action(self) -> Self:
        """
        (Optional) Indicates that the use of elements in this block should dispatch a block_actions payload
        :return: self
        """
        self.dispatches_action = True
        return self

    def set_hint(self, hint_text: str) -> Self:
        """
        (Optional) Sets an optional hint that appears below an input element in a lighter grey
        :param hint_text: PlainText; max 2,000 chars
        :return: self
        """
        if not isinstance(hint_text, PlainText):
            raise IncorrectTypeError(self, method="set_hint", compatible_types=PlainText, incompatible_type=hint_text)
        if not 1 <= len(hint_text.text) <= 2000:
            raise TextLengthError(self, field="hint", min_length=1, max_length=2000)
        self.hint = hint_text
        return self

    def optional(self) -> Self:
        """
        (Optional) Indicates that the input element may be empty when a user submits the modal
        :return: self
        """
        self.is_optional = True
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.label, self.element]]):
            raise RequiredFieldsError(self, missing_field_names=["label", "element"])
        if self.dispatches_action is True and isinstance(self.element, FileInput):
            raise TypeError("The 'dispatch_action' field of the Input block is incompatible with the FileInput element "
                            "and will result in the Slack API raising an unsupported type error.")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "element": json.loads(self.element.build_to_json()),
            "label": json.loads(self.label.build_to_json())
        }
        if self.block_id:
            data["block_id"] = self.block_id
        if self.hint:
            data["hint"] = json.loads(self.hint.build_to_json())
        if self.is_optional:
            data["optional"] = self.is_optional
        if self.dispatches_action:
            data["dispatch_action"] = self.dispatches_action

        return json.dumps(data)