import sys

if sys.version_info >= (3, 11):
    from typing import Self, Any, Literal
else:
    from typing_extensions import Self, Any, Literal
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (IncorrectTypeError, RequiredFieldError, IncorrectValueError)

@dataclass
class DispatchActionConfig:
    """
    Defines when a plain-text input element will return a block_actions interaction payload.
    """
    trigger_actions_on: list[str] | None = None

    def set_triggers(self, triggers: list[Literal["on_enter_pressed", "on_character_entered"]]) -> Self:
        """
        Sets the interaction types that you would like to receive a block_actions payload for
        :param triggers: Must be one or both of "on_enter_pressed" or "on_character_entered"
        :return: self
        """
        POSSIBLE_TRIGGERS = ["on_enter_pressed", "on_character_entered"]
        if not isinstance(triggers, list):
            raise IncorrectTypeError(self, method="set_triggers", compatible_types=list, incompatible_type=triggers)
        for trigger in triggers:
            if trigger not in POSSIBLE_TRIGGERS:
                raise IncorrectValueError(self, method="set_triggers", acceptable_values=POSSIBLE_TRIGGERS,
                                          unacceptable_value=trigger)
        self.trigger_actions_on = triggers
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.trigger_actions_on:
            raise RequiredFieldError(self, missing_field_names="trigger_actions_on")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {}
        if self.trigger_actions_on:
            data["trigger_actions_on"] = self.trigger_actions_on

        return json.dumps(data)
