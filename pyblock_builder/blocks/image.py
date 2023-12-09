import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Image:
    """
    A Python class representing an Image block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "image"
        self._block_id = ""
        self._image_url = ""
        self._alt_text = ""
        self._title = None
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

    def set_image_url(self, url: str) -> Self:
        """
        Sets the URL of the image to be displayed
        :param url: String; max 3,000 chars
        :return: self
        """
        self._image_url = url
        self.block["image_url"] = self._image_url
        return self

    def set_alt_text(self, alt_text: str) -> Self:
        """
        Sets the text summary of the image
        :param alt_text: String; cannot contain any markup, max 2,000 chars
        :return: self
        """
        self._alt_text = alt_text
        self.block["alt_text"] = self._alt_text
        return self

    def set_title(self, title_text: str) -> Self:
        """
        (Optional) Sets the title for the image
        :param title_text: String; max 2,000 chars
        :return: self
        """
        self._title = Text().set_text(title_text)
        self.block["title"] = self._title.json
        return self

