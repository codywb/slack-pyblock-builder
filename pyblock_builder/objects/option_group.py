import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class OptionGroup:
    """
    A Python class representing an Option Group object from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._label = {}
        self._options = []
        self.json = {
            "label": self._label,
            "options": self._options
        }

    def set_label(self, label_text: str) -> Self:
        """
        Sets the label to be displayed above the group of Options
        :param label_text: String; max 75 chars
        :return: self
        """
        self._label = Text().set_text(label_text)
        self.json["label"] = self._label.json
        return self

    def set_options(self, *options) -> Self:
        """
        Sets the options belonging to this specific group
        :param options: One or more Option objects; maximum of 100 items; preface with * if passing in a list
        :return: self
        """
        for option in options:
            self._options.append(option.json)
        self.json["options"] = self._options
        return self
