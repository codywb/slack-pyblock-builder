import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from datetime import datetime
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError)
from pyblock_builder.objects import ConfirmationDialog

@dataclass
class DateTimePicker:
    """
    Allows users to select both a date and a time of day, formatted as a Unix timestamp.
    Can be added to: Actions, Input
    Works on: Modal, Message
    """
    type: Literal["datetimepicker"] = "datetimepicker"
    action_id: str | None = None
    initial_date_time: int | datetime = None
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
        return self

    def set_initial_date_time(self, initial_date_time: int | datetime) -> Self:
        """
        (Optional) Sets the initial date and time that is selected when the element is loaded
        :param date_time: UNIX timestamp in seconds (should be 10 digits) or Python datetime object
        :return: self
        """
        if not isinstance(initial_date_time, int) and not isinstance(initial_date_time, datetime):
            raise IncorrectTypeError(self, method="set_initial_date_time", compatible_types=[int, datetime], incompatible_type=initial_date_time)
        if isinstance(initial_date_time, datetime):
            self.initial_date_time = int(initial_date_time.timestamp())
        else:
            self.initial_date_time = initial_date_time
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
        (Optional) Defines an optional confirmation dialog that appears after a time is selected.
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
        if self.action_id:
            data["action_id"] = self.action_id
        if self.initial_date_time:
            data["initial_date_time"] = self.initial_date_time
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())

        return json.dumps(data)
