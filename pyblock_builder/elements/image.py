import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError,
                                              RequiredFieldError)
from pyblock_builder.objects import SlackFile

@dataclass
class Image:
    """
    A Python class representing an Image element from the Slack BlockKit UI framework
    Can be added to: Section, Context
    Works on: Modal, Message, AppHome
    """
    type: Literal["image"] = "image"
    image_url: str | None = None
    alt_text: str | None = None
    slack_file: SlackFile | None = None

    def set_image_url(self, url: str) -> Self:
        """
        Sets the URL of the image to be displayed
        :param url: String
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_url", compatible_types=str, incompatible_type=url)
        if not 1 <= len(url) <= 3000:
            raise TextLengthError(self, field="url", min_length=1, max_length=3000)
        self.image_url = url
        return  self

    def add_slack_file(self, slack_file: SlackFile) -> Self:
        """
        Add a SlackFile representation of an image instead of a URL
        :param slack_file: SlackFile object
        :return: self
        """
        if not isinstance(slack_file, SlackFile):
            raise IncorrectTypeError(self, method="add_slack_file", compatible_types=SlackFile, incompatible_type=slack_file)
        self.slack_file = slack_file
        return self

    def set_alt_text(self, alt_text: str) -> Self:
        """
        (Required) Sets the text summary of the image
        :param alt_text: String; cannot contain any markup
        :return: self
        """
        if not isinstance(alt_text, str):
            raise IncorrectTypeError(self, method="set_alt_text", compatible_types=str, incompatible_type=alt_text)
        self.alt_text = alt_text
        return  self

    def build_to_json(self) -> str:
        if None in [self.type, self.alt_text]:
            raise RequiredFieldsError(self, missing_field_names=["type", "alt_text"])
        if not any([self.image_url, self.slack_file]):
            raise RequiredFieldError(self, missing_field_names=["image_url", "slack_file"])
        if self.image_url and self.slack_file:
            raise TypeError("Setting both 'image_url' and 'slack_file' on an Image element will result in the Slack API rejecting the payload.")
        data = {
            "type": self.type,
            "alt_text": self.alt_text,
        }
        if self.image_url:
            data["image_url"] = self.image_url
        if self.slack_file:
            data["slack_file"] = json.loads(self.slack_file.build_to_json())

        return json.dumps(data)
