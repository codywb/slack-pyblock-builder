import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, asdict, field
import json
from datetime import datetime
from pyblock_builder._internal.errors import IncorrectValueError, RequiredFieldError, IncorrectTypeError, RequiredFieldsError
from pyblock_builder.base_blocks import RichTextElement

@dataclass
class RichTextBroadcast:
    """
    Defines a rich text element broadcast object
    """
    type: Literal["broadcast"] = "broadcast"
    range: Literal["here", "channel", "everyone"] | None = None

    def set_range(self, range: Literal["here", "channel", "everyone"]) -> Self:
        """
        (Optional) Sets the range of the broadcast.
        :param range: String; "here" notifies active members of a channel, "channel" notifies all members of a channel, "everyone" notifies everyone in #general
        :return: self
        """
        if range not in ("here", "channel", "everyone"):
            raise IncorrectValueError(self, method="set_range", acceptable_values=["here", "channel", "everyone"], unacceptable_value=range)
        self.range = range
        return self

    def build_to_json(self):
        # raise error if required fields are not set
        if not self.range:
            raise RequiredFieldError(self, missing_field_names="range")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        return json.dumps({k.replace("_", ""): v for k, v in asdict(self).items() if v is not None})

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextBroadcast instance from its JSON representation
        :param json: a JSON representation of a RichTextBroadcast object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.range = json["range"]
        return self

@dataclass
class RichTextColor:
    """
    Defines a rich text element color object
    """
    type: Literal["color"] = "color"
    value: str | None = None

    def set_hex_value(self, hex_value: str) -> Self:
        """
        (Optional) Sets the hex value for the color.
        :param hex_value: String (e.g. "#F405B3")
        :return: self
        """
        if not isinstance(hex_value, str):
            raise IncorrectTypeError(self, method="set_hex_value", compatible_types=str,
                                      incompatible_type=hex_value)
        self.value = hex_value
        return self

    def build_to_json(self):
        # raise error if required fields are not set
        if not self.value:
            raise RequiredFieldError(self, missing_field_names="value")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        return json.dumps({k.replace("_", ""): v for k, v in asdict(self).items() if v is not None})

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextColor instance from its JSON representation
        :param json: a JSON representation of a RichTextColor object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.value = json["value"]
        return self

@dataclass
class RichTextChannel:
    """
    Defines a rich text element channel object. Set individually with bold(), italic(), etc. or using set_style()
    """
    type: Literal["channel"] = "channel"
    channel_id: str | None = None
    style: dict[Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"], bool] | None = None

    def set_channel_id(self, channel_id: str) -> Self:
        """
        (Optional) Sets the id of the channel to be mentioned
        :param channel_id: String
        :return: self
        """
        if not isinstance(channel_id, str):
            raise IncorrectTypeError(self, method="set_channel_id", compatible_types=str,
                                      incompatible_type=channel_id)
        self.channel_id = channel_id
        return self

    def set_style(self, styles: Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"] |
                                list[Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"]]) -> Self:
        """
        Apply one or more rich text styling
        :param styles: string or list of strings comprising "bold", "italic", "strike", "highlight", "client_highlight", "unlink"
        :return: self
        """
        possible_styles = ["bold", "italic", "strike", "highlight", "client_highlight", "unlink"]
        if not isinstance(styles, str) and not isinstance(styles, list):
            raise IncorrectTypeError(self, method="set_style", compatible_types=[str, list[str]], incompatible_type=styles)
        if isinstance(styles, str):
            if styles not in possible_styles:
                raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles, unacceptable_value=styles)
            if not self.style:
                self.style = {}
            self.style[styles] = True
        if isinstance(styles, list):
            for style in styles:
                if style not in possible_styles:
                    raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                              unacceptable_value=style)
                if not self.style:
                    self.style = {}
                self.style[style] = True
        return self

    def bold(self):
        """
        (Optional) Applies bold styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["bold"] = True
        return self

    def italic(self):
        """
        (Optional) Applies italic styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["italic"] = True
        return self

    def strike(self):
        """
        (Optional) Applies strikethrough styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["strike"] = True
        return self

    def highlight(self):
        """
        (Optional) Applies highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["highlight"] = True
        return self

    def client_highlight(self):
        """
        (Optional) Applies client highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["client_highlight"] = True
        return self

    def unlink(self):
        """
        (Optional) Applies unlink styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["unlink"] = True
        return self

    def build_to_json(self):
        # raise error if required fields are not set
        if not self.channel_id:
            raise RequiredFieldError(self, missing_field_names="channel_id")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "channel_id": self.channel_id,
        }
        if self.style:
            data["style"] = self.style

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextChannel instance from its JSON representation
        :param json: a JSON representation of a RichTextChannel object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.channel_id = json["channel_id"]
        if "style" in json.keys() and json["style"] is not None:
            self.style = json["style"]
        return self

