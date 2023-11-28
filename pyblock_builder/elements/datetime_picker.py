import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from datetime import datetime

class DatetimePicker:
    """
    A Python class representing a Datetime Picker element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message
    """
    def __init__(self):
        self._type = "datetimepicker"
        self._action_id = ""
        self._initial_date_time = None
        self._confirm = None
        self._focus_on_load = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id
        }

    def set_action_id(self, action_id: str) -> Self:
        """
        Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        self._action_id = action_id
        self.json["action_id"] = self._action_id
        return self

    def set_initial_date_time(self, date_time: str | datetime) -> Self:
        """
        (Optional) Sets the initial date and time that is selected when the element is loaded
        :param date_time: UNIX timestamp in seconds as string (should be 10 digits) or Python datetime object
        :return: self
        """
        if isinstance(date_time, datetime):
            self._initial_date_time = date_time.timestamp()
        else:
            self._initial_date_time = date_time
        self.json["initial_date_time"] = self._initial_date_time
        return self

    def set_confirm_dialog(self, confirm_dialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after one of the checkboxes is clicked
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        self._confirm = confirm_dialog
        self.json["confirm"] = self._confirm.json
        return self

    def focus_on_load(self) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self._focus_on_load = True
        self.json["focus_on_load"] = self._focus_on_load
        return self