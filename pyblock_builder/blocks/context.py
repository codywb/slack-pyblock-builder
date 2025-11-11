import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder.elements import Image
from pyblock_builder.objects import PlainText, MrkdwnText
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError,
                                              ItemLengthError)

@dataclass
class Context:
    """
    Holds image elements and text objects to display under other blocks.
    Works on: Modal, Message, AppHome
    """
    type: Literal["context"] = "context"
    block_id: str | None = None
    elements: list[Image | PlainText | MrkdwnText] = field(default_factory=list)

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

    def add_elements(self, *elements: Image | PlainText | MrkdwnText | Sequence[Image | PlainText | MrkdwnText]) -> Self:
        """
        Used to add one or more image elements or text objects to the block.
        :param elements: One or more image elements or text objects; maximum of 10 elements per block
        :return: self
        """
        compatible_elements = [Image, PlainText, MrkdwnText]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        if not 1 <= len(flattened_elements) <= 10:
            raise ItemLengthError(self, field="elements", min_length=1, max_length=10)

        for element in flattened_elements:
            if not isinstance(element, tuple(compatible_elements)):
                raise IncorrectTypeError(self, method="add_elements", compatible_types=compatible_elements,
                                         incompatible_type=element)
            self.elements.append(element)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.elements:
            raise RequiredFieldError(self, missing_field_names="elements")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "elements": [json.loads(element.build_to_json()) for element in self.elements],
        }
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Context instance from its JSON representation
        :param json: a JSON representation of a Context block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.block_id = json["block_id"]
        compatible_types = {
            "image": Image,
            "plain_text": PlainText,
            "mrkdwn_text": MrkdwnText,
        }
        self.elements = [compatible_types[element["type"]]().build_from_json(element) for element in json["elements"]]
        return self