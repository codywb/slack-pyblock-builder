import sys

from pyblock_builder.blocks import RichText

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import TextLengthError, IncorrectTypeError, RequiredFieldError, ItemLengthError

@dataclass
class ColSettings:
    """
    A simple object for defining column settings in a Table block. Defaults to left-aligned and no wrapping.
    """
    align: Literal["right", "center", "left"] = "left"
    is_wrapped: bool = False

    def build_to_json(self):
        if self.align not in ["right", "left", "center"]:
            raise ValueError("'align' parameter of ColSettings must be one of 'right', 'center', or 'left'")
        if self.is_wrapped not in [True, False]:
            raise ValueError("'is_wrapped' parameter of ColSettings must be either 'True' or 'False'")
        data: dict[str, Any] = {
            "align": self.align,
            "is_wrapped": self.is_wrapped
        }

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a ColSettings instance from its JSON representation
        :param json: a JSON representation of a ColSettings object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "align" in json.keys():
            self.align = json["align"]
        if "is_wrapped" in json.keys():
            self.is_wrapped = json["is_wrapped"]
        return self

@dataclass
class Row:
    """
    A simple object for defining a rows in a Table block.
    """
    cells: list[RichText | dict[str, str]] | None = field(default_factory=list)

    def add_cells(self, *cells: RichText | str | Sequence[RichText | str]) -> Self:
        """
        Add one or more cells to a row in the Table block.
        :param rows: one or more RichText objects or strings or a list/tuple of RIchText objects and strings
        :return: self
        """
        flattened_cells = []
        for cell in cells:
            if isinstance(cell, (list, tuple)):
                flattened_cells.extend(cell)
            else:
                flattened_cells.append(cell)

        if not 1 <= len(flattened_cells) <= 20:
            raise Exception("Each row of a Table block must have no more than 20 cells.")

        for cell in flattened_cells:
            if not isinstance(cell, (RichText, str)):
                raise IncorrectTypeError(self, method="add_cells", compatible_types=[RichText, str],
                                         incompatible_type=cell)
            if isinstance(cell, str):
                cell = {"type": "raw_text", "text": cell}
                self.cells.append(cell)
            else:
                self.cells.append(cell)
                # self.cells.append(json.loads(cell.build_to_json()))
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.cells:
            raise RequiredFieldError(self, missing_field_names="cells")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "cells": [json.loads(cell.build_to_json()) if isinstance(cell, RichText) else cell for cell in self.cells]
        }

        return json.dumps(data)

    def build_from_json(self, json: list[dict[str, Any]]) -> Self:
        """
        Generates a Row instance from its JSON representation
        :param json: a JSON representation of a Row object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, list):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=list, incompatible_type=json)
        self.cells = [RichText().build_from_json(cell) if cell["type"] == "rich_text" else cell for cell in json]
        return self

@dataclass
class Table:
    """
    Displays structured information in a table.
    Works on: Message
    Compatible with: RichText blocks, ColSettings
    """
    type: Literal["table"] = "table"
    block_id: str | None = None
    rows: list[Row] | None = field(default_factory=list)
    column_settings: list[ColSettings | dict[Literal["is_wrapped", "align"], bool | str]] | None = field(default_factory=list)

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

    def add_rows(self, *rows: Row | Sequence[Row]) -> Self:
        """
        Add one or more rows to the Table block.
        :param rows: one or more Row objects or a list/tuple of Row objects
        :return: self
        """
        flattened_rows = []
        for row in rows:
            if isinstance(row, (list, tuple)):
                flattened_rows.extend(row)
            else:
                flattened_rows.append(row)

        if not 1 <= len(flattened_rows) <= 100:
            raise ItemLengthError(self, field="rows", min_length=1, max_length=100, )

        for row in flattened_rows:
            if not isinstance(row, Row):
                raise IncorrectTypeError(self, method="add_rows", compatible_types=Row,
                                         incompatible_type=row)
            self.rows.append(row)
        return self

    def set_column_settings(self, *settings: ColSettings | dict[Literal["is_wrapped", "align"], bool | str] |
                                             Sequence[ColSettings | dict[Literal["is_wrapped", "align"], bool | str]]) -> Self:
        """
        Defines an array describing column behavior. If there are fewer items in the column_settings array than there
        are columns in the table, then the items in the column_settings array will describe the same number of columns
        in the table as there are in the array itself. Any additional columns will have the default behavior.
        :param settings: one or more ColSettings objects or dicts or a list/tuple of ColSettings objects or dicts
        :return: self
        """
        flattened_settings = []
        for setting in settings:
            if isinstance(setting, (list, tuple)):
                flattened_settings.extend(setting)
            else:
                flattened_settings.append(setting)

        if not 1 <= len(flattened_settings) <= 20:
            raise Exception("The 'set_column_settings' method of the Table block must be passed between 1 and 20 items.")

        for setting in flattened_settings:
            if not isinstance(setting, (ColSettings, dict)):
                raise IncorrectTypeError(self, method="set_column_settings", compatible_types=[ColSettings, dict],
                                         incompatible_type=setting)
            self.column_settings.append(setting)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.rows:
            raise RequiredFieldError(self, missing_field_names="rows")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "rows": [json.loads(row.build_to_json()) for row in self.rows]
        }
        if self.block_id:
            data["block_id"] = self.block_id
        if self.column_settings:
            data["column_settings"] = [json.loads(setting.build_to_json()) if isinstance(setting, ColSettings) else setting for setting in self.column_settings]

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Table instance from its JSON representation
        :param json: a JSON representation of a Table block, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "block_id" in json.keys() and json["block_id"] is not None:
            self.block_id = json["block_id"]
        self.rows = [Row().build_from_json(row) for row in json["rows"]]
        if "column_settings" in json.keys() and json["column_settings"] is not None:
            self.column_settings = [ColSettings().build_from_json(setting) for setting in json["column_settings"]]
        return self
