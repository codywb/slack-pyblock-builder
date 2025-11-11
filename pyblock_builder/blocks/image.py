import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError)
from pyblock_builder.objects import PlainText, SlackFile

@dataclass
class Image:
    """
    Displays an image.
    Works on: Modal, Message, AppHome
    """
    type: Literal["image"] = "image"
    alt_text: str | None = None
    image_url: str | None = None
    slack_file: SlackFile | None = None
    title: PlainText | None = None
    block_id: str | None = None

    def set_image_url(self, url: str) -> Self:
        """
        Sets the URL of the image to be displayed
        :param url: String; max 3,000 characters
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
        :param alt_text: String; cannot contain any markup, max 2,000 characters
        :return: self
        """
        if not isinstance(alt_text, str):
            raise IncorrectTypeError(self, method="set_alt_text", compatible_types=str, incompatible_type=alt_text)
        if not 1 <= len(alt_text) <= 2000:
            raise TextLengthError(self, field="alt_text", min_length=1, max_length=2000)
        self.alt_text = alt_text
        return  self

    def set_title(self, title: PlainText) -> Self:
        """
        (Optional) Sets the title for the image
        :param title: A PlainText object; max 2,000 characters
        :return: self
        """
        if not isinstance(title, PlainText):
            raise IncorrectTypeError(self, method="set_title", compatible_types=PlainText, incompatible_type=title)
        if not 1 <= len(title.text) <= 75:
            raise TextLengthError(self, field="text", min_length=1, max_length=75)
        self.title = title
        return self

    def set_block_id(self, block_id: str) -> Self:
        """
        (Optional) Sets a unique identifier for a block which can be used when receiving an interaction payload to
        identify the source of an action. If not set, will be auto-generated.
        :param block_id: String; max 255 chars, should be unique for each message and each subsequent iteration thereof.
        If a message is updated, use a new block_id.
        :return: self
        """
        if not isinstance(block_id, str):
            raise IncorrectTypeError(self, method="set_block_id", compatible_types=str, incompatible_type=block_id)
        if not 1 <= len(block_id) <= 255:
            raise TextLengthError(self, field="block_id", min_length=1, max_length=255)
        self.block_id = block_id
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.alt_text:
            raise RequiredFieldError(self, missing_field_names="alt_text")
        if not any([self.image_url, self.slack_file]):
            raise RequiredFieldError(self, missing_field_names=["image_url", "slack_file"])
        if self.image_url and self.slack_file:
            raise TypeError("Setting both 'image_url' and 'slack_file' on an Image element will result in the Slack API rejecting the payload.")
        data: dict[str, Any] = {
            "type": self.type,
            "alt_text": self.alt_text,
        }
        if self.image_url:
            data["image_url"] = self.image_url
        if self.slack_file:
            data["slack_file"] = json.loads(self.slack_file.build_to_json())
        if self.title:
            data["title"] = self.title
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates an Image instance from its JSON representation
        :param json: a JSON representation of an Image block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.block_id = json["block_id"]
        self.alt_text = json["alt_text"]
        if "image_url" in json.keys() and json["image_url"] is not None:
            self.image_url = json["image_url"]
        if "slack_file" in json.keys() and json["slack_file"] is not None:
            self.slack_file = SlackFile().build_from_json(json["slack_file"])
        if "title" in json.keys() and json["title"] is not None:
            self.title = PlainText().build_from_json(json["title"])
        return self