@dataclass
class RichTextDate:
    """
    Defines a rich text element date object
    """
    type: Literal["date"] = "date"
    timestamp: int | datetime | None = None
    format: str | None = None
    url: str | None = None
    fallback: str | None = None

    def set_date(self, timestamp: int | datetime) -> Self:
        """
        Sets the date to be displayed
        :param timestamp: UNIX timestamp in seconds (should be 10 digits) or Python datetime object
        :return: self
        """
        if not isinstance(timestamp, int) and not isinstance(timestamp, datetime):
            raise IncorrectTypeError(self, method="set_date", compatible_types=[int, datetime], incompatible_type=timestamp)
        if isinstance(timestamp, datetime):
            self.timestamp = int(timestamp.timestamp())
        else:
            self.timestamp = timestamp
        return self

    def set_format(self, format: str) -> Self:
        """
        Sets a template string containing curly-brace-enclosed tokens to substitute the provided timestamp.
        :param format: string containing one or more available tokens, e,g, "{date_num} at {time}"
        :return: self
        """
        allowed_tokens = [
            "{day_divider_pretty}", "{date_num}", "{date_slash}", "{date_long}", "{date_long_full}", "{date_long_pretty}",
            "{date}", "{date_pretty}", "{date_short}", "{date_short_pretty}", "{time}", "{time_secs}", "{ago}"
        ]
        if not isinstance(format, str):
            raise IncorrectTypeError(self, method="set_format", compatible_types=str, incompatible_type=format)
        for s in format.split():
            if s.startswith("{") and s.endswith("}"):
                if s not in allowed_tokens:
                    raise IncorrectValueError(self, method="set_format", acceptable_values=allowed_tokens, unacceptable_value=s)
        if not any([token in format.split() for token in allowed_tokens]):
            raise ValueError(f"Template string passed to 'set_format' method of {self.__class__.__name__} must include "
                             f"at least one allowed curly-brace-enclosed token.")
        self.format = format
        return self

    def set_url(self, url: str) -> Self:
        """
        (Optional) Sets the URL to link the entire format string to.
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_url", compatible_types=str,
                                      incompatible_type=url)
        self.url = url
        return self

    def set_fallback_text(self, fallback_text: str) -> Self:
        """
        (Optional) Sets the fext to display in place of the date should parsing, formatting or displaying fail.
        :param fallback_text: string
        :return: self
        """
        if not isinstance(fallback_text, str):
            raise IncorrectTypeError(self, method="set_fallback_text", compatible_types=str,
                                      incompatible_type=fallback_text)
        self.fallback = fallback_text
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.format, self.timestamp]]):
            raise RequiredFieldsError(self, missing_field_names=["format", "timestamp"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "timestamp": self.timestamp,
            "format": self.format,
        }
        if self.url:
            data["url"] = self.url
        if self.fallback:
            data["fallback"] = self.fallback

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextDate instance from its JSON representation
        :param json: a JSON representation of a RichTextDate object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.timestamp = json["timestamp"]
        self.format = json["format"]
        if "url" in json.keys() and json["url"] is not None:
            self.url = json["url"]
        if "fallback" in json.keys() and json["fallback"] is not None:
            self.fallback = json["fallback"]
        return self

@dataclass
class RichTextEmoji:
    """
    Defines a rich text element emoji object
    """
    type: Literal["emoji"] = "emoji"
    name: str | None = None
    unicode: str | None = None

    def set_name(self, name: str) -> Self:
        """
        Specifies the name of the emoji to be displayed.
        :param name: string, e.g. "wave", "wave::skin-tone-2"
        :return: self
        """
        if not isinstance(name, str):
            raise IncorrectTypeError(self, method="set_name", compatible_types=str,
                                      incompatible_type=name)
        self.name = name
        return self

    def set_unicode(self, unicode: str) -> Self:
        """
        Specifies the unicode code pointing to the emoji to be displayed.
        :param unicode: string, e.g. "U+1F600"
        :return: self
        """
        if not isinstance(unicode, str):
            raise IncorrectTypeError(self, method="set_unicode", compatible_types=str,
                                     incompatible_type=unicode)
        self.unicode = unicode
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.name:
            raise RequiredFieldError(self, missing_field_names="name")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "name": self.name,
        }
        if self.unicode:
            data["unicode"] = self.unicode

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextEmoji instance from its JSON representation
        :param json: a JSON representation of a RichTextEmoji object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.name = json["name"]
        if "unicode" in json.keys() and json["unicode"] is not None:
            self.unicode = json["unicode"]
        return self

@dataclass
class RichTextLink:
    """
    Defines a rich text element link object
    """
    type: Literal["link"] = "link"
    url: str | None = None
    text: str | None = None
    is_unsafe: bool | None = None
    style: dict[Literal["bold", "italic", "strike", "code"], bool] | None = None

    def set_url(self, url: str) -> Self:
        """
        (Optional) Sets the target URL for the link
        :param url: string
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_url", compatible_types=str,
                                     incompatible_type=url)
        self.url = url
        return self

    def set_text(self, text: str) -> Self:
        """
        Sets the text shown to the user (instead of the url). If no text is provided, the url is used.
        :param text: string
        :return: self
        """
        if not isinstance(text, str):
            raise IncorrectTypeError(self, method="set_text", compatible_types=str,
                                     incompatible_type=text)
        self.text = text
        return self

    def unsafe(self):
        """
        (Optional) Indicates the link is unsafe
        :return: self
        """
        self.is_unsafe = True
        return self

    def set_style(self, styles: Literal["bold", "italic", "strike", "code"] |
                                list[Literal["bold", "italic", "strike", "code"]]) -> Self:
        """
        Apply one or more rich text styling to the link
        :param styles: string or list of strings comprising "bold", "italic", "strike", "code"
        :return: self
        """
        possible_styles = ["bold", "italic", "strike", "code"]
        if not isinstance(styles, str) and not isinstance(styles, list):
            raise IncorrectTypeError(self, method="set_style", compatible_types=[str, list[str]], incompatible_type=styles)
        if isinstance(styles, str):
            if styles not in possible_styles:
                raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles, unacceptable_value=styles)
            if not self.style:
                self.style = {}
            self.style[styles] = True
        if isinstance(styles, list):
            for style in styles:
                if style not in possible_styles:
                    raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                              unacceptable_value=style)
                if not self.style:
                    self.style = {}
                self.style[style] = True
        return self

    def bold(self):
        """
        (Optional) Applies bold styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["bold"] = True
        return self

    def italic(self):
        """
        (Optional) Applies italic styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["italic"] = True
        return self

    def strike(self):
        """
        (Optional) Applies strikethrough styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["strike"] = True
        return self

    def code(self):
        """
        (Optional) Applies code styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["code"] = True
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.url:
            raise RequiredFieldError(self, missing_field_names="url")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "url": self.url,
        }
        if self.text:
            data["text"] = self.text
        if self.is_unsafe:
            data["unsafe"] = self.is_unsafe
        if self.style:
            data["style"] = self.style

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextLink instance from its JSON representation
        :param json: a JSON representation of a RichTextLink object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.url = json["url"]
        if "text" in json.keys() and json["text"] is not None:
            self.text = json["text"]
        if "unsafe" in json.keys() and json["unsafe"] is not None:
            self.unsafe = json["unsafe"]
        if "style" in json.keys() and json["style"] is not None:
            self.style = json["style"]
        return self

