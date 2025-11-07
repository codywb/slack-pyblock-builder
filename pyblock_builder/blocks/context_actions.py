import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder.elements import FeedbackButtons, IconButton
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError,
                                              ItemLengthError)

@dataclass
class ContextActions:
    """
    Displays actions as contextual info, which can include both feedback buttons and icon buttons.
    Works on: Message
    Compatible with: Feedback buttons, Icon button
    """
    type: Literal["context_actions"] = "context_actions"
    block_id: str | None = None
    elements: list[FeedbackButtons | IconButton] = field(default_factory=list)

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

    def add_elements(self, *elements: FeedbackButtons | IconButton | Sequence[FeedbackButtons | IconButton]) -> Self:
        """
        Used to add one or more Feedback buttons or Icon button elements to the block.
        :param elements: One or more Feedback buttons or Icon button elements; maximum of 5 elements per block
        :return: self
        """
        compatible_elements = [FeedbackButtons, IconButton]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        if not 1 <= len(flattened_elements) <= 10:
            raise ItemLengthError(self, field="elements", min_length=1, max_length=5)

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
