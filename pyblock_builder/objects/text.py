import sys
if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass, asdict
import json
from pyblock_builder._internal.errors import TextLengthError, RequiredFieldError, IncorrectTypeError

@dataclass
class Text:
    """
    Defines an object containing some text.
    """
    text: str | None = None

    def set_text(self, text: str) -> Self:
        """
        Sets the text for the block. MrkdwnText objects May include Slack standard text formatting markup.
        :param text: String; must be between 1 and 3,000 characters.
        :return: self
        """
        if not isinstance(text, str):
            raise IncorrectTypeError(self, method="set_text", compatible_types=str, incompatible_type=text)
        if not 1 <= len(text) <= 3000:
            raise TextLengthError(self, field="text", min_length=1, max_length=3000)
        self.text = text
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.text:
            raise RequiredFieldError(self, missing_field_names="text")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        return json.dumps({k.replace("_", ""): v for k, v in asdict(self).items() if v is not None})


@dataclass
class PlainText(Text):
    """
    Defines an object containing some text formatted as plain_text.
    """
    type: str = "plain_text"
    emoji: bool | None = True

    def disable_emojis(self) -> Self:
        """
        (Optional) Indicates whether emojis in text should be escaped into the colon emoji format.
        :return: self
        """
        self.emoji = False
        return self

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a PlainText instance from its JSON representation
        :param json: a JSON representation of a PlainText object, e.g. from the 'text' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if not json["type"] == "plain_text":
            raise TypeError("The 'build_from_json' method of the PlainText object requires a text object with a type of 'plain_text'.")
        if json["text"]:
            self.text = json["text"]
        if json["emoji"]:
            self.emoji = json["emoji"]
        return self

@dataclass
class MrkdwnText(Text):
    """
    Defines an object containing some text formatted as proprietary Slack mrkdwn.
    """
    type: str = "mrkdwn"
    verbatim: bool | None = False

    def is_verbatim(self) -> Self:
        """
        (Optional) Indicates whether text should be preprocessed for links, conversation names, mentions,
        etc.
        :return: self
        """
        self.verbatim = True
        return self

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a MrkdwnText instance from its JSON representation
        :param json: a JSON representation of a MrkdwnText object, e.g. from the 'text' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if not json["type"] == "mrkdwn":
            raise TypeError("The 'build_from_json' method of the MrkdwnText object requires a text object with a type of 'mrkdwn'.")
        if json["text"]:
            self.text = json["text"]
        if json["verbatim"]:
            self.verbatim = json["verbatim"]
        return self