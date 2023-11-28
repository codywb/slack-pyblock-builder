import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class ImageElement:
    """
    A Python class representing an Image element from the Slack BlockKit UI framework\n
    Can be added to: Section, Context
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = "image"
        self._image_url = ""
        self._alt_text = ""
        self.json = {
            "type": self._type,
            "image_url": self._image_url,
            "alt_text": self._alt_text
        }

    def set_image_url(self, url: str) -> Self:
        """
        (Required) Sets the URL of the image to be displayed
        :param url: String
        :return: self
        """
        self._image_url = url
        self.json["image_url"] = self._image_url
        return self

    def set_alt_text(self, alt_text: str) -> Self:
        """
        (Required) Sets the text summary of the image
        :param alt_text: String; cannot contain any markup
        :return: self
        """
        self._alt_text = alt_text
        self.json["alt_text"] = self._alt_text
        return self
