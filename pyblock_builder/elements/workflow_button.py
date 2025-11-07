import sys
from multiprocessing.pool import worker

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any
else:
    from typing_extensions import Self, Literal, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import (TextLengthError, IncorrectTypeError, IncorrectValueError, RequiredFieldsError)
from pyblock_builder.objects import PlainText, Workflow

@dataclass
class WorkflowButton:
    """
    Allows users to run a link trigger with customizable inputs
    Can be added to: Section, Action
    Works on: Message
    """
    type: Literal["workflow_button"] = "workflow_button"
    text: PlainText | None = None
    workflow: Workflow | None = None
    action_id: str | None = None
    style: Literal["danger", "primary"] | None = None
    accessibility_label: str | None = None

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

    def set_text(self, label_text: PlainText) -> Self:
        """
        Sets the text to be displayed on the button
        :param label_text: PlainText; max 75 chars, may truncate after 30 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_text", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 75:
            raise TextLengthError(self, field="text", min_length=1, max_length=75)
        self.text = label_text
        return self

    def set_style(self, style: Literal["danger", "primary"]) -> Self:
        """
        (Optional) Sets the style for the button to decorate with alternative visual color schemes.
        :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
        :return: self
        """
        if style not in ("danger", "primary"):
            raise IncorrectValueError(self, method="set_style", acceptable_values=["danger", "primary"],
                                      unacceptable_value=style)
        self.style = style
        return self

    def set_accessibility_label(self, label_text: str) -> Self:
        """
        (Optional) Sets a label for longer descriptive text about a button that is read aloud by a screen reader
        instead of the text used in the button label
        :param label_text: String; max 75 chars
        :return: self
        """
        if not isinstance(label_text, str):
            raise IncorrectTypeError(self, method="set_accessibility_label", compatible_types=str, incompatible_type=label_text)
        if not 1 <= len(label_text) <= 75:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=75)
        self.accessibility_label = label_text
        return  self

    def add_workflow(self, workflow: Workflow) -> Self:
        pass

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.text, self.workflow, self.action_id]]):
            raise RequiredFieldsError(self, missing_field_names=["text", "workflow", "action_id"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "text": json.loads(self.text.build_to_json()),
            "workflow": json.loads(self.workflow.build_to_json()),
            "action_id": self.action_id,
        }
        if self.style:
            data["style"] = self.style
        if self.accessibility_label:
            data["accessibility_label"] = self.accessibility_label

        return json.dumps(data)