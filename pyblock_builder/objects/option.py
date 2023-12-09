import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Option:
    """
    A Python class representing an Option object from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._text = {}
        self._value = ""
        self._description = None
        self._url = None
        self.json = {
            "text": self._text,
            "value": self._value
        }

    def set_text(self, text: str, mrkdwn=False) -> Self:
        """
        (Required) Sets the text shown in the option on the menu
        :param text: String, max 75 chars
        :param mrkdwn: Boolean; defaults to False -- must be False for Overflow, Select, and Multi-Select Menus, can be True for Radio Buttons and Checkboxes
        :return: self
        """
        if not mrkdwn:
            self._text = Text().set_text(text)
        else:
            self._text = Text().set_text(text).as_mrkdwn()
        self.json["text"] = self._text.json
        return self

    def set_value(self, value: str) -> Self:
        """
        (Required) Sets the value to be passed to your app when the option is chosen
        :param value: String; max 75 chars
        :return: self
        """
        self._value = value
        self.json["value"] = self._value
        return self

    def set_url(self, target_url: str) -> Self:
        """
        (Optional) Sets the url to be opened when a user clicks the option. Only available in overflow menus!
        :param target_url: String; max 3,000 chars, still requires an ack() response to the Slack API
        :return: self
        """
        self._url = target_url
        self.json["url"] = self._url
        return self

    def set_description(self, descriptive_text: str) -> Self:
        """
        (Optional) Sets the text to be shown below the Option's text beside a radio button
        :param descriptive_text: String; max 75 chars
        :return: self
        """
        self._description = Text().set_text(descriptive_text)
        self.json["description"] = self._description.json
        return self
