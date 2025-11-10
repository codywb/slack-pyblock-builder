import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.objects import ConfirmationDialog, Option, PlainText


@dataclass
class OverflowMenu:
    """
    Allows users to press a button to view a list of options.
    Can be added to: Section, Actions
    Works on: Modal, Message, AppHome
    """
    type: Literal["overflow"] = "overflow"
    action_id: str | None = None
    options: list[Option] = field(default_factory=list)
    confirm: ConfirmationDialog | None = None

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
        return self

    def set_options(self, *options: Option | Sequence[Option]) -> Self:
        """
       Sets the options belonging to this specific menu
       :param options: One or more Option objects, or a list/tuple of Option objects; maximum of 5 items
       :return: self
       """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        if not 1 <= len(flattened_options) <= 5:
            raise ItemLengthError(self, field="options", min_length=1, max_length=5)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_options", compatible_types=Option, incompatible_type=option)
            if not isinstance(option.text, PlainText):
                raise TypeError("One or more Option objects include MrkdwnText objects. OverflowMenu elements can only "
                                "include Option objects comprising PlainText objects.")
            self.options.append(option)
        return self

    def set_confirm_dialog(self, confirm_dialog: ConfirmationDialog) -> Self:
        """
        (Optional) Adds a confirmation dialog that appears before the multi-select choices are submitted
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
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
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates an OverflowMenu instance from its JSON representation
        :param json: a JSON representation of an OverflowMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.options = [Option().build_from_json(option) for option in json["options"]]
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self
