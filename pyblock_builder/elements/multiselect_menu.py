import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.objects.text import PlainText
from pyblock_builder.objects import ConfirmationDialog, Option, OptionGroup, ConversationsFilter

@dataclass
class MultiSelectMenu:
    """
    Allows users to select multiple items from a list of options.
    Can be added to: Section, Input
    Works on: Modal, Message, AppHome
    """
    type: str | None = None
    action_id: str | None = None
    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
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

    def set_placeholder_text(self, placeholder_text: PlainText) -> Self:
        """
        (Optional) Sets the placeholder text shown on the multi-select menu
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
        (Optional) Adds a confirmation dialog that appears before the multi-select choices are submitted
        :param confirm_dialog: ConfirmationDialog object
        :return: self
        """
        if not isinstance(confirm_dialog, ConfirmationDialog):
            raise IncorrectTypeError(self, method="set_confirm_dialog", compatible_types=ConfirmationDialog,
                                     incompatible_type=confirm_dialog)
        self.confirm = confirm_dialog
        return self

    def set_max_selected_items(self, max_items: int) -> Self:
        """
        Specifies the maximum number of items that can be selected in the menu.
        :param max_items: int; minimum number is 1
        :return: self
        """
        if not isinstance(max_items, int):
            raise IncorrectTypeError(self, method="set_max_selected_items", compatible_types=int, incompatible_type=max_items)
        if not max_items >= 1:
            raise ValueError(f"The 'set_max_selected_items' method of {self.__class__.__name__} must be set to a value of at least 1")
        self.max_selected_items = max_items
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.max_selected_items:
            data["max_selected_items"] = self.max_selected_items

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
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
        if "max_selected_items" in json.keys() and json["max_selected_items"] is not None:
            self.max_selected_items = json["max_selected_items"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self

@dataclass
class MultiStaticSelectMenu(MultiSelectMenu):
    """
    The most basic form of multi-select menu, with a static list of options passed in when defining the element
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["multi_static_select"] = "multi_static_select"
    options: list[Option] = field(default_factory=list)
    option_groups: list[OptionGroup] = field(default_factory=list)
    initial_options: list[Option] = field(default_factory=list)

    def set_options(self, *options: Option | Sequence[Option]) -> Self:
        """
       Sets the options belonging to this specific group
       :param options: One or more Option objects, or a list/tuple of Option objects; maximum of 100 items
       :return: self
       """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        if not 1 <= len(flattened_options) <= 100:
            raise ItemLengthError(self, field="options", min_length=1, max_length=100)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_options", compatible_types=Option, incompatible_type=option)
            if not isinstance(option.text, PlainText):
                raise TypeError("One or more Option objects include MrkdwnText objects in the 'text' field. "
                                "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            if option.description:
                if not isinstance(option.description, PlainText):
                    raise TypeError(
                        "One or more Option objects include MrkdwnText objects in the 'description' field. "
                        "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            self.options.append(option)
        return self

    def set_option_groups(self, *option_groups: OptionGroup | Sequence[OptionGroup]) -> Self:
        """
       Sets the option groups belonging to this specific group
       :param option_groups: One or more OptionGroup objects, or a list/tuple of OptionGroup objects; maximum of 100 items
       :return: self
       """
        flattened_option_groups = []
        for opt_group in option_groups:
            if isinstance(opt_group, (list, tuple)):
                flattened_option_groups.extend(opt_group)
            else:
                flattened_option_groups.append(opt_group)

        if not 1 <= len(flattened_option_groups) <= 100:
            raise ItemLengthError(self, field="option_groups", min_length=1, max_length=100)

        for option_group in flattened_option_groups:
            if not isinstance(option_group, OptionGroup):
                raise IncorrectTypeError(self, method="set_option_groups", compatible_types=OptionGroup, incompatible_type=option_group)
            for option in option_group.options:
                if not isinstance(option.text, PlainText):
                    raise TypeError("One or more Option objects include MrkdwnText objects in the 'text' field. "
                                    "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
                if option.description:
                    if not isinstance(option.description, PlainText):
                        raise TypeError(
                            "One or more Option objects include MrkdwnText objects in the 'description' field. "
                            "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            self.option_groups.append(option_group)
        return self

    def set_initial_options(self, *options: Option | Sequence[Option]) -> Self:
        """
        (Optional) Sets the options that will be initially selected when the menu loads. Must contain at
        least one option that exactly matches one of the options in self.options or self.option_groups
        :param options: One or more Option objects, or a list/tuple of Option objects
        :return: self
        """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_initial_options", compatible_types=Option,
                                         incompatible_type=option)
            if not isinstance(option.text, PlainText):
                raise TypeError("One or more Option objects include MrkdwnText objects in the 'text' field. "
                                "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            if option.description:
                if not isinstance(option.description, PlainText):
                    raise TypeError(
                        "One or more Option objects include MrkdwnText objects in the 'description' field. "
                        "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            self.initial_options.append(option)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not any([self.options, self.option_groups]):
            raise RequiredFieldError(self, missing_field_names=["options", "options_groups"])
        if self.option_groups and self.options:
            raise TypeError(f"Setting both 'options' and 'option_groups' on an {self.__class__.__name__} element will result in the Slack API rejecting the payload.")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.max_selected_items:
            data["max_selected_items"] = self.max_selected_items
        if self.options:
            data["options"] = [json.loads(option.build_to_json()) for option in self.options]
        if self.option_groups:
            data["option_groups"] = [json.loads(option_group.build_to_json()) for option_group in self.option_groups]
        if self.initial_options:
            data["initial_options"] = [json.loads(option.build_to_json()) for option in self.initial_options]

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiStaticSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiStaticSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "options" in json.keys() and json["options"] is not None:
            self.options = [Option().build_from_json(option) for option in json["options"]]
        if "option_groups" in json.keys() and json["option_groups"] is not None:
            self.option_groups = [OptionGroup().build_from_json(group) for group in json["option_groups"]]
        if "initial_options" in json.keys() and json["initial_options"] is not None:
            self.initial_options = [Option().build_from_json(option) for option in json["initial_options"]]
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "max_selected_items" in json.keys() and json["max_selected_items"] is not None:
            self.max_selected_items = json["max_selected_items"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self

@dataclass
class MultiExternalSelectMenu(MultiSelectMenu):
    """
    This menu will load its options from an external data source, allowing for a dynamic list of options.
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["multi_external_select"] = "multi_external_select"
    initial_options: list[Option] = field(default_factory=list)
    min_query_length: int | None = None

    def set_initial_options(self, *options: Option | Sequence[Option]) -> Self:
        """
        (Optional) Sets the options that will be initially selected when the menu loads. Must contain at
        least one option that exactly matches one of the options in self.options or self.option_groups
        :param options: One or more Option objects, or a list/tuple of Option objects
        :return: self
        """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_initial_options", compatible_types=Option,
                                         incompatible_type=option)
            if not isinstance(option.text, PlainText):
                raise TypeError("One or more Option objects include MrkdwnText objects in the 'text' field. "
                                "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            if option.description:
                if not isinstance(option.description, PlainText):
                    raise TypeError(
                        "One or more Option objects include MrkdwnText objects in the 'description' field. "
                        "MultiSelectMenu elements can only include Option objects comprising PlainText objects.")
            self.initial_options.append(option)
        return self

    def set_min_query_length(self, min_length: int) -> Self:
        """
        Specifies the fewest number of typed characters required before dispatching a request to the external source.
        :param min_length: int; defaults to 3
        :return: self
        """
        if not isinstance(min_length, int):
            raise IncorrectTypeError(self, method="set_min_query_length", compatible_types=int, incompatible_type=min_length)
        if not min_length >= 1:
            raise ValueError(f"The 'set_min_query_length' method of {self.__class__.__name__} must be set to a value of at least 1")
        self.min_query_length = min_length
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.min_query_length:
            data["min_query_length"] = self.min_query_length
        if self.initial_options:
            data["initial_options"] = [json.loads(option.build_to_json()) for option in self.initial_options]

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiExternalSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiExternalSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "initial_options" in json.keys() and json["initial_options"] is not None:
            self.initial_options = [Option().build_from_json(option) for option in json["initial_options"]]
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "min_query_length" in json.keys() and json["min_query_length"] is not None:
            self.min_query_length = json["min_query_length"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self

@dataclass
class MultiUsersSelectMenu(MultiSelectMenu):
    """
    This multi-select menu will populate its options with a list of Slack users visible to the current user in the
    active workspace.
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["multi_users_select"] = "multi_users_select"
    initial_users: list[str] = field(default_factory=list)

    def set_initial_users(self, user_ids: list[str]) -> Self:
        """
        (Optional) Sets a list of pre-selected users when the menu loads
        :param user_ids: List of Slack User IDs as strings
        :return: self
        """
        if not isinstance(user_ids, list):
            raise IncorrectTypeError(self, method="set_initial_users", compatible_types=list[str], incompatible_type=user_ids)
        if isinstance(user_ids, list):
            for user_id in user_ids:
                if not isinstance(user_id, str):
                    raise TypeError("Non-string value included in user_ids list passed as argument to the 'set_initial_users' method of MultiUserSelect")
        self.initial_users = user_ids
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.max_selected_items:
            data["max_selected_items"] = self.max_selected_items
        if self.initial_users:
            data["initial_users"] = self.initial_users

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiUsersSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiUsersSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "initial_users" in json.keys() and json["initial_users"] is not None:
            self.initial_users = json["initial_users"]
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "max_selected_items" in json.keys() and json["max_selected_items"] is not None:
            self.max_selected_items = json["max_selected_items"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self

@dataclass
class MultiConversationsSelectMenu(MultiSelectMenu):
    """
    This multi-select menu will populate its options with a list of public and private channels, DMs, and MPIMs visible
    to the current user in the active workspace.
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["multi_conversations_select"] = "multi_conversations_select"
    initial_conversations: list[str] = field(default_factory=list)
    defaults_to_current_conversation: bool | None = None
    filter: ConversationsFilter | None = None

    def set_initial_conversations(self, conversation_ids: list) -> Self:
        """
        (Optional) Sets a list of pre-selected conversations when the menu loads
        :param conversation_ids: List of valid conversation IDs as Strings; ignored if self.default_to_current_conversation is set to True
        :return: self
        """
        if not isinstance(conversation_ids, list):
            raise IncorrectTypeError(self, method="set_initial_conversations", compatible_types=list[str], incompatible_type=conversation_ids)
        if isinstance(conversation_ids, list):
            for conversation_id in conversation_ids:
                if not isinstance(conversation_id, str):
                    raise TypeError("Non-string value included in conversation_ids list passed as argument to the "
                                    "'set_initial_conversations' method of MultiConversationSelect")
        self.initial_conversations = conversation_ids
        return self

    def default_to_current_conversation(self) -> Self:
        """
        (Optional) Pre-populates the select menu with the conversation that the user was viewing when they opened the
        modal, if available
        :return: self
        """
        self.defaults_to_current_conversation = True
        return self

    def set_filter(self, filter: ConversationsFilter) -> Self:
        """
        (Optional) Sets a filter for reducing the list of available conversations using the specified criteria
        :param filter_obj: ConversationsFilter object
        :return: self
        """
        if not isinstance(filter, ConversationsFilter):
            raise IncorrectTypeError(self, method="set_filter", compatible_types=ConversationsFilter,
                                     incompatible_type=filter)
        self.filter = filter
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.filter:
            data["filter"] = json.loads(self.filter.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.default_to_current_conversation:
            data["default_to_current_conversation"] = self.defaults_to_current_conversation
        if self.max_selected_items:
            data["max_selected_items"] = self.max_selected_items
        if self.initial_conversations:
            data["initial_conversations"] = self.initial_conversations

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiConversationsSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiConversationsSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "initial_conversations" in json.keys() and json["initial_conversations"] is not None:
            self.initial_conversations = json["initial_conversations"]
        if "default_to_current_conversation" in json.keys() and json["default_to_current_conversation"] is not None:
            self.defaults_to_current_conversation = json["default_to_current_conversation"]
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "max_selected_items" in json.keys() and json["max_selected_items"] is not None:
            self.max_selected_items = json["max_selected_items"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        if "filter" in json.keys() and json["filter"] is not None:
            self.filter = ConversationsFilter().build_from_json(json["filter"])
        return self

@dataclass
class MultiChannelsSelectMenu(MultiSelectMenu):
    """
    This multi-select menu will populate its options with a list of public channels visible to the current user in the
    active workspace.
    Can be added to: Section, Actions, Input
    Works on: Modal, Message, AppHome
    """
    type: Literal["multi_channels_select"] = "multi_channels_select"
    initial_channels: list[str] = field(default_factory=list)

    def set_initial_channels(self, channel_ids: list[str]) -> Self:
        """
        (Optional) Sets a list of pre-selected public channels when the menu loads
        :param channel_ids: List of valid public Slack Channel IDs as strings
        :return: self
        """
        if not isinstance(channel_ids, list):
            raise IncorrectTypeError(self, method="set_initial_channels", compatible_types=list[str], incompatible_type=channel_ids)
        if isinstance(channel_ids, list):
            for channel_id in channel_ids:
                if not isinstance(channel_id, str):
                    raise TypeError("Non-string value included in channel_ids list passed as argument to the 'set_initial_channels' method of MultiChannelSelect")
        self.initial_channels = channel_ids
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())
        if self.action_id:
            data["action_id"] = self.action_id
        if self.confirm:
            data["confirm"] = json.loads(self.confirm.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.max_selected_items:
            data["max_selected_items"] = self.max_selected_items
        if self.initial_channels:
            data["initial_channels"] = self.initial_channels

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MultiChannelsSelectMenu instance from its JSON representation
        :param json: a JSON representation of a MultiChannelsSelectMenu element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "initial_channels" in json.keys() and json["initial_channels"] is not None:
            self.initial_channels = json["initial_channels"]
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "max_selected_items" in json.keys() and json["max_selected_items"] is not None:
            self.max_selected_items = json["max_selected_items"]
        if "confirm" in json.keys() and json["confirm"] is not None:
            self.confirm = ConfirmationDialog().build_from_json(json["confirm"])
        return self
