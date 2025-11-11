import sys

from pyblock_builder.objects import PlainText

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import TextLengthError, IncorrectTypeError, RequiredFieldsError

@dataclass
class Video:
    """
    Displays an embedded video player.
    Works on: Modal, Message, AppHome
    """
    type: Literal["video"] = "video"
    alt_text: str | None = None
    author_name: str | None = None
    block_id: str | None = None
    description: PlainText | None = None
    provider_icon_url: str | None = None
    provider_name: str | None = None
    title: PlainText | None = None
    title_url: str | None = None
    thumbnail_url: str | None = None
    video_url: str | None = None

    def set_alt_text(self, alt_text: str) -> Self:
        """
        Sets the tooltip for the video. Required for accessibility
        :param alt_text: String
        :return: self
        """
        if not isinstance(alt_text, str):
            raise IncorrectTypeError(self, method="set_alt_text", compatible_types=str, incompatible_type=alt_text)
        self.alt_text = alt_text
        return  self

    def set_author_name(self, name: str) -> Self:
        """
        (Optional) Sets the author name to be displayed.
        :param alt_text: String; must be less than 50 characters
        :return: self
        """
        if not isinstance(name, str):
            raise IncorrectTypeError(self, method="set_author_name", compatible_types=str, incompatible_type=name)
        if not 1 <= len(name) < 50:
            raise TextLengthError(self, field="author_name", min_length=1, max_length=49)
        self.author_name = name
        return  self

    def set_provider_name(self, name: str) -> Self:
        """
        (Optional) Sets the name of the  originating application or domain of the video (e.g. YouTube).
        :param alt_text: String
        :return: self
        """
        if not isinstance(name, str):
            raise IncorrectTypeError(self, method="set_provider_name", compatible_types=str, incompatible_type=name)
        if not 1 <= len(name) < 50:
            raise TextLengthError(self, field="provider_name", min_length=1, max_length=49)
        self.provider_name = name
        return  self

    def set_title(self, title_text: PlainText) -> Self:
        """
        Sets the title of the video.
        :param description_text: PlainText object; must be less than 200 characters
        :return: self
        """
        if not isinstance(title_text, PlainText):
            raise IncorrectTypeError(self, method="set_title", compatible_types=PlainText, incompatible_type=title_text)
        if not 1 <= len(title_text.text) < 200:
            raise TextLengthError(self, field="text", min_length=1, max_length=199)
        self.title = title_text
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

    def set_description(self, description_text: PlainText) -> Self:
        """
        (Preferred) Sets the description for the video.
        :param description_text: PlainText object; must be less than 200 characters
        :return: self
        """
        if not isinstance(description_text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=description_text)
        if not 1 <= len(description_text.text) < 200:
            raise TextLengthError(self, field="text", min_length=1, max_length=199)
        self.description = description_text
        return self

    def set_provider_icon_url(self, url: str) -> Self:
        """
        (Optional) Sets the URL of the icon for the video provider (e.g. YouTube)
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_provider_icon_url", compatible_types=str, incompatible_type=url)
        self.provider_icon_url = url
        return  self

    def set_video_url(self, url: str) -> Self:
        """
        Sets the URL of the video to be embedded. Must match any existing unfurl domains within the app and point to an
        HTTPS URL.
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_video_url", compatible_types=str, incompatible_type=url)
        self.video_url = url
        return  self

    def set_title_url(self, url: str) -> Self:
        """
        (Preferred) Sets the hyperlink for the title text. Must correspond to the non-embeddable URL for the video.
        Must go to an HTTPS URL.
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_title_url", compatible_types=str, incompatible_type=url)
        self.title_url = url
        return  self

    def set_thumbnail_url(self, url: str) -> Self:
        """
        Sets the URL of the thumbnail image to be displayed.
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_thumbnail_url", compatible_types=str, incompatible_type=url)
        self.thumbnail_url = url
        return  self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.alt_text, self.title, self.thumbnail_url, self.video_url]]):
            raise RequiredFieldsError(self, missing_field_names=["alt_text", "title", "thumbnail_url", "video_url"])
        data: dict[str, Any] = {
            "type": self.type,
            "alt_text": self.alt_text,
            "title": json.loads(self.title.build_to_json()),
            "thumbnail_url": self.thumbnail_url,
            "video_url": self.video_url,
        }
        if self.author_name:
            data["author_name"] = self.author_name
        if self.block_id:
            data["block_id"] = self.block_id
        if self.description:
            data["description"] = json.loads(self.description.build_to_json())
        if self.provider_icon_url:
            data["provider_icon_url"] = self.provider_icon_url
        if self.provider_name:
            data["provider_name"] = self.provider_name
        if self.title_url:
            data["title_url"] = self.title_url

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Video instance from its JSON representation
        :param json: a JSON representation of a Video block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.block_id = json["block_id"]
        self.alt_text = json["alt_text"]
        self.title = PlainText().build_from_json(json["title"])
        self.thumbnail_url = json["thumbnail_url"]
        self.video_url = json["video_url"]
        if "author_name" in json.keys() and json["author_name"] is not None:
            self.author_name = json["author_name"]
        if "provider_icon_url" in json.keys() and json["provider_icon_url"] is not None:
            self.provider_icon_url = json["provider_icon_url"]
        if "provider_name" in json.keys() and json["provider_name"] is not None:
            self.provider_name = json["provider_name"]
        if "title_url" in json.keys() and json["title_url"] is not None:
            self.title_url = json["title_url"]
        if "description" in json.keys() and json["description"] is not None:
            self.description = PlainText().build_from_json(json["description"])
        return self
