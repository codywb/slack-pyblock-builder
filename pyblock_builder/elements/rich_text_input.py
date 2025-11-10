from __future__ import annotations
import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, TYPE_CHECKING
else:
    from typing_extensions import Self, Literal, Any, TYPE_CHECKING
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, IncorrectTypeError, RequiredFieldError)
from pyblock_builder.objects import DispatchActionConfig, PlainText
if TYPE_CHECKING:
    from pyblock_builder.blocks import RichText

@dataclass
class RichTextInput:
    """
    Allows users to enter formatted text in a WYSIWYG composer, offering the same messaging writing experience as in
    Slack.
    Can be added to: Input
    Works on: Modal, AppHome
    """
    type: Literal["rich_text_input"] = "rich_text_input"
    action_id: str | None = None
    initial_value: RichText | None = None
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
        return self

    def set_initial_value(self, value: RichText) -> Self:
        """
        (Optional) Sets the initial value in the rich text input when it is loaded.
        :param value: a RichTextObject
        :return: self
        """
        from pyblock_builder.blocks import RichText
        if not isinstance(value, RichText):
            raise IncorrectTypeError(self, method="set_initial_value", compatible_types=RichText, incompatible_type=value)
        self.initial_value = value
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
        if not self.action_id:
            raise RequiredFieldError(self, missing_field_names="action_id")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "action_id": self.action_id,
        }
        if self.initial_value:
            data["initial_value"] = json.loads(self.initial_value.build_to_json())
        if self.dispatch_action_config:
            data["dispatch_action_config"] = json.loads(self.dispatch_action_config.build_to_json())
        if self.is_focus_on_load:
            data["focus_on_load"] = self.is_focus_on_load
        if self.placeholder:
            data["placeholder"] = json.loads(self.placeholder.build_to_json())

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextInput instance from its JSON representation
        :param json: a JSON representation of a RichTextInput element, e.g. from the 'elements' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.action_id = json["action_id"]
        if "initial_value" in json.keys() and json["initial_value"] is not None:
            self.initial_value = RichText().build_from_json(json["initial_value"])
        if "focus_on_load" in json.keys() and json["focus_on_load"] is not None:
            self.is_focus_on_load = json["focus_on_load"]
        if "placeholder" in json.keys() and json["placeholder"] is not None:
            self.placeholder = PlainText().build_from_json(json["placeholder"])
        if "dispatch_action_config" in json.keys() and json["dispatch_action_config"] is not None:
            self.dispatch_action_config = DispatchActionConfig().build_from_json(json["dispatch_action_config"])
        return self
