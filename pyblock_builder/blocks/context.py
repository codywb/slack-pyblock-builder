import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Context:
    """
    A Python class representing a Context block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "context"
        self._block_id = ""
        self._elements = []
        self.block = {
            "type": self._type,
            "elements": self._elements
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

    def add_elements(self, elements) -> Self:
        """
        Used to add one or more interactive elements to the block
        :param elements: Either a single element object or a list of element objects (images or text objects only); maximum of 10 elements per block
        :return: self
        """
        if isinstance(elements, list):
            for element in elements:
                self._elements.append(element.json)
        else:
            self._elements.append(elements.json)
        self.block["elements"] = self._elements
        return self