@dataclass
class RichTextText:
    """
    Defines a rich text element text object
    """
    type: Literal["text"] = "text"
    text: str | None = None
    style: dict[Literal["bold", "italic", "strike", "code"], bool] | None = None

    def set_text(self, text: str) -> Self:
        """
        Sets the text shown to the user
        :param text: string
        :return: self
        """
        if not isinstance(text, str):
            raise IncorrectTypeError(self, method="set_text", compatible_types=str,
                                     incompatible_type=text)
        self.text = text
        return self

    def set_style(self, styles: Literal["bold", "italic", "strike", "code"] |
                                list[Literal["bold", "italic", "strike", "code"]]) -> Self:
        """
        Apply one or more rich text styling to the text
        :param styles: string or list of strings comprising "bold", "italic", "strike", "code"
        :return: self
        """
        possible_styles = ["bold", "italic", "strike", "code"]
        if not isinstance(styles, str) and not isinstance(styles, list):
            raise IncorrectTypeError(self, method="set_style", compatible_types=[str, list[str]], incompatible_type=styles)
        if isinstance(styles, str):
            if styles not in possible_styles:
                raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles, unacceptable_value=styles)
            if not self.style:
                self.style = {}
            self.style[styles] = True
        if isinstance(styles, list):
            for style in styles:
                if style not in possible_styles:
                    raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                              unacceptable_value=style)
                if not self.style:
                    self.style = {}
                self.style[style] = True
        return self

    def bold(self):
        """
        (Optional) Applies bold styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["bold"] = True
        return self

    def italic(self):
        """
        (Optional) Applies italic styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["italic"] = True
        return self

    def strike(self):
        """
        (Optional) Applies strikethrough styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["strike"] = True
        return self

    def code(self):
        """
        (Optional) Applies code styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["code"] = True
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.text:
            raise RequiredFieldError(self, missing_field_names="text")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "text": self.text,
        }
        if self.style:
            data["style"] = self.style

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextText instance from its JSON representation
        :param json: a JSON representation of a RichTextText object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.text = json["text"]
        if "style" in json.keys() and json["style"] is not None:
            self.style = json["style"]
        return self

