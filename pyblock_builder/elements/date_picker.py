import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from datetime import date, datetime
from pyblock_builder.objects.text import Text


class DatePicker:
    """
    A Python class representing a Date Picker element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "datepicker"
        self._action_id = ""
        self._initial_date = None
        self._confirm = None
        self._focus_on_load = False
        self._placeholder = None
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

    def set_initial_date(self, initial_date: str | date | datetime) -> Self:
        """
        (Optional) Sets the initial date that is selected when the element is loaded
        :param date: String in YYYY-MM-DD format or Python date/datetime object
        :return: self
        """
        if isinstance(initial_date, date) or isinstance(initial_date, datetime):
            self._initial_date = initial_date.strftime("%Y-%m-%d")
        else:
            self._initial_date = initial_date
        self.json["initial_date"] = self._initial_date
        return self

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        (Optional) Sets the placeholder text shown on the datepicker
        :param placeholder_text: String; max 150 chars
        :return: self
        """
        self._placeholder = Text("plain_text", placeholder_text)
        self.json["placeholder"] = self._placeholder.json
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
