import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from datetime import datetime
from pyblock_builder.objects.text import Text


class TimePicker:
    """
    A Python class representing a Time picker element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "timepicker"
        self._action_id = ""
        self._initial_time = ""
        self._confirm = None
        self._focus_on_load = False
        self._placeholder = None
        self._timezone = ""
        self.json = {
            "type": self._type,
            "action_id": self._action_id
        }

    def set_action_id(self, action_id: str) -> Self:
        """
        (Optional) Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        self._action_id = action_id
        self.json["action_id"] = self._action_id
        return self

    def set_initial_time(self, time: str | datetime) -> Self:
        """
        (Optional) Sets the time to be initially selected when the element loads. Must be in HH:mm format where HH is
        the 24-hour format of an hour (00 to 23) and mm is the minutes with a leading zero (00 to 59).
        :param time: String in HH:mm format or Python datetime object
        :return: self
        """
        if isinstance(time, datetime):
            self._initial_time = time.strftime("%H:%M")
        self._initial_time = time
        self.json["initial_time"] = self._initial_time
        return self

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        (Optional) Sets the placeholder text shown on the timepicker
        :param placeholder_text: String; max 150 chars
        :return: self
        """
        self._placeholder = Text().set_text(placeholder_text)
        self.json["placeholder"] = self._placeholder.json
        return self

    def set_confirm_dialog(self, confirm_dialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after a time is selected
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

    def set_timezone(self, timezone: str) -> Self:
        """
        (Optional) Sets the timezone in IANA format, e.g. "America/Chicago". The timezone is displayed to end users as
        hint text underneath the time picker. It is also passed to the app upon certain interactions, such as
        view_submission.
        :param timezone: String
        :return: self
        """
        self._timezone = timezone
        self.json["timezone"] = self._timezone
        return self
