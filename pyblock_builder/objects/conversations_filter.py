import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (RequiredFieldError, IncorrectTypeError, IncorrectValueError)

@dataclass
class ConversationsFilter:
    included_conversations: list[str] | None = None
    exclude_external: bool = False
    exclude_bots : bool = False

    def include(self, conversations: list[str]) -> Self:
        FILTERABLE_CONVERSATIONS = ["im", "mpim", "private", "public"]
        if not isinstance(conversations, list):
            raise IncorrectTypeError(self, method="include", compatible_types=list, incompatible_type=conversations)
        for conversation in conversations:
            if conversation not in FILTERABLE_CONVERSATIONS:
                raise IncorrectValueError(self, method="include", acceptable_values=FILTERABLE_CONVERSATIONS, unacceptable_value=conversation)
        self.included_conversations = conversations
        return self

    def exclude_external_shared_channels(self) -> Self:
        self.exclude_external = True
        return self

    def exclude_bot_users(self) -> Self:
        self.exclude_bots = True
        return self

    def build_to_json(self) -> str:
        # raise error if at least one field is not set
        if not any([self.included_conversations, self.exclude_external, self.exclude_bots]):
            raise RequiredFieldError(self, missing_field_names=["included_conversations", "exclude_external", "exclude_bots"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {}
        if self.included_conversations:
            data["included_conversations"] = self.included_conversations
        if self.exclude_external:
            data["exclude_external_shared_channels"] = self.exclude_external
        if self.exclude_bots:
            data["exclude_bot_users"] = self.exclude_bots

        return json.dumps(data)
#
# class ConversationsFilter:
#     """
#     A Python class representing a Conversations filter object for conversation lists Slack BlockKit UI framework
#     """
#     def __init__(self):
#         self._included_conversations = []
#         self._exclude_external_shared_channels = False
#         self._exclude_bot_users = False
#         self.json = {
#             "include": self._included_conversations,
#             "exclude_external_shared_channels": self._exclude_external_shared_channels,
#             "exclude_bot_users": self._exclude_bot_users
#         }
#
#     def include(self, *conversation_types) -> Self:
#         """
#         (Optional) Sets which type of conversations should be included in the list. When provided, any matching
#         conversations will be excluded.
#         :param conversation_types: One or more of "im", "mpim", "private", and "public"; preface with * if passing in a list
#         :return: self
#         """
#         for conversation_type in conversation_types:
#             self._included_conversations.append(conversation_type)
#         self.json["include"] = self._included_conversations
#         return self
#
#     def exclude_external_shared_channels(self) -> Self:
#         """
#         (Optional) Indicates whether to exclude external shared channels from conversation lists
#         :return: self
#         """
#         self._exclude_external_shared_channels = True
#         self.json["exclude_external_shared_channels"] = self._exclude_external_shared_channels
#         return self
#
#     def exclude_bot_users(self) -> Self:
#         """
#         (Optional) Indicates whether to exclude bot users from conversation lists
#         :return: self
#         """
#         self._exclude_bot_users = True
#         self.json["exclude_bot_users"] = self._exclude_bot_users
#         return self
#
