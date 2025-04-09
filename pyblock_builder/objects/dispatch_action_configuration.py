import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (RequiredFieldError, IncorrectTypeError, IncorrectValueError)

@dataclass
class DispatchActionConfig:
    trigger_actions_on: list[str] | None = None

    def set_triggers(self, triggers: list[str]) -> Self:
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
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {}
        if self.trigger_actions_on:
            data["trigger_actions_on"] = self.trigger_actions_on

        return json.dumps(data)
#
# class DispatchActionConfig:
#     """
#     A Python class representing a Dispatch action configuration from the Slack BlockKit UI framework
#     """
#     def __init__(self):
#         self._trigger_actions_on = []
#         self.json = {
#             "trigger_actions_on": self._trigger_actions_on
#         }
#
#     def set_triggers(self, *triggers) -> Self:
#         """
#         Sets the interaction types that you would like to receive a block_actions payload for
#         :param triggers: Must be one or both of "on_enter_pressed" or "on_character_entered"; preface with * if passing in a list
#         :return: self
#         """
#         for trigger in triggers:
#             self._trigger_actions_on.append(trigger)
#         self.json["trigger_actions_on"] = self._trigger_actions_on
#         return self
