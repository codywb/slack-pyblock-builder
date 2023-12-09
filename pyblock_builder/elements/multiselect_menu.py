import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class MultiSelectMenu:
    """
    A Python class representing a basic Multi-select menu element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = None
        self._action_id = ""
        self._confirm = None
        self._max_selected_items = None
        self._focus_on_load = False
        self._placeholder = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
            "confirm": None,
            "placeholder": None
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

    def set_max_selected_items(self, num_items: int) -> Self:
        """
        (Optional) Sets the maximum number of items that can be selected in the menu
        :param num_items: Integer; minimum number is 1
        :return: self
        """
        self._max_selected_items = num_items
        self.json["max_selected_items"] = self._max_selected_items
        return self

    def set_placeholder_text(self, placeholder_text):
        """
        (Optional) Sets the placeholder text shown on the menu.
        :param placeholder_text: String; max 150 chars
        :return: Nothing
        """
        self._placeholder = Text().set_text(placeholder_text)
        self.json["placeholder"] = self._placeholder.json
        return self

    def set_confirm_dialog(self, confirm_dialog) -> Self:
        """
        (Optional) Adds a confirmation dialog to be displayed before the multi-select choices are submitted
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


class MultiStaticSelect(MultiSelectMenu):
    """
    A Python class representing a Multi-select menu element with static options from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "multi_static_select"
        self._options = []
        self._option_groups = []
        self._initial_options = []
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load
        }

    def set_options(self, *options) -> Self:
        """
        (Required) Sets the options for selection in this menu
        :param options: One or more Option objects; maximum of 100 options. Do not set if setting self.option_groups!
        :return: self
        """
        for option in options:
            self._options.append(option.json)
        self.json["options"] = self._options
        return self

    def set_option_groups(self, *option_groups) -> Self:
        """
        (Optional) Sets the options for selection in this menu
        :param option_groups: One or more OptionGroup objects; maximum of 100 option groups. Do not set if setting
        self.options!
        :return: self
        """
        for option_group in option_groups:
            self._option_groups.append(option_group.json)
        self.json["option_groups"] = self._option_groups
        return self

    def set_initial_options(self, *options) -> Self:
        """
        (Optional) Sets the options that will be initially selected when the menu loads. Must contain at
        least one option that exactly matches one of the options in self.options or self.option_groups.
        :param options: One or more Option objects; preface with * if passing in a list
        :return: self
        """
        for option in options:
            self._initial_options.append(option.json)
        self.json["initial_options"] = self._initial_options
        return self


class MultiUsersSelect(MultiSelectMenu):
    """
    A Python class representing a Multi-select menu element with a User list from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "multi_users_select"
        self._initial_users = []
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
        }

    def set_initial_users(self, user_ids: list) -> Self:
        """
        (Optional) Sets a list of pre-selected users when the menu loads
        :param user_ids: List of Slack User IDs as Strings
        :return: self
        """
        self._initial_users = user_ids
        self.json["initial_users"] = self._initial_users
        return self


class MultiConversationsSelect(MultiSelectMenu):
    """
    A Python class representing a Multi-select menu element with a Conversations list from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "multi_conversations_select"
        self._initial_conversations = []
        self._default_to_current_conversation = False
        self._filter = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
            "default_to_current_conversation": False,
        }

    def set_initial_conversations(self, conversation_ids: list) -> Self:
        """
        (Optional) Sets a list of pre-selected conversations when the menu loads
        :param conversation_ids: List of valid conversation IDs as Strings; ignored if self.default_to_current_conversation is set to True
        :return: self
        """
        self._initial_conversations = conversation_ids
        self.json["initial_conversations"] = self._initial_conversations
        return self

    def default_to_current_conversation(self) -> Self:
        """
        (Optional) Pre-populates the select menu with the conversation that the user was viewing when they opened the
        modal, if available
        :return: self
        """
        self._default_to_current_conversation = True
        self.json["default_to_current_conversation"] = self._default_to_current_conversation
        return self

    def set_filter(self, filter_obj) -> Self:
        """
        (Optional) Sets a filter for reducing the list of available conversations using the specified criteria
        :param filter_obj: ConversationsFilter object
        :return: self
        """
        self._filter = filter_obj
        self.json["filter"] = self._filter
        return self


class MultiChannelsSelect(MultiSelectMenu):
    """
    A Python class representing a Multi-select menu element with a public channels list from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "multi_channels_select"
        self._initial_channels = []
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
        }

    def set_initial_channels(self, channel_ids: list) -> Self:
        """
        Sets a list of pre-selected public channels when the menu loads
        :param channel_ids: List of valid public Slack Channel IDs as Strings
        :return: self
        """
        self._initial_channels = channel_ids
        self.json["initial_channels"] = self._initial_channels
        return self

