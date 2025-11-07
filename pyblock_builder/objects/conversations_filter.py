import sys

if sys.version_info >= (3, 11):
    from typing import Self, Any, Literal
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (RequiredFieldError, IncorrectTypeError, IncorrectValueError)

@dataclass
class ConversationsFilter:
    """
    Defines a filter for the list of options in a conversation selector menu. The menu can be either a conversations
    select menu or a conversations multi-select menu.
    """
    included_conversations: list[str] | None = None
    exclude_external: bool = False
    exclude_bots : bool = False

    def include(self, conversations: list[Literal["im", "mpim", "private", "public"]]) -> Self:
        """
        (Optional) Sets which type of conversations should be included in the list. When provided, any matching
        conversations will be excluded.
        :param conversations: One or more of "im", "mpim", "private", and "public"
        :return: self
        """
        FILTERABLE_CONVERSATIONS = ["im", "mpim", "private", "public"]
        if not isinstance(conversations, list):
            raise IncorrectTypeError(self, method="include", compatible_types=list, incompatible_type=conversations)
        for conversation in conversations:
            if conversation not in FILTERABLE_CONVERSATIONS:
                raise IncorrectValueError(self, method="include", acceptable_values=FILTERABLE_CONVERSATIONS, unacceptable_value=conversation)
        self.included_conversations = conversations
        return self

    def exclude_external_shared_channels(self) -> Self:
        """
        (Optional) Exclude external shared channels from conversation lists
        :return: self
        """
        self.exclude_external = True
        return self

    def exclude_bot_users(self) -> Self:
        """
        (Optional) Exclude bot users from conversation lists
        :return: self
        """
        self.exclude_bots = True
        return self

    def build_to_json(self) -> str:
        # raise error if at least one field is not set
        if not any([self.included_conversations, self.exclude_bots, self.exclude_external]):
            raise RequiredFieldError(self, missing_field_names="included_conversations")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "exclude_external_shared_channels": self.exclude_external,
            "exclude_bot_users": self.exclude_bots,
        }
        if self.included_conversations:
            data["include"] = self.included_conversations

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a ConversationsFilter instance from its JSON representation
        :param json: a JSON representation of a ConversationsFilter object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "include" in json.keys() and json["include"] is not None:
            self.included_conversations = json["include"]
        if "exclude_external_shared_channels" in json.keys() and json["exclude_external_shared_channels"] is not None:
            self.exclude_external = json["exclude_external_shared_channels"]
        if "exclude_bot_users" in json.keys() and json["exclude_bot_users"] is not None:
            self.exclude_bots = json["exclude_bot_users"]
        return self
