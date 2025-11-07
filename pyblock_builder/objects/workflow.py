import sys

if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import RequiredFieldError, IncorrectTypeError
from pyblock_builder.objects import Trigger

@dataclass
class Workflow:
    """
    Defines an object containing workflow information.
    """
    trigger: Trigger | None = None

    def set_trigger(self, trigger: Trigger) -> Self:
        """
        Sets the trigger for a workflow.
        :param trigger: Trigger object
        :return: self
        """
        if not isinstance(trigger, Trigger):
            raise IncorrectTypeError(self, method="set_trigger", compatible_types=Trigger, incompatible_type=trigger)
        self.trigger = trigger
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.trigger:
            raise RequiredFieldError(self, missing_field_names="trigger")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "trigger": self.trigger
        }

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Workflow instance from its JSON representation
        :param json: a JSON representation of a Workflow object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.trigger = Trigger().build_from_json(json["trigger"])
        return self
