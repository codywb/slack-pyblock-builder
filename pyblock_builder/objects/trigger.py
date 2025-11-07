import sys

if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import RequiredFieldError, IncorrectTypeError

@dataclass
class Trigger:
    """
    Defines an object containing trigger information.
    """
    url: str | None = None
    customizable_input_parameters: list[dict] | None = None

    def set_trigger_url(self, url: str) -> Self:
        """
        Sets A link trigger URL. Must be associated with a valid trigger.
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_trigger_url", compatible_types=str, incompatible_type=url)
        self.url = url
        return self

    def set_customizable_input_parameters(self, input_params: list[dict]) -> Self:
        """
        Sets an array of input parameter objects.
        :param input_params: A list of dicts with names and values
        :return: self
        """
        if not isinstance(input_params, list):
            raise IncorrectTypeError(self, method="set_customizable_input_parameters", compatible_types=list[dict], incompatible_type=input_params)
        self.customizable_input_parameters = input_params
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.url:
            raise RequiredFieldError(self, missing_field_names="url")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "url": self.url
        }
        if self.customizable_input_parameters:
            data["customizable_input_parameters"] = self.customizable_input_parameters

        return json.dumps(data)
