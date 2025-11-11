import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError, IncorrectValueError)

@dataclass
class File:
    """
    Displays info about remote files.
    Works on: Message
    """
    type: Literal["file"] = "file"
    external_id: str | None = None
    source: str | None = "remote"
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

    def set_external_id(self, external_id: str) -> Self:
        """
        Sets the external unique ID for the file
        :param external_id: String
        :return: self
        """
        if not isinstance(external_id, str):
            raise IncorrectTypeError(self, method="set_external_id", compatible_types=str, incompatible_type=external_id)
        self.external_id = external_id
        return self

    def set_source(self, source: str) -> Self:
        """
        Sets the source of a file
        :param source: String; at the moment, this will always be "remote" for a remote file
        :return: self
        """
        if not isinstance(source, str):
            raise IncorrectTypeError(self, method="set_source", compatible_types=str, incompatible_type=source)
        if self.source != "remote": # may be updated in later versions to accept other values
            raise IncorrectValueError(self, method="set_source", acceptable_values="remote", unacceptable_value=source)
        self.source = source
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.external_id, self.source]]):
            raise RequiredFieldsError(self, missing_field_names=["external_id", "source"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "external_id": self.external_id,
            "source": self.source,
        }
        if self.block_id:
            data["block_id"] = self.block_id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a File instance from its JSON representation
        :param json: a JSON representation of a File block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "block_id" in json.keys() and json["block_id"] is not None:
            self.block_id = json["block_id"]
        self.external_id = json["external_id"]
        self.source = json["source"]
        return self
