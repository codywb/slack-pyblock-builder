import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class ConfirmationDialog:
    """
    A Python class representing a Confirmation dialog object from the Slack BlockKit UI framework\n
    """

    def __init__(self):
        self._title = {}
        self._text = {}
        self._confirm_text = {}
        self._deny_text = {}
        self._style = None
        self.json = {
            "title": self._title,
            "text": self._text,
            "confirm": self._confirm_text,
            "deny": self._deny_text
        }

    def set_title(self, title_text: str) -> Self:
        """
        Sets the title text for the Confirmation dialog
        :param title_text: String; max 100 chars
        :return: self
        """
        self._title = Text().set_text(title_text)
        self.json["title"] = self._title.json
        return self

    def set_text(self, text: str) -> Self:
        """
        Sets the explanatory text that appears in the Confirmation dialog
        :param text: String; max 300 chars
        :return: self
        """
        self._text = Text().set_text(text)
        self.json["text"]= self._text.json
        return self

    def set_confirm_label(self, label_text: str) -> Self:
        """
        Sets the label for the button that confirms the action
        :param label_text: String; max 30 chars
        :return: self
        """
        self._confirm_text = Text().set_text(label_text)
        self.json["confirm"]= self._confirm_text.json
        return self

    def set_deny_label(self, label_text: str) -> Self:
        """
        Sets the label for the button that cancels the action
        :param label_text: String; max 30 chars
        :return: self
        """
        self._deny_text = Text().set_text(label_text)
        self.json["deny"] = self._deny_text.json
        return self

    def set_style(self, style: str) -> Self:
        """
        (Optional) Sets the style for the button to decorate with alternative visual color schemes. If unset, defaults
        to "primary".
        :param style: String; "primary" gives a green outline and text, "danger" gives a red outline and text
        :return: self
        """
        self._style = style
        self.json["style"] = self._style
        return self

    def primary(self) -> Self:
        """
        (Optional) Sets the style of the button to "primary", decorating it with a green background.
        :return: self
        """
        self._style = "primary"
        self.json["style"] = self._style
        return self

    def danger(self) -> Self:
        """
        (Optional) Sets the style of the button to "danger", decorating it with a red background.
        :return: self
        """
        self._style = "danger"
        self.json["style"] = self._style
        return self
