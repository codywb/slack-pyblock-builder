import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Header:
    """
    A Python class representing a Header block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "header"
        self._block_id = ""
        self._text = ""
        self.block = {
            "type": self._type
        }

    def set_block_id(self, block_id: str) -> Self:
        """
        (Optional) Sets a unique identifier for a block which can be used when receiving an interaction payload to
        identify the source of an action. If not set, will be auto-generated.
        :param block_id: String; max 255 chars, should be unique for each message and each subsequent iteration thereof. If a message is updated, use a new block_id.
        :return: self
        """
        self._block_id = block_id
        self.block["block_id"] = self._block_id
        return self

    def set_text(self, text: str) -> Self:
        """
        Sets the text to be displayed on the header
        :param text: String; max 150 chars
        :return: self
        """
        self._text = Text().set_text(text)
        self.block["text"] = self._text.json
        return self
