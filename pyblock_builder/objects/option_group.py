import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText
from pyblock_builder.objects.option import Option

@dataclass
class OptionGroup:
    label: Text | None = None
    options: list[Option] = field(default_factory=list)

    def set_label(self, label_text: Text) -> Self:
        if not isinstance(label_text, (PlainText, MrkdwnText)):
            raise IncorrectTypeError(self, method="set_label", compatible_types=[PlainText, MrkdwnText], incompatible_type=label_text)
        if not 1 <= len(label_text.text) <= 75:
            raise TextLengthError(self, field="label_text", min_length=1, max_length=75)
        self.label = label_text
        return self

    def set_options(self, *options: Option) -> Self:
        if not 1 <= len(options) <= 100:
            raise ItemLengthError(self, field="options", min_length=1, max_length=100)
        for option in options:
            if not isinstance(option, Option):
                raise IncorrectTypeError(self, method="set_options", compatible_types=Option, incompatible_type=option)
            self.options.append(option)
        return self

    def build_to_json(self) -> str:
        if self.label is None:
            raise RequiredFieldError(self, missing_field_names="label")
        if not self.options:
            raise RequiredFieldError(self, missing_field_names="options")
        # # return JSON representation of object using only non-empty fields and removing leading underscores
        data = {
            "label": json.loads(self.label.build_to_json()),
            "options": [json.loads(option.build_to_json()) for option in self.options]
        }

        return json.dumps(data)

# class OptionGroup:
#     """
#     A Python class representing an Option Group object from the Slack BlockKit UI framework
#     """
#     def __init__(self):
#         self._label = {}
#         self._options = []
#         self.json = {
#             "label": self._label,
#             "options": self._options
#         }
#
#     def set_label(self, label_text: str) -> Self:
#         """
#         Sets the label to be displayed above the group of Options
#         :param label_text: String; max 75 chars
#         :return: self
#         """
#         self._label = Text().set_text(label_text)
#         self.json["label"] = self._label.json
#         return self
#
#     def set_options(self, *options) -> Self:
#         """
#         Sets the options belonging to this specific group
#         :param options: One or more Option objects; maximum of 100 items; preface with * if passing in a list
#         :return: self
#         """
#         for option in options:
#             self._options.append(option.json)
#         self.json["options"] = self._options
#         return self
