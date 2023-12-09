import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Text:
    """
    A Python class representing a Text object from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._type = "plain_text"
        self._text = ""
        self._emoji = True
        self._verbatim = False
        self.json = {
            "type": self._type,
            "text": self._text
        }

    def as_mrkdwn(self) -> Self:
        """
        (Optional) Sets the formatting of the object to "mrkdwn". The object will be of type plain_text if unused.
        :return: self
        """
        self._type = "mrkdwn"
        self.json['type'] = self._type
        return self

    def set_text(self, text: str) -> Self:
        """
        (Required) Sets the text for the object. May include Slack standard text formatting markup when using as_mrkdwn().
        :param text: String; must be between 1 and 3,000 characters.
        :return: self
        """
        self._text = text
        self.json['text'] = self._text
        return self

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
