import sys
if sys.version_info >= (3, 11):
    from typing import Self, Sequence, Any
else:
    from typing_extensions import Self, Sequence, Any
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import TextLengthError, RequiredFieldsError, IncorrectTypeError, ItemLengthError
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText
from pyblock_builder.objects.option import Option

@dataclass
class OptionGroup:
    """
    Defines a way to group options in a select menu or a multi-select menu.
    """
    label: PlainText | None = None
    options: list[Option] = field(default_factory=list)

    def set_label(self, label_text: PlainText) -> Self:
        """
        Sets the label to be displayed above the group of Options
        :param label_text: PlainText object; max 75 chars
        :return: self
        """
        if not isinstance(label_text, PlainText):
            raise IncorrectTypeError(self, method="set_label", compatible_types=PlainText, incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 75:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=75)
        self.label = label_text
        return self

    def set_options(self, *options: Option | Sequence[Option]) -> Self:
        """
       Sets the options belonging to this specific group
       :param options: One or more Option objects, or a list/tuple of Option objects; maximum of 100 items
       :return: self
       """
        flattened_options = []
        for opt in options:
            if isinstance(opt, (list, tuple)):
                flattened_options.extend(opt)
            else:
                flattened_options.append(opt)

        if not 1 <= len(flattened_options) <= 100:
            raise ItemLengthError(self, field="options", min_length=1, max_length=100)

        for option in flattened_options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_options", compatible_types=Option, incompatible_type=option)
            self.options.append(option)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.label, self.options]]):
            raise RequiredFieldsError(self, missing_field_names=["label", "options"])
        # # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "label": json.loads(self.label.build_to_json()),
            "options": [json.loads(option.build_to_json()) for option in self.options]
        }

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a class OptionGroup instance from its JSON representation
        :param json: a JSON representation of a OptionGroup object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.label = PlainText().build_from_json(json["label"])
        self.options = [Option().build_from_json(option) for option in json["options"]]
        return self
