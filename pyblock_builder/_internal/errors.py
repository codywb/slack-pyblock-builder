from dataclasses import dataclass
from typing import Any
from pyblock_builder.base_blocks import Buiildable

@dataclass
class TextLengthError(Exception):
    obj: Buiildable
    field: str
    min_length: int
    max_length: int
    __module__: str = "errors"  # 👈 Fake module name for traceback display

    def __str__(self):
        return (f"'{self.field}' field for {self.obj.__class__.__name__} object must be between {self.min_length} and "
                f"{self.max_length} characters")

@dataclass
class ItemLengthError(Exception):
    obj: Buiildable
    field: str
    min_length: int
    max_length: int
    __module__: str = "errors"  # 👈 Fake module name for traceback display

    def __str__(self):
        return (f"'{self.field}' field for {self.obj.__class__.__name__} object must be between {self.min_length} and "
                f"{self.max_length} items")

@dataclass
class IncorrectTypeError(Exception):
    obj: Buiildable
    method: str
    compatible_types: Any | list[Any]
    incompatible_type: Any

    __module__: str = "errors"

    def __str__(self):
        incompatible_type_name = type(self.incompatible_type).__name__

        if isinstance(self.compatible_types, list):
            if len(self.compatible_types) > 1:
                compatible_types_str = "\n".join(f"- {t.__name__}" for t in self.compatible_types)
            else:
                compatible_types_str = self.compatible_types[0].__name__
        else:
            compatible_types_str = self.compatible_types.__name__

        return (
            f"Incompatible type passed as argument to the '{self.method}' method of {self.obj.__class__.__name__}:\n"
            f"Received: {incompatible_type_name}\n"
            f"Expected one of:\n{compatible_types_str}"
        )

@dataclass
class IncorrectValueError(Exception):
    obj: Buiildable
    method: str
    acceptable_values: str | list[str]
    unacceptable_value: str

    __module__: str = "errors"

    def __str__(self):
        if isinstance(self.acceptable_values, list):
            if len(self.acceptable_values) > 1:
                acceptable_values_str = "\n".join(f"- {s}" for s in self.acceptable_values)
            else:
                acceptable_values_str = self.acceptable_values[0]
        else:
            acceptable_values_str = self.acceptable_values

        return (
            f"Incompatible value passed as argument to '{self.method}' method of {self.obj.__class__.__name__}:\n"
            f"Received: {self.unacceptable_value}\n"
            f"Expected one of:\n{acceptable_values_str}"
        )

@dataclass
class RequiredFieldsError(Exception):
    obj: Buiildable
    missing_field_names: list[str]

    __module__: str = "errors"  # 👈 Fake module name for traceback display

    def __str__(self):
        missing_fields_str = "\n".join(f"- {f}" for f in self.missing_field_names)
        return (
            f"{self.obj.__class__.__name__} requires the following fields to be set:\n"
            f"{missing_fields_str}"
        )

@dataclass
class RequiredFieldError(Exception):
    obj: Buiildable
    missing_field_names: str | list[str]

    __module__: str = "errors"  # 👈 Fake module name for traceback display

    def __str__(self):
        if isinstance(self.missing_field_names, list):
            if len(self.missing_field_names) > 1:
                # list with multiple field names
                missing_fields_str = "\n".join(f"- {f}" for f in self.missing_field_names)
                return (
                    f"{self.obj.__class__.__name__} requires at least one of the following fields to be set:\n"
                    f"{missing_fields_str}"
                )
            else:
                missing_fields_str = self.missing_field_names[0]
        else:
            missing_fields_str = self.missing_field_names

        return (
            f"{self.obj.__class__.__name__} missing required field:\n"
            f"- {missing_fields_str}"
        )
