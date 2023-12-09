import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Video:
    """
    A Python class representing a Video block from the Slack BlockKit UI framework\n
    Works on: Modal, Message, AppHome
    """
    def __init__(self):
        self._type = 'video'
        self._block_id = ""
        self._alt_text = ""
        self._author_name = ""
        self._description = None
        self._provider_icon_url = ""
        self._provider_name = ""
        self._title = None
        self._title_url = ""
        self._thumbnail_url = ""
        self._video_url = ""
        self.block = {
            "type": self.type,
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

    def set_alt_text(self, alt_text: str) -> Self:
        """
        (Required) Sets a tooltip for the video. Required for accessibility
        :param alt_text: String
        :return: self
        """
        self._alt_text = alt_text
        self.block["alt_text"] = self._alt_text
        return self

    def set_author_name(self, author_name: str) -> Self:
        """
        (Optional) Sets author name to be displayed
        :param author_name: String; must be less than 50 characters
        :return: self
        """
        self._author_name = author_name
        self.block["author_name"] = self._author_name
        return self

    def set_description(self, descriptive_text: str) -> Self:
        """
        (Optional) Sets the text to be shown above the video
        :param descriptive_text: String
        :return: self
        """
        self._description = Text().set_text(descriptive_text)
        self.block["description"] = self._description.json
        return self

    def set_provider_icon_url(self, provider_icon_url: str) -> Self:
        """
        (Optional) Sets the icon for the video provider, e.g. YouTube icon
        :param provider_icon_url: String
        :return: self
        """
        self._provider_icon_url = provider_icon_url
        self.block["provider_icon_url"] = self._provider_icon_url
        return self

    def set_provider_name(self, provider_name: str) -> Self:
        """
        (Optional) Sets the originating application or domain of the video, e.g. YouTube
        :param provider_name: String
        :return: self
        """
        self._provider_name = provider_name
        self.block["provider_name"] = self._provider_name
        return self

    def set_title(self, title_text: str) -> Self:
        """
        (Required) Set the video title
        :param title_text: String; must be less than 200 characters
        :return: self
        """
        self._title = Text().set_text(title_text)
        self.block["title"] = self._title.json
        return self

    def set_title_url(self, title_url: str) -> Self:
        """
        (Preferred) Sets the hyperlink for the title text. Must correspond to the non-embeddable URL for the video.
        Must go to an HTTPS URL.
        :param title_url: String
        :return: self
        """
        self._title_url = title_url
        self.block["title_url"] = self._title_url
        return self

    def set_thumbnail_url(self, thumbnail_url: str) -> Self:
        """
        (Required) Sets the thumbnail image URL
        :param thumbnail_url: String
        :return: self
        """
        self._thumbnail_url = thumbnail_url
        self.block["thumbnail_url"] = self._thumbnail_url
        return self

    def set_video_url(self, video_url: str) -> Self:
        """
        (Required) Sets the URL to be embedded. Must match any existing unfurl domains within the app and point to a
        HTTPS URL.
        :param video_url: String
        :return: self
        """
        self._video_url = video_url
        self.block["video_url"] = self._video_url
        return self
