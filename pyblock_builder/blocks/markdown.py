import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import TextLengthError, IncorrectTypeError

@dataclass
class Markdown:
    """
    Displays formatted markdown.
    Works on: Message
    """
    type: Literal["markdown"] = "markdown"
    text: str | None = None
    block_id: str | None = None

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

    def set_text(self, markdown_text: str) -> Self:
        """
        Defines the standard markdown-formatted text to be displayed.
        :param markdown_text: string; max 12,000 characters
        :return: self
        """
        if not isinstance(markdown_text, str):
            raise IncorrectTypeError(self, method="set_text", compatible_types=str, incompatible_type=markdown_text)
        self.text = markdown_text
        return self

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "text": self.text,
        }
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Markdown instance from its JSON representation
        :param json: a JSON representation of a Markdown block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.block_id = json["block_id"]
        self.text = json["text"]
        return self