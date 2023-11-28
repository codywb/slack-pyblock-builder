import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class File:
    """
    A Python class representing a File block from the Slack BlockKit UI framework\n
    Works on: Message
    """
    def __init__(self):
        self._type = "file"
        self._block_id = ""
        self._external_id = ""
        self._source = "remote"
        self.block = {
            "type": self._type,
            "source": self._source
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

    def set_external_id(self, external_id: str) -> Self:
        """
        Sets the external unique ID for the file
        :param external_id: String
        :return: self
        """
        self._external_id = external_id
        self.block["external_id"] = self._external_id
        return self

    def set_source(self, source: str) -> Self:
        """
        Sets the source of a file
        :param source: String; at the moment, this will always be "remote" for a remote file
        :return: self
        """
        self._source = source
        self.block["source"] = self._source
        return self
