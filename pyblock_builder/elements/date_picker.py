import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from datetime import date, datetime
from pyblock_builder._internal.errors import (TextLengthError, IncorrectTypeError)
from pyblock_builder.objects.text import PlainText
from pyblock_builder.objects import ConfirmationDialog

@dataclass
class DatePicker:
    """
    Allows users to select a date from a calendar style UI.
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["datepicker"] = "datepicker"
    action_id: str | None = None
    initial_date: str | date | datetime = None
    confirm: ConfirmationDialog | None = None
    is_focus_on_load: bool | None = None
    placeholder: PlainText | None = None

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

    def set_initial_date(self, initial_date: str | date | datetime) -> Self:
        """
        (Optional) Sets the initial date that is selected when the element is loaded
        :param date: String in YYYY-MM-DD format or Python date/datetime object
        :return: self
        """
        if not isinstance(initial_date, str) and not isinstance(initial_date, date) and not isinstance(initial_date, datetime):
            raise IncorrectTypeError(self, method="set_initial_date", compatible_types=[str, date, datetime])
        if isinstance(initial_date, date) or isinstance(initial_date, datetime):
            self.initial_date = initial_date.strftime("%Y-%m-%d")
        else:
            self.initial_date = initial_date
        return self

    def set_placeholder_text(self, placeholder_text: PlainText) -> Self:
        """
        (Optional) Sets the placeholder text shown on the datepicker
        :param placeholder_text: PlainText; max 150 chars
        :return: self
        """
        if not isinstance(placeholder_text, PlainText):
            raise IncorrectTypeError(self, method="set_placeholder_text", compatible_types=PlainText, incompatible_type=placeholder_text)
        if not 1 <= len(placeholder_text.text) <= 150:
            raise TextLengthError(self, field="text", min_length=1, max_length=150)
        self.placeholder = placeholder_text
        return self

    def focus_on_load(self, focus: bool=True) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self.is_focus_on_load = focus
        return self

    def set_confirm_dialog(self, confirm_dialog: ConfirmationDialog) -> Self:
        """
        (Optional) Defines an optional confirmation dialog that appears after a date is selected.
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.initial_date:
            data["initial_date"] = self.initial_date
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a DatePicker instance from its JSON representation
        :param json: a JSON representation of a DatePicker element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "initial_date" in json.keys() and json["initial_date"] is not None:
            self.initial_date = json["initial_date"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self
