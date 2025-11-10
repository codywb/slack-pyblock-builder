import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, IncorrectTypeError, ValueLengthError)

@dataclass
class FileInput:
    """
    Allows user to upload files.
    Can be added to: Input
    Works on: Modal
    """
    type: Literal["file_input"] = "file_input"
    action_id: str | None = None
    filetypes: list[str] = field(default_factory=list)
    max_files: int | None = None

    def set_action_id(self, action_id: str) -> Self:
        """
        Sets the action_id of the Block element which identifies the source of the action in the JSON payload
        :param action_id: String; must be unique within a single block, max 255 chars
        :return: self
        """
        if not isinstance(action_id, str):
            raise IncorrectTypeError(self, method="set_action_id", compatible_types=str, incompatible_type=action_id)
        if not 1 <= len(action_id) <= 255:
            raise TextLengthError(self, field="action_id", min_length=1, max_length=255)
        self.action_id = action_id
        return self

    def set_filetypes(self, filetypes: list[str]) -> Self:
        """
        Sets an array of valid file extensions that will be accepted for this element.
        All file extensions will be accepted if filetypes is not specified.
        :param filetypes: list of strings
        :return: self
        """
        if not isinstance(filetypes, list):
            raise IncorrectTypeError(self, method="set_filetypes", compatible_types=list[str], incompatible_type=filetypes)
        if isinstance(filetypes, list):
            for filetype in filetypes:
                if not isinstance(filetype, str):
                    raise TypeError("Non-string value included in filetypes list passed as argument to the 'set_filetypes' method of FileInput")
        self.filetypes = filetypes
        return self

    def set_max_files(self, max_files: int = 10) -> Self:
        """
        Sets the Maximum number of files that can be uploaded for this file_input element. Defaults to 10 if not specified.
        :param max_files: integer
        :return: self
        """
        if not isinstance(max_files, int):
            raise IncorrectTypeError(self, method="set_max_files", compatible_types=int, incompatible_type=max_files)
        if not 1 <= max_files <= 10:
            raise ValueLengthError(self, field="max_files", min_length=1, max_length=10)

    def build_to_json(self) -> str:
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
        }
        if self.action_id:
            data["action_id"] = self.action_id
        if self.filetypes:
            data["filetypes"] = self.filetypes
        if self.max_files:
            data["max_files"] = self.max_files

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates an FileInput instance from its JSON representation
        :param json: a JSON representation of an FileInput element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "action_id" in json.keys() and json["action_id"] is not None:
            self.action_id = json["action_id"]
        if "filetypes" in json.keys() and json["filetypes"] is not None:
            self.filetypes = json["filetypes"]
        if "max_files" in json.keys() and json["max_files"] is not None:
            self.max_files = json["max_files"]
        return self