@dataclass
class RichTextUser:
    """
    Defines a rich text element user object
    """
    type: Literal["user"] = "user"
    user_id: str | None = None
    style: dict[Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"], bool] | None = None

    def set_user_id(self, user_id: str) -> Self:
        """
        Specifies the id of the user to be mentioned
        :param user_id: string
        :return: self
        """
        if not isinstance(user_id, str):
            raise IncorrectTypeError(self, method="set_user_id", compatible_types=str,
                                     incompatible_type=user_id)
        self.user_id = user_id
        return self

    def set_style(self, styles: Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"] |
                                list[Literal[
                                    "bold", "italic", "strike", "highlight", "client_highlight", "unlink"]]) -> Self:
        """
        Apply one or more rich text styling
        :param styles: string or list of strings comprising "bold", "italic", "strike", "highlight", "client_highlight", "unlink"
        :return: self
        """
        possible_styles = ["bold", "italic", "strike", "highlight", "client_highlight", "unlink"]
        if not isinstance(styles, str) and not isinstance(styles, list):
            raise IncorrectTypeError(self, method="set_style", compatible_types=[str, list[str]],
                                     incompatible_type=styles)
        if isinstance(styles, str):
            if styles not in possible_styles:
                raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                          unacceptable_value=styles)
            if not self.style:
                self.style = {}
            self.style[styles] = True
        if isinstance(styles, list):
            for style in styles:
                if style not in possible_styles:
                    raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                              unacceptable_value=style)
                if not self.style:
                    self.style = {}
                self.style[style] = True
        return self

    def bold(self):
        """
        (Optional) Applies bold styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["bold"] = True
        return self

    def italic(self):
        """
        (Optional) Applies italic styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["italic"] = True
        return self

    def strike(self):
        """
        (Optional) Applies strikethrough styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["strike"] = True
        return self

    def highlight(self):
        """
        (Optional) Applies highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["highlight"] = True
        return self

    def client_highlight(self):
        """
        (Optional) Applies client highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["client_highlight"] = True
        return self

    def unlink(self):
        """
        (Optional) Applies unlink styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["unlink"] = True
        return self

    def build_to_json(self):
        # raise error if required fields are not set
        if not self.user_id:
            raise RequiredFieldError(self, missing_field_names="user_id")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "user_id": self.user_id,
        }
        if self.style:
            data["style"] = self.style

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextUser instance from its JSON representation
        :param json: a JSON representation of a RichTextUser object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.user_id = json["user_id"]
        if "style" in json.keys() and json["style"] is not None:
            self.style = json["style"]
        return self

