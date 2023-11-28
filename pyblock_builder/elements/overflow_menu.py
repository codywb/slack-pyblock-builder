import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class OverflowMenu:
    """
    A Python class representing an Overflow menu element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "overflow"
        self._action_id = ""
        self._options = []
        self._confirm = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "options": self._options
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

    def set_confirm_dialog(self, confirm_dialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed after a menu item is selected
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        self._confirm = confirm_dialog
        self.json["confirm"] = self._confirm.json
        return self

    def set_options(self, *options) -> Self:
        """
        (Required) Sets the options for selection in this menu
        :param options: One or more Option objects; maximum of 100 options. Preface with * if passing in a list. Do not set if setting self.option_groups!
        :return: self
        """
        for option in options:
            self._options.append(option.json)
        self.json["options"] = self._options
        return self
