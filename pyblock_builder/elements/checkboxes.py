import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Checkboxes:
    """
    A Python class representing a Checkboxes element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "checkboxes"
        self._action_id = ""
        self._options = []
        self._initial_options = []
        self._confirm = None
        self._focus_on_load = False
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "options": self._options
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

    def set_options(self, *options) -> Self:
        """
        (Required) Sets the options belonging to this specific group
        :param options: One or more Option objects; maximum of 10 options; preface with * if passing in a list.
        :return: self
        """
        for option in options:
            self._options.append(option.json)
        self.json["options"] = self._options
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

    def set_initial_options(self, *options) -> Self:
        """
        (Optional) Sets the options that will be initially selected when the Checkbox group loads. Must contain at
        least one option that exactly matches one of the options in self.options.
        :param options: One or more Option objects; maximum of 10 options; preface with * if passing in a list.
        :return: self
        """
        for option in options:
            self._initial_options.append(option.json)
        self.json["initial_options"] = self._initial_options
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
