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
                self.cells.append(json.loads(cell.build_to_json()))
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.cells:
            raise RequiredFieldError(self, missing_field_names="cells")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        return json.dumps(self.cells)

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
    column_settings: list[dict[Literal["is_wrapped", "align"], bool | str]] | None = field(default_factory=list)

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
                                             Sequence[ ColSettings | dict[Literal["is_wrapped", "align"], bool | str]]) -> Self:
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
            if isinstance(setting, dict):
                self.column_settings.append(setting)
            else:
                self.column_settings.append(json.loads(setting.build_to_json()))
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
            data["column_settings"] = self.column_settings

        return json.dumps(data)
