import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class SelectMenu:
    """
    A Python class representing a basic Select menu element from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = None
        self._action_id = ""
        self._confirm = None
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

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        (Optional) Sets the placeholder text shown on the menu
        :param placeholder_text: String; max 150 chars
        :return: self
        """
        self._placeholder = Text().set_text(placeholder_text)
        self.json["placeholder"] = self._placeholder.json
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

    def focus_on_load(self) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self._focus_on_load = True
        self.json["focus_on_load"] = self._focus_on_load
        return self


class StaticSelectMenu(SelectMenu):
    """
    A Python class representing a Select menu element with static options from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "static_select"
        self._options = []
        self._option_groups = []
        self._initial_option = None
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load
        }

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

    def set_option_groups(self, *option_groups) -> Self:
        """
        (Optional) Sets the options for selection in this menu
        :param option_groups: One or more OptionGroup objects; maximum of 100 option groups. Preface with * if passing in a list. Do not set if setting self.options!
        :return: self
        """
        for option_group in option_groups:
            self._option_groups.append(option_group.json)
        self.json["option_groups"] = self._option_groups
        return self

    def set_initial_option(self, option) -> Self:
        """
        (Optional) Sets the option that will be initially selected when the radio button group loads. Must exactly
        match one of the options within self.options.
        :param option: An Option object
        :return: self
        """
        self._initial_option = option
        self.json["initial_option"] = self._initial_option.json
        return self


class UsersSelectMenu(SelectMenu):
    """
    A Python class representing a Select menu element with a list of users from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "users_select"
        self._initial_user = ""
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load
        }

    def set_initial_user(self, user_id: str) -> Self:
        """
        (Optional) Sets a pre-selected user when the menu loads.
        :param user_id: Slack User IDs as String
        :return: self
        """
        self._initial_user = user_id
        self.json["initial_user"] = self._initial_user
        return self


class ConversationsSelectMenu(SelectMenu):
    """
    A Python class representing a Select menu element of conversations from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "conversations_select"
        self._initial_conversation = ""
        self._default_to_current_conversation = False
        self._filter = None
        self._response_url_enabled = False
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
            "default_to_current_conversation": self._default_to_current_conversation,
            "response_url_enabled": False,
        }

    def enable_response_url(self) -> Self:
        """
        (Optional) Can be used to enable a response url, When True, the view_submission payload from the menu's
        parent view will contain a response_url which can be used for message responses. The target conversation will be
        determined by the value of this select menu.
        :return: self
        """
        self._response_url_enabled = True
        self.json["response_url_enabled"] = self._response_url_enabled
        return self

    def set_initial_conversation(self, conversation_id: str) -> Self:
        """
        (Optional) Sets a pre-selected conversation when the menu loads. Will take precedence if
        self.default_to_current_conversation is also set to True
        :param conversation_id: A valid conversation ID as a String
        :return: self
        """
        self._initial_conversation = conversation_id
        self.json["initial_conversation"] = self._initial_conversation
        return self

    def default_to_current_conversation(self) -> Self:
        """
        Pre-populates the select menu with the conversation that the user was viewing when they opened the modal,
        if available.
        :return: self
        """
        self._default_to_current_conversation = True
        self.json["default_to_current_conversation"] = self._default_to_current_conversation
        return self

    def set_filter(self, filter_obj) -> Self:
        """
        Sets a filter for reducing the list of available conversations using the specified criteria
        :param filter_obj: ConversationsFilter object
        :return: self
        """
        self._filter = filter_obj
        self.json["filter"] = self._filter
        return self


class ChannelsSelectMenu(SelectMenu):
    """
    A Python class representing a Select menu element of public channels from the Slack BlockKit UI framework\n
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        super().__init__()
        self._type = "channels_select"
        self._initial_channel = ""
        self._response_url_enabled = False
        self.json = {
            "type": self._type,
            "action_id": self._action_id,
            "focus_on_load": self._focus_on_load,
            "response_url_enabled": False,
        }

    def set_initial_channel(self, channel_id: str) -> Self:
        """
        (Optional) Sets a pre-selected public channel when the menu loads
        :param channel_id: A valid public Slack Channel ID as a String
        :return: self
        """
        self._initial_channel = channel_id
        self.json["initial_channel"] = self._initial_channel
        return self

    def enable_response_url(self) -> Self:
        """
        (Optional) Can be used to enable a response url, When True, the view_submission payload from the menu's
        parent view will contain a response_url which can be used for message responses. The target conversation will be
        determined by the value of this select menu.
        :return: self
        """
        self._response_url_enabled = True
        self.json["response_url_enabled"] = self._response_url_enabled
        return self
