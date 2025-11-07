import sys

if sys.version_info >= (3, 11):
    from typing import Self, Any
else:
    from typing_extensions import Self, Any
from dataclasses import dataclass
import json
from pyblock_builder._internal.errors import RequiredFieldError, IncorrectTypeError

@dataclass
class SlackFile:
    """
    Defines an object containing Slack file information to be used in an image block or image element.
    This file must be an image and you must provide either the URL or ID. In addition, the user posting these blocks
    must have access to this file. If both are provided then the payload will be rejected. Currently only png, jpg,
    jpeg, and gif Slack image files are supported.
    """
    url: str | None = None
    id: str | None = None

    def set_url(self, url: str) -> Self:
        """
        Sets the URL of the image to be displayed. This URL can be the url_private or the permalink of the Slack file.
        :param url: String
        :return: self
        """
        if not isinstance(url, str):
            raise IncorrectTypeError(self, method="set_url", compatible_types=str, incompatible_type=url)
        self.url = url
        return self

    def set_id(self, id: str) -> Self:
        """
       Sets the Slack ID of the file to be displayed.
       :param url: String
       :return: self
       """
        if not isinstance(id, str):
            raise IncorrectTypeError(self, method="set_id", compatible_types=str, incompatible_type=id)
        self.id = id
        return self

    def build_to_json(self) -> str:
        # raise error if neither text nor fields are set
        if not any([self.url, self.id]):
            raise RequiredFieldError(self, missing_field_names=["url", "id"])
        if self.url and self.id:
            raise TypeError("Setting both 'url' and 'id' on SlackFile will result in the Slack API rejecting the payload.")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {}
        if self.url:
            data["url"] = self.url
        if self.id:
            data["id"] = self.id

        return json.dumps(data)

    def build_from_json(self, json: dict[str, Any]) -> Self:
        """
        Generates a SlackFile instance from its JSON representation
        :param json: a JSON representation of a SlackFile object, e.g. from the 'blocks' property of a Slack API interaction payload
        :return: self
        """
        if not isinstance(json, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=json)
        if "url" in json.keys() and json["url"] is not None:
            self.url = json["url"]
        if "id" in json.keys() and json["id"] is not None:
            self.id = json["id"]
        return self
