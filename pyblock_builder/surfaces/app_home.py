import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.base_blocks import Block
from pyblock_builder.blocks import *

@dataclass
class AppHome:
    """
    The Home tab is available only for Bolt apps, not apps created with the Deno Slack SDK.
    Home tab view objects are used within the views.publish Web API method.
    """
    type: Literal["home"] = "home"
    blocks: list[Block] | None = field(default_factory=list)
    private_metadata: str | None = None
    callback_id: str | None = None
    external_id: str | None = None

    def add_blocks(self, *blocks: Block | Sequence[Block]) -> Self:
        """
        Add one or more blocks that defines the content of the view.
        :param blocks: one or more Block objects or a list/tuple of Block objects; max 100 blocks
        :return: self
        """
        flattened_blocks = []
        for block in blocks:
            if isinstance(block, (list, tuple)):
                flattened_blocks.extend(block)
            else:
                flattened_blocks.append(block)

        if not 1 <= len(flattened_blocks) <= 100:
            raise ItemLengthError(self, field="blocks", min_length=1, max_length=100)

        for block in flattened_blocks:
            if not isinstance(block, Block):
                raise IncorrectTypeError(self, method="set_blocks", compatible_types=Block, incompatible_type=block)
            self.blocks.append(block)
        return self

    def set_private_metadata(self, metadata: str) -> Self:
        """
        (Optional) Defines a string that will be sent to your app in view_submission and block_actions events.
        :param metadata: string; max 3,000 characters
        :return: self
        """
        if not isinstance(metadata, str):
            raise IncorrectTypeError(self, method="set_private_metadata", compatible_types=str, incompatible_type=metadata)
        if not 1 <= len(metadata) <= 3000:
            raise TextLengthError(self, field="private_metadata", min_length=1, max_length=3000)
        self.private_metadata = metadata
        return self

    def set_callback_id(self, callback_id: str) -> Self:
        """
        (Optional) Sets an identifier to recognize interactions and submissions of this particular view.
        Don't use this to store sensitive information (use private_metadata instead).
        :param callback_id: string; max 255 characters
        :return: self
        """
        if not isinstance(callback_id, str):
            raise IncorrectTypeError(self, method="set_callback_id", compatible_types=str, incompatible_type=callback_id)
        if not 1 <= len(callback_id) <= 255:
            raise TextLengthError(self, field="callback_id", min_length=1, max_length=255)
        self.callback_id = callback_id
        return self

    def set_external_id(self, external_id: str) -> Self:
        """
        (Optional) Sets a custom identifier that must be unique for all views on a per-team basis.
        :param external_id: string
        :return: self
        """
        if not isinstance(external_id, str):
            raise IncorrectTypeError(self, method="set_external_id", compatible_types=str, incompatible_type=external_id)
        self.external_id = external_id
        return self

    def build_to_json(self) -> Self:
        # raise error if required fields are not set
        if not self.blocks:
            raise RequiredFieldError(self, missing_field_names="blocks")
        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "blocks": [json.loads(block.build_to_json()) for block in self.blocks],
        }
        if self.private_metadata:
            data["private_metadata"] = self.private_metadata
        if self.callback_id:
            data["callback_id"] = self.callback_id
        if self.external_id:
            data["external_id"] = self.external_id

        return json.dumps(data)

    def build_from_json(self, view: dict[str, Any]) -> Self:
        """
        Generates an AppHome instance
        :param view: the contents of a "view" property of a Slack API interaction payload from an interactive component used in a Home tab
        """
        if not isinstance(view, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=view)
        if "private_metadata" in view.keys() and view["private_metadata"] is not None:
            self.private_metadata = view["private_metadata"]
        if "external_id" in view.keys() and view["external_id"] is not None:
            self.external_id = view["external_id"]
        if "callback_id" in view.keys() and view["callback_id"] is not None:
            self.callback_id = view["callback_id"]
        compatible_types = {
            "actions": Actions,
            "context": Context,
            "context_actions": ContextActions,
            "divider": Divider,
            "file": File,
            "header": Header,
            "image": Image,
            "input": Input,
            "markdown": Markdown,
            "rich_text": RichText,
            "section": Section,
            "table": Table,
            "video": Video,
        }
        self.blocks = [compatible_types[block["type"]]().build_from_json(block) for block in view["blocks"]]
        return self

    def publish_view(self, slack_client, payload, logger):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.publish Web API
        methods of the Slack Bolt for Python client.
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :param payload: the event or other API response payload passed to the app from the Slack API
        :param logger: instance of logger to correctly log API errors
        :return: Slack API response
        """
        if payload["type"] == "app_home_opened":
            user_id = payload["user"]
        else:
            user_id = payload["user"]["id"]
        try:
            result = slack_client.views_publish(
                user_id=user_id,
                view=self.build_to_json()
            )
            return result
        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")