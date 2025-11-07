import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Sequence, Any
else:
    from typing_extensions import Self, Literal, Sequence, Any
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.objects import Option, ConfirmationDialog

@dataclass
class Checkboxes:
    """
    Allows users to choose multiple items from a list of options.\n
    Can be added to: Section, Actions, Input\n
    Works on: Modal, Message, AppHome
    """
    type: Literal["checkboxes"] = "checkboxes"
    action_id: str | None = None
    options: list[Option] = field(default_factory=list)
    initial_options: list[Option] = field(default_factory=list)
    confirm: ConfirmationDialog | None = None
    is_focus_on_load: bool | None = None

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

    def set_options(self, *options: Option | Sequence[Option]) -> Self:
        """
        Sets the options belonging to this specific group.

        :param options: One or more Option objects, or a list/tuple of Option objects; maximum of 10 options.
        :return: self
        """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        if not 1 <= len(flattened_options) <= 10:
            raise ItemLengthError(self, field="options", min_length=1, max_length=10)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_options", compatible_types=Option, incompatible_type=option)
            self.options.append(option)

        return self

    def set_initial_options(self, *options: Option | Sequence[Option]) -> Self:
        """
        (Optional) Sets the options that will be initially selected when the Checkbox group loads. Must contain at
        least one option that exactly matches one of the options in self.options.
        :param options: One or more Option objects, or a list/tuple of Option objects; maximum of 10 options.
        :return: self
        """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        if not 1 <= len(flattened_options) <= 10:
            raise ItemLengthError(self, field="options", min_length=1, max_length=10)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_initial_options", compatible_types=Option, incompatible_type=option)
            self.initial_options.append(option)
        return self

    def set_confirm_dialog(self, confirm_dialog: ConfirmationDialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after one of the checkboxes is clicked
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
        return self

    def focus_on_load(self, bool=True) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self.is_focus_on_load = bool
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.options:
            raise RequiredFieldError(self, missing_field_names="options")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "options": [json.loads(option.build_to_json()) for option in self.options],
        }
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.action_id:
            data["action_id"] = self.action_id
        if self.initial_options:
            data["initial_options"] = [json.loads(option.build_to_json()) for option in self.initial_options]
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())

        return json.dumps(data)
