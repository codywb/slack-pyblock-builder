from dataclasses import dataclass
from pyblock_builder.base_blocks import Buiildable

@dataclass
class FieldLengthError(Exception):
    obj: Buiildable
    field: str
    min_length: int
    max_length: int

    def __str__(self):
        return f"'{self.field}' field for {self.obj.__class__.__name__} object must be between {self.min_length} and {self.max_length} characters"


@dataclass
class RequiredFieldError(Exception):
    obj: Buiildable
    field_names: str | list[str]

    def __str__(self):
        if isinstance(self.field_names, list):
            if len(self.field_names) > 1:
                # list with multiple field names
                missing_fields = "', '".join(self.field_names)
                return f"{self.obj.__class__.__name__} object requires one of the following fields be set: '{missing_fields}'"
            else:
                # List with one field name
                return f"{self.obj.__class__.__name__} object missing required field: '{self.field_names}'"
        else:
            # single field name as string
            return f"{self.obj.__class__.__name__} object missing required field: '{self.field_names}'"

