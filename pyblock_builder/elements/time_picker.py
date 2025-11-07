import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
from datetime import datetime
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError)
from pyblock_builder.objects import ConfirmationDialog, PlainText

@dataclass
class TimePicker:
    """
    Allows users to select a time of day.
    Can be added to: Section, Actions
    Works on: Modal, Message, AppHome
    """
    type: Literal["timepicker"] = "timepicker"
    action_id: str | None = None
    initial_time: str | datetime | None = None
    confirm: ConfirmationDialog | None = None
    is_focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    timezone: str | None = None

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

    def set_initial_time(self, time: str | datetime) -> Self:
        """
        (Optional) Sets the time to be initially selected when the element loads. Must be in HH:mm format where HH is
        the 24-hour format of an hour (00 to 23) and mm is the minutes with a leading zero (00 to 59).
        :param time: String in HH:mm format or Python datetime object
        :return: self
        """
        if not isinstance(time, str) and not isinstance(time, datetime):
            raise IncorrectTypeError(self, method="set_initial_time", compatible_types=[str, datetime], incompatible_type=time)
        if isinstance(time, datetime):
            self.initial_time = time.strftime("%H:%M")
        else:
            self.initial_time = time
        return self

    def set_placeholder_text(self, placeholder_text: PlainText) -> Self:
        """
        (Optional) Sets the placeholder text shown on the timepicker.
        :param placeholder_text: PlainText; max 150 chars
        :return: self
        """
        if not isinstance(placeholder_text, PlainText):
            raise IncorrectTypeError(self, method="set_placeholder_text", compatible_types=PlainText,
                                     incompatible_type=placeholder_text)
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
        (Optional) Defines an optional confirmation dialog that appears after a time is selected.
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
        return self

    def set_timezone(self, timezone: str) -> Self:
        """
        (Optional) Sets the timezone in IANA format, e.g. "America/Chicago". The timezone is displayed to end users as
        hint text underneath the time picker. It is also passed to the app upon certain interactions, such as
        view_submission.
        :param timezone: String
        :return: self
        """
        if not isinstance(timezone, str):
            raise IncorrectTypeError(self, method="set_timezone", compatible_types=str, incompatible_type=timezone)
        self.timezone = timezone
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
        if self.initial_time:
            data["initial_time"] = self.initial_time
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.timezone:
            data["timezone"] = self.timezone

        return json.dumps(data)

