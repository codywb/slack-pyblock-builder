import sys
if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import TextLengthError, IncorrectTypeError, RequiredFieldsError
from pyblock_builder.objects.text import Text, PlainText, MrkdwnText


@dataclass
class Option:
    """
    Defines a single item in a number of item selection elements.
    """
    text: PlainText | MrkdwnText | None = None
    value: str | None = None
    description: PlainText | MrkdwnText | None = None
    url: str | None = None

    def set_text(self, text: PlainText | MrkdwnText) -> Self:
        """
        Sets the text shown in the option on the menu
        :param text: String, max 75 chars
        :return: self
         """
        if not isinstance(text, (PlainText, MrkdwnText)):
            raise IncorrectTypeError(self, method="set_text", compatible_types=[PlainText, MrkdwnText], incompatible_type=text)
        if not 1 <= len(text.text) <= 75:
            raise TextLengthError(self, field="text", min_length=1, max_length=75)
        self.text = text
        return self

    def set_value(self, value: str) -> Self:
        """
        Sets the value to be passed to your app when the option is chosen
        :param value: String; max 75 chars
        :return: self
        """
        if not 1 <= len(value) <= 150:
            raise TextLengthError(self, field="value", min_length=1, max_length=150)
        self.value = value
        return self

    def set_url(self, target_url: str) -> Self:
        """
        (Optional) Sets the url to be opened when a user clicks the option. Only available in overflow menus!
        :param target_url: String; max 3,000 chars, still requires an ack() response to the Slack API
        :return: self
        """
        if not 1 <= len(target_url) <= 3000:
            raise TextLengthError(self, field="url", min_length=1, max_length=3000)
        self.url = target_url
        return self

    def set_description(self, descriptive_text: PlainText | MrkdwnText) -> Self:
        """
        (Optional) Sets the text to be shown below the Option's text beside a radio button
        :param descriptive_text: PlainText or MrkdwnText object; max 75 chars
        :return: self
        """
        if not isinstance(descriptive_text, (PlainText, MrkdwnText)):
            raise IncorrectTypeError(self, method="set_description", compatible_types=[PlainText, MrkdwnText], incompatible_type=descriptive_text)
        if not 1 <= len(descriptive_text.text) <= 75:
            raise TextLengthError(self, field="description", min_length=1, max_length=75)
        self.description = descriptive_text
        return self

    def build_to_json(self) -> str:
        # raise error if required fields are not set
        if any([field is None for field in [self.text, self.value]]):
            raise RequiredFieldsError(self, missing_field_names=["text", "value"])
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "text": json.loads(self.text.build_to_json()),
            "value": self.value
        }
        if self.description:
            data["description"] = json.loads(self.description.build_to_json())
        if self.url:
            data["url"] = self.url

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a Option instance from its JSON representation
        :param json: a JSON representation of a Option object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if json["text"]["type"] == "plain_text":
            self.text = PlainText().build_from_json(json["text"])
        else:
            self.text = MrkdwnText().build_from_json(json["text"])
        self.value = json["value"]
        if "url" in json.keys() and json["url"] is not None:
            self.url = json["url"]
        if "description" in json.keys() and json["url"] is not None:
            if json["description"]["type"] == "plain_text":
                self.description = PlainText().build_from_json(json["description"])
            else:
                self.description = MrkdwnText().build_from_json(json["description"])
        return self