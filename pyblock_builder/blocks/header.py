import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder.objects import PlainText
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError)

@dataclass
class Header:
    """
    Displays a larger-sized text.\n
    Works on: Modal, Message, AppHome
    """
    type: Literal["header"] = "header"
    text: PlainText | None = None
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

    def set_text(self, text: PlainText) -> Self:
        """
        Sets the text to be displayed on the block
        :param text: PlainText; max 150 chars
        :return: self
        """
        if not isinstance(text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=text)
        if not 1 <= len(text.text) <= 150:
            raise TextLengthError(self, field="text", min_length=1, max_length=150)
        self.text = text
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.text:
            raise RequiredFieldError(self, missing_field_names="text")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "text": json.loads(self.text.build_to_json()),
        }
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)
