import sys
if sys.version_info >= (3, 11): # make package ^3.7
    from typing import Self
else:
    from typing_extensions import Self

class Text:
    """
    A Python class representing a Text object from the Slack BlockKit UI framework
    """
    def __init__(self, text_type, text):
        self._type = text_type
        self._text = text
        self._emoji = True
        self._verbatim = False
        self.json = {
            "type": self._type,
            "text": self._text
        }
        if self._type == "plain_text":
            self.json["emoji"] = self._emoji

    def escape_emojis(self) -> Self:
        """
        (Optional) Indicates whether emojis in text should be escaped into the colon emoji format. Only usable when
        self.type is "plain_text".
        :return: self
        """
        self._emoji = False
        self.json["emoji"] = self._emoji
        return self

    def is_verbatim(self) -> Self:
        """
        (Optional) Indicates whether text should be preprocessed for links, conversation names, mentions,
        etc. Only usable when self.type is "mrkdwn".
        :return: self
        """
        self._verbatim = True
        self.json["verbatim"] = self._verbatim
        return self
