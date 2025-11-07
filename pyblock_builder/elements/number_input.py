import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, IncorrectTypeError, RequiredFieldError)
from pyblock_builder.objects import DispatchActionConfig, PlainText

@dataclass
class NumberInput:
    """
    Allows user to enter a number into a single-line field. Accepts both whole and decimal numbers. Decimal numbers
    are only allowed when is_decimal_allowed is equal to true.
    Can be added to: Input
    Works on: Modal
    """
    type: Literal["number_input"] = "number_input"
    is_decimal_allowed: bool = False
    action_id: str | None = None
    initial_value: str | None = None
    min_value: str | None = None
    max_value: str | None = None
    dispatch_action_config: DispatchActionConfig | None = None
    is_focus_on_load: bool | None = None
    placeholder: PlainText | None = None

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
        return  self

    def allow_decimals(self) -> Self:
        """
        (Optional) Allow decimal numbers in inputs.
        :return: self
        """
        self.is_decimal_allowed = True
        return self

    def set_initial_value(self, value: str) -> Self:
        """
        (Optional) Sets the initial value in the plain-text input when it is loaded.
        :param value: str
        :return: self
        """
        if not isinstance(value, str):
            raise IncorrectTypeError(self, method="set_initial_value", compatible_types="str", incompatible_type=value)
        self.initial_value = value
        return self

    def set_min_value(self, min_value: str) -> Self:
        """
        (Optional) Sets the minimum value allowed in the plain-text input.
        :param min_value: str; cannot be greater than max_value
        :return: self
        """
        if not isinstance(min_value, str):
            raise IncorrectTypeError(self, method="set_min_value", compatible_types=str, incompatible_type=min_value)
        self.min_value = min_value
        return self

    def set_max_value(self, max_value: str) -> Self:
        """
        (Optional) Sets the maximum value allowed in the plain-text input.
        :param max_value: str; cannot be less than min_value
        :return: self
        """
        if not isinstance(max_value, str):
            raise IncorrectTypeError(self, method="set_max_value", compatible_types=str, incompatible_type=max_value)
        self.max_value = max_value
        return self

    def set_dispatch_action_config(self, dispatch_action_config: DispatchActionConfig) -> Self:
        """
        (Optional) Adds a dispatch configuration object that determines when during text input the element returns a
        block_actions payload.
        :param dispatch_action_config: DispatchActionConfig object
        :return: self
        """
        if not isinstance(dispatch_action_config, DispatchActionConfig):
            raise IncorrectTypeError(self, method="set_dispatch_action_config", compatible_types=DispatchActionConfig,
                                     incompatible_type=dispatch_action_config)
        self.dispatch_action_config = dispatch_action_config
        return self

    def focus_on_load(self, focus: bool=True) -> Self:
        """
        (Optional) Indicates whether the element will be set to autofocus within the View object. Only one element
        can be set to focus.
        :return: self
        """
        self.is_focus_on_load = focus
        return self

    def set_placeholder_text(self, placeholder_text: PlainText) -> Self:
        """
        (Optional) Sets the placeholder text shown on the number input
        :param placeholder_text: PlainText; max 150 chars
        :return: self
        """
        if not isinstance(placeholder_text, PlainText):
            raise IncorrectTypeError(self, method="set_placeholder_text", compatible_types=PlainText, incompatible_type=placeholder_text)
        if not 1 <= len(placeholder_text.text) <= 150:
            raise TextLengthError(self, field="text", min_length=1, max_length=150)
        self.placeholder = placeholder_text
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.is_decimal_allowed:
            raise RequiredFieldError(self, missing_field_names="is_decimal_allowed")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "is_decimal_allowed": self.is_decimal_allowed,
        }
        if self.action_id:
            data["action_id"] = self.action_id
        if self.initial_value:
            data["initial_value"] = self.initial_value
        if self.min_value:
            data["min_value"] = self.min_value
        if self.max_value:
            data["max_value"] = self.max_value
        if self.min_value and self.max_value:
            if not float(self.min_value) < float(self.max_value):
                raise ValueError("Argument passed to 'set_min_value' method of NumberInput must be less than max_value")
        if self.dispatch_action_config:
            data["dispatch_action_config"] = json.loads(self.dispatch_action_config.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())

        return json.dumps(data)