@dataclass
class RichTextUserGroup:
    """
    Defines a rich text element usergroup object
    """
    type: Literal["usergroup"] = "usergroup"
    usergroup_id: str | None = None
    style: dict[Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"], bool] | None = None

    def set_usergroup_id(self, usergroup_id: str) -> Self:
        """
        Specifies the id of the user to be mentioned
        :param user_id: string
        :return: self
        """
        if not isinstance(usergroup_id, str):
            raise IncorrectTypeError(self, method="set_usergroup_id", compatible_types=str,
                                     incompatible_type=usergroup_id)
        self.usergroup_id = usergroup_id
        return self

    def set_style(self, styles: Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"] |
                                list[Literal["bold", "italic", "strike", "highlight", "client_highlight", "unlink"]]) -> Self:
        """
        Apply one or more rich text styling
        :param styles: string or list of strings comprising "bold", "italic", "strike", "highlight", "client_highlight", "unlink"
        :return: self
        """
        possible_styles = ["bold", "italic", "strike", "highlight", "client_highlight", "unlink"]
        if not isinstance(styles, str) and not isinstance(styles, list):
            raise IncorrectTypeError(self, method="set_style", compatible_types=[str, list[str]],
                                     incompatible_type=styles)
        if isinstance(styles, str):
            if styles not in possible_styles:
                raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                          unacceptable_value=styles)
            if not self.style:
                self.style = {}
            self.style[styles] = True
        if isinstance(styles, list):
            for style in styles:
                if style not in possible_styles:
                    raise IncorrectValueError(self, method="set_style", acceptable_values=possible_styles,
                                              unacceptable_value=style)
                if not self.style:
                    self.style = {}
                self.style[style] = True
        return self

    def bold(self):
        """
        (Optional) Applies bold styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["bold"] = True
        return self

    def italic(self):
        """
        (Optional) Applies italic styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["italic"] = True
        return self

    def strike(self):
        """
        (Optional) Applies strikethrough styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["strike"] = True
        return self

    def highlight(self):
        """
        (Optional) Applies highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["highlight"] = True
        return self

    def client_highlight(self):
        """
        (Optional) Applies client highlight styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["client_highlight"] = True
        return self

    def unlink(self):
        """
        (Optional) Applies unlink styling
        :return: self
        """
        if not self.style:
            self.style = {}
        self.style["unlink"] = True
        return self

    def build_to_json(self):
        # raise error if required fields are not set
        if not self.usergroup_id:
            raise RequiredFieldError(self, missing_field_names="usergroup_id")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "usergroup_id": self.usergroup_id,
        }
        if self.style:
            data["style"] = self.style

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextUserGroup instance from its JSON representation
        :param json: a JSON representation of a RichTextUserGroup object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.usergroup_id = json["usergroup_id"]
        if "style" in json.keys() and json["style"] is not None:
            self.style = json["style"]
        return self

@dataclass
class RichTextSection:
    """
    Defines a rich text object section sub-element containing some rich text.
    """
    type: Literal["rich_text_section"] = "rich_text_section"
    elements: list[RichTextElement] = field(default_factory=list)

    def add_elements(self, *elements: RichTextElement | Sequence[RichTextElement]) -> Self:
        """
        Used to add one or more rich text elements to a rich text object sub-element
        :param elements: One or more rich text elements (broadcast, channel, color, emoji, etc.)
        :return: self
        """
        compatible_elements = [RichTextBroadcast, RichTextColor, RichTextChannel, RichTextDate, RichTextEmoji,
                               RichTextText, RichTextLink, RichTextUser, RichTextUserGroup]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        for element in flattened_elements:
            if type(element) not in compatible_elements:
                raise IncorrectTypeError(self, method="add_elements", compatible_types=compatible_elements, incompatible_type=element)
            self.elements.append(element)
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.elements:
            raise RequiredFieldError(self, missing_field_names="elements")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "elements": [json.loads(element.build_to_json()) for element in self.elements if element],
        }

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextSection instance from its JSON representation
        :param json: a JSON representation of a RichTextSection object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        compatible_types = {
            "broadcast": RichTextBroadcast,
            "color": RichTextColor,
            "channel": RichTextChannel,
            "dats": RichTextDate,
            "emoji": RichTextEmoji,
            "text": RichTextText,
            "link": RichTextLink,
            "user": RichTextUser,
            "usergroup": RichTextUserGroup
        }
        self.elements = [compatible_types[element["type"]]().build_from_json(element) for element in json["elements"]]
        return self

@dataclass
class RichTextList:
    """
    Defines a rich text object list sub-element containing some rich text.
    """
    type: Literal["rich_text_list"] = "rich_text_list"
    style: Literal["bullet", "ordered"] | None = None
    elements: list[RichTextSection] = field(default_factory=list)
    indent: int | None = None
    offset: int | None = None
    border: int | None = None

    def set_style(self, style: Literal["bullet", "ordered"]) -> Self:
        """
        Specifies the styling of the list
        :param style: string; either "bullet" or "ordered"
        :return: self
        """
        if not isinstance(style, str):
            raise IncorrectTypeError(self, method="set_style", compatible_types=str,
                                     incompatible_type=style)
        if style not in ("bullet", "ordered"):
            raise IncorrectValueError(self, method="set_style", acceptable_values=["bullet", "ordered"],
                                      unacceptable_value=style)
        self.style = style
        return self

    def add_elements(self, *elements: RichTextSection | Sequence[RichTextSection]) -> Self:
        """
        Used to add one or more rich text sections to the list
        :param elements: A rich text section or list of rich text section objects
        :return: self
        """
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        for element in flattened_elements:
            if not isinstance(element, RichTextSection):
                raise IncorrectTypeError(self, method="add_elements", compatible_types=RichTextSection, incompatible_type=element)
            self.elements.append(element)
        return self

    def set_indent(self, indent: int) -> Self:
        """
        Specifies the number of pixels to indent the list
        :param indent: int
        :return: self
        """
        if not isinstance(indent, int):
            raise IncorrectTypeError(self, method="set_indent", compatible_types=int, incompatible_type=indent)
        self.indent = indent
        return self

    def set_offset(self, offset: int) -> Self:
        """
        Specifies the humber to offset the first number in the list.
        For example, if the offset = 4, the first number in the ordered list would be 5.
        :param offset: int
        :return: self
        """
        if not isinstance(offset, int):
            raise IncorrectTypeError(self, method="set_offset", compatible_types=int, incompatible_type=offset)
        self.offset = offset
        return self

    def set_border(self, border: int) -> Self:
        """
        Specifies the number of pixels of border thickness
        :param border: int
        :return: self
        """
        if not isinstance(border, int):
            raise IncorrectTypeError(self, method="set_border", compatible_types=int, incompatible_type=border)
        self.border = border
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.elements, self.style]]):
            raise RequiredFieldsError(self, missing_field_names=["elements", "style"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "style": self.style,
            "elements": [json.loads(element.build_to_json()) for element in self.elements if element],
        }
        if self.indent:
            data["indent"] = self.indent
        if self.offset:
            data["offset"] = self.offset
        if self.border:
            data["border"] = self.border

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextList instance from its JSON representation
        :param json: a JSON representation of a RichTextList object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        self.style = json["style"]
        self.elements = [RichTextSection().build_from_json(element) for element in json["elements"]]
        if "indent" in json.keys() and json["indent"] is not None:
            self.indent = json["indent"]
        if "offset" in json.keys() and json["offset"] is not None:
            self.offset = json["offset"]
        if "border" in json.keys() and json["border"] is not None:
            self.border = json["border"]
        return self

@dataclass
class RichTextPreformatted:
    """
    Defines a rich text object preformatted code block sub-element containing some rich text.
    """
    type: Literal["rich_text_preformatted"] = "rich_text_preformatted"
    elements: list[RichTextElement] = field(default_factory=list)
    border: int | None = None

    def add_elements(self, *elements: RichTextElement | Sequence[RichTextElement]) -> Self:
        """
        Used to add one or more rich text elements to a rich text object sub-element
        :param elements: One or more rich text elements (broadcast, channel, color, emoji, etc.)
        :return: self
        """
        compatible_elements = [RichTextBroadcast, RichTextColor, RichTextChannel, RichTextDate, RichTextEmoji,
                               RichTextText, RichTextLink, RichTextUser, RichTextUserGroup]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        for element in flattened_elements:
            if type(element) not in compatible_elements:
                raise IncorrectTypeError(self, method="add_elements", compatible_types=compatible_elements,
                                         incompatible_type=element)
            self.elements.append(element)
        return self

    def set_border(self, border: int) -> Self:
        """
        Specifies the number of pixels of border thickness
        :param border: int
        :return: self
        """
        if not isinstance(border, int):
            raise IncorrectTypeError(self, method="set_border", compatible_types=int, incompatible_type=border)
        self.border = border
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.elements:
            raise RequiredFieldError(self, missing_field_names="elements")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "elements": [json.loads(element.build_to_json()) for element in self.elements if element],
        }
        if self.border:
            data["border"] = self.border

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextPreformatted instance from its JSON representation
        :param json: a JSON representation of a RichTextPreformatted object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        compatible_types = {
            "broadcast": RichTextBroadcast,
            "color": RichTextColor,
            "channel": RichTextChannel,
            "dats": RichTextDate,
            "emoji": RichTextEmoji,
            "text": RichTextText,
            "link": RichTextLink,
            "user": RichTextUser,
            "usergroup": RichTextUserGroup
        }
        self.elements = [compatible_types[element["type"]]().build_from_json(element) for element in json["elements"]]
        if "border" in json.keys() and json["border"] is not None:
            self.border = json["border"]
        return self

@dataclass
class RichTextQuote:
    """
    Defines a rich text object quote sub-element containing some rich text.
    """
    type: Literal["rich_text_quote"] = "rich_text_quote"
    elements: list[RichTextElement] = field(default_factory=list)
    border: int | None = None

    def add_elements(self, *elements: RichTextElement | Sequence[RichTextElement]) -> Self:
        """
        Used to add one or more rich text elements to a rich text object sub-element
        :param elements: One or more rich text elements (broadcast, channel, color, emoji, etc.)
        :return: self
        """
        compatible_elements = [RichTextBroadcast, RichTextColor, RichTextChannel, RichTextDate, RichTextEmoji,
                               RichTextText, RichTextLink, RichTextUser, RichTextUserGroup]
        flattened_elements = []
        for element in elements:
            if isinstance(element, (list, tuple)):
                flattened_elements.extend(element)
            else:
                flattened_elements.append(element)

        for element in flattened_elements:
            if type(element) not in compatible_elements:
                raise IncorrectTypeError(self, method="add_elements", compatible_types=compatible_elements,
                                         incompatible_type=element)
            self.elements.append(element)
        return self

    def set_border(self, border: int) -> Self:
        """
        Specifies the number of pixels of border thickness
        :param border: int
        :return: self
        """
        if not isinstance(border, int):
            raise IncorrectTypeError(self, method="set_border", compatible_types=int, incompatible_type=border)
        self.border = border
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if not self.elements:
            raise RequiredFieldError(self, missing_field_names="elements")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "elements": [json.loads(element.build_to_json()) for element in self.elements if element],
        }
        if self.border:
            data["border"] = self.border

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a RichTextQuote instance from its JSON representation
        :param json: a JSON representation of a RichTextQuote object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        compatible_types = {
            "broadcast": RichTextBroadcast,
            "color": RichTextColor,
            "channel": RichTextChannel,
            "dats": RichTextDate,
            "emoji": RichTextEmoji,
            "text": RichTextText,
            "link": RichTextLink,
            "user": RichTextUser,
            "usergroup": RichTextUserGroup
        }
        self.elements = [compatible_types[element["type"]]().build_from_json(element) for element in json["elements"]]
        if "border" in json.keys() and json["border"] is not None:
            self.border = json["border"]
        return self
