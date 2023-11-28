import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class ConversationsFilter:
    """
    A Python class representing a Conversations filter object for conversation lists Slack BlockKit UI framework
    """
    def __init__(self):
        self._included_conversations = []
        self._exclude_external_shared_channels = False
        self._exclude_bot_users = False
        self.json = {
            "include": self._included_conversations,
            "exclude_external_shared_channels": self._exclude_external_shared_channels,
            "exclude_bot_users": self._exclude_bot_users
        }

    def include(self, *conversation_types) -> Self:
        """
        (Optional) Sets which type of conversations should be included in the list. When provided, any matching
        conversations will be excluded.
        :param conversation_types: One or more of "im", "mpim", "private", and "public"; preface with * if passing in a list
        :return: self
        """
        for conversation_type in conversation_types:
            self._included_conversations.append(conversation_type)
        self.json["include"] = self._included_conversations
        return self

    def exclude_external_shared_channels(self) -> Self:
        """
        (Optional) Indicates whether to exclude external shared channels from conversation lists
        :return: self
        """
        self._exclude_external_shared_channels = True
        self.json["exclude_external_shared_channels"] = self._exclude_external_shared_channels
        return self

    def exclude_bot_users(self) -> Self:
        """
        (Optional) Indicates whether to exclude bot users from conversation lists
        :return: self
        """
        self._exclude_bot_users = True
        self.json["exclude_bot_users"] = self._exclude_bot_users
        return self

