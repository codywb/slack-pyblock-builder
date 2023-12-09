import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Fields:
    """
    A Python class representing a Fields object from the Slack BlockKit UI framework\n
    Can be added to: Section
    """
    def __init__(self):
        self.fields = []

    def add_field(self, text: str, mrkdwn=True) -> Self:
        """
        Sets the text for the field
        :param text: String; max 3,000 chars
        :param mrkdwn: Boolean; defaults to True
        :return: self
        """
        if not mrkdwn:
            text = Text().set_text(text)
        else:
            text = Text().set_text(text).as_mrkdwn()
        self.fields.append(text.json)
        return self

