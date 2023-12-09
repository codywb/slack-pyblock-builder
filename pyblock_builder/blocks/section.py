import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Section:
    """
    A Python class representing a Section block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "section"
        self._block_id = ""
        self._text = ""
        self._fields = None
        self._accessory = None
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

    def set_text(self, text, mrkdwn=True) -> Self:
        """
        (Preferred) Sets the text for the block. Not required if a list of fields objects is provided.
        :param text: String or Text object; max 3,000 chars
        :param mrkdwn: Boolean; defaults to True
        :return: self
        """
        if not mrkdwn:
            if not isinstance(text, str):
                self._text = text
            else:
                self._text = Text().set_text(text)
        else:
            if not isinstance(text, str):
                if text._type == "mrkdwn":
                    self._text = text
                else:
                    self._text = text.as_mrkdwn()
            else:
                self._text = Text().set_text(text).as_mrkdwn()
        self.block["text"] = self._text.json
        return self

    def set_fields(self, fields_obj) -> Self:
        """
        (Maybe) Required if self.text not set. Any text included will be rendered in a compact format allowing for 2
        columns of side-by-side text.
        :param fields_obj: Fields object; max number of fields is 10, max chars per field is 2,000
        :return: self
        """
        self._fields = fields_obj.fields
        self.block["fields"] = self._fields
        return self

    def add_accessory(self, accessory) -> Self:
        """
        (Optional) Can be used to add an element block to a section.
        :param accessory: One of the available element objects
        :return: Nothing
        """
        self._accessory = accessory
        self.block["accessory"] = self._accessory.json
        return self
