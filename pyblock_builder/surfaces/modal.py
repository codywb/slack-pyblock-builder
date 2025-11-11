import sys

if sys.version_info >= (3, 11):
    from typing import Self, Literal, Any, Sequence
else:
    from typing_extensions import Self, Literal, Any, Sequence
from dataclasses import dataclass, field
import json
from pyblock_builder._internal.errors import (TextLengthError, RequiredFieldsError, IncorrectTypeError, ItemLengthError)
from pyblock_builder.base_blocks import Block
from pyblock_builder.objects import PlainText
from pyblock_builder.blocks import *

@dataclass
class Modal:
    """
    Modal view objects are used within the following Web API methods: views.open, views.update, views.push.
    Non-standard characters (including characters with diacritics) within view objects are converted and sent in
    unicode format when you receive the view callback payloads.
    """
    type: Literal["modal"] = "modal"
    title: PlainText | None = None
    blocks: list[Block] | None = field(default_factory=list)
    close: PlainText | None = None
    submit: PlainText | None = None
    private_metadata: str | None = None
    callback_id: str | None = None
    clears_on_close: bool = False
    notifies_on_close: bool = False
    external_id: str | None = None
    submit_disabled: bool | None = None

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

    def set_title(self, title_text: PlainText) -> Self:
        """
        Sets the title that appears in the top-left of the modal.
        :param title: PlainText object; max 24 characters
        :return: self
        """
        if not isinstance(title_text, PlainText):
            raise IncorrectTypeError(self, method="set_title", compatible_types=PlainText, incompatible_type=title_text)
        if not 1 <= len(title_text.text) < 24:
            raise TextLengthError(self, field="text", min_length=1, max_length=24)
        self.title = title_text
        return self

    def set_submit_label(self, submit_text: PlainText) -> Self:
        """
        (Optional) Sets a custom label for the submit button at the bottom-right of the view. Required when an Input
        block is included in blocks.
        :param submit_text: PlainText object; max 24 chars
        :return: self
        """
        if not isinstance(submit_text, PlainText):
            raise IncorrectTypeError(self, method="set_submit_label", compatible_types=PlainText, incompatible_type=submit_text)
        if not 1 <= len(submit_text.text) < 24:
            raise TextLengthError(self, field="text", min_length=1, max_length=24)
        self.submit = submit_text
        return self

    def set_close_label(self, close_text: PlainText) -> Self:
        """
        (Optional) Sets a custom label for the close button at the bottom-right of the view
        :param close_text: PlainText object; max 24 chars
        :return: self
        """
        if not isinstance(close_text, PlainText):
            raise IncorrectTypeError(self, method="set_close_label", compatible_types=PlainText,
                                     incompatible_type=close_text)
        if not 1 <= len(close_text.text) < 24:
            raise TextLengthError(self, field="text", min_length=1, max_length=24)
        self.close = close_text
        return self

    def clear_on_close(self) -> Self:
        """
        (Optional) When set to True, clicking on the close button will clear all views in a modal and close it.
        :return: self
        """
        self.clears_on_close = True
        return self

    def notify_on_close(self) -> Self:
        """
        (Optional) Indicates whether Slack will send your request URL a view_closed event when a user clicks the
        close button.
        :return: self
        """
        self.notifies_on_close = True
        return self

    def disable_submit(self) -> Self:
        """
        (Optional) When set to True, disables the submit button until the user has completed one or more inputs.
        This property is for legacy configuration modals.
        :return: self
        """
        self.submit_disabled = True
        return self

    def build_to_json(self) -> Self:
        # raise error if required fields are not set
        if any([field is None for field in [self.blocks, self.title]]):
            raise RequiredFieldsError(self, missing_field_names=["blocks", "title"])
        for block in self.blocks:
            if isinstance(block, Input):
                if not self.submit:
                    raise Exception("The 'submit' field is required when an Input block is included in a Modal's blocks array.")

        # return JSON representation of object using only non-empty fields and removing leading underscores
        data: dict[str, Any] = {
            "type": self.type,
            "title": json.loads(self.title.build_to_json()),
            "blocks": [json.loads(block.build_to_json()) for block in self.blocks],
        }
        if self.private_metadata:
            data["private_metadata"] = self.private_metadata
        if self.callback_id:
            data["callback_id"] = self.callback_id
        if self.external_id:
            data["external_id"] = self.external_id
        if self.close:
            data["close"] = json.loads(self.close.build_to_json())
        if self.submit:
            data["submit"] = json.loads(self.submit.build_to_json())
        if self.clears_on_close:
            data["clear_on_close"] = self.clears_on_close
        if self.notifies_on_close:
            data["notify_on_close"] = self.notifies_on_close
        if self.submit_disabled:
            data["submit_disabled"] = self.submit_disabled

        return json.dumps(data)

    def build_from_json(self, view: dict[str, Any]) -> Self:
        """
        Generates a Modal instance
        :param view: the contents of a "view" property of a Slack API interaction payload from an interactive component
        """
        if not isinstance(view, dict):
            raise IncorrectTypeError(self, method="build_from_json", compatible_types=dict, incompatible_type=view)
        if "private_metadata" in view.keys() and view["private_metadata"] is not None:
            self.private_metadata = view["private_metadata"]
        if "external_id" in view.keys() and view["external_id"] is not None:
            self.external_id = view["external_id"]
        if "callback_id" in view.keys() and view["callback_id"] is not None:
            self.callback_id = view["callback_id"]
        if "close" in view.keys() and view["close"] is not None:
            self.close = PlainText().build_from_json(view["close"])
        if "submit" in view.keys() and view["submit"] is not None:
            self.submit = PlainText().build_from_json(view["submit"])
        if "clear_on_close" in view.keys() and view["clear_on_close"] is not None:
            self.clears_on_close = view["clear_on_close"]
        if "notify_on_close" in view.keys() and view["notify_on_close"] is not None:
            self.notifies_on_close = view["notify_on_close"]
        if "submit_disabled" in view.keys() and view["submit_disabled"] is not None:
            self.submit_disabled = view["submit_disabled"]
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
        self.title = PlainText().build_from_json(view["title"])
        return self

    def open_view(self, request_body, slack_client):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.open Web API method
        of the Slack Bolt for Python client.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: Slack API response
        """
        result = slack_client.views_open(
            trigger_id=request_body["trigger_id"],
            view_id=request_body["view"]["id"],
            hash=request_body["view"]["hash"],
            view=self.build_to_json()
        )
        return result

    def update_view(self, request_body, slack_client, view_id=None, exclude_hash=False):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.update Web API method
        of the Slack Bolt for Python client.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :param view_id: (Optional) Required to update a view after the initial 3-second timeout
        :param exclude_hash: (Optional) Can be used to disable the inclusion of a hash value. May be necessary when updating a view after 3-second timeout
        :return: Slack API response
        """
        if not view_id:
            view_id = request_body["view"]["id"]

        if not exclude_hash:
            result = slack_client.views_update(
                view_id=view_id,
                hash=request_body["view"]["hash"],
                view=self.build_to_json()
            )
        else:
            result = slack_client.views_update(
                view_id=view_id,
                view=self.build_to_json()
            )
        return result

    def push_view(self, request_body, slack_client):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.push Web API method
        of the Slack Bolt for Python client. Only two additional views may be pushed after opening a Modal.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: Slack API response
        """
        result = slack_client.views_push(
            trigger_id=request_body["trigger_id"],
            view_id=request_body["view"]["id"],
            hash=request_body["view"]["hash"],
            view=self.build_to_json()
        )
        return result

    def update_view_from_submission(self, ack):
        """
        Uses the attributes set on the class to generate a view payload and update a view by passing a response_action
        of type "update" with a newly composed view. Use when responding to a views_submission request (i.e., when a
        views payload includes any input blocks).
        :param ack: the ack() function received from the Slack Bolt for Python framework
        :return: Slack API response
        """
        result = ack(response_action="update", view=self.build_to_json())
        return result

    def push_view_from_submission(self, ack):
        """
        Uses the attributes set on the class to generate a view payload and push a new view on top of an existing view
        by passing a response_action of type "push" with the newly composed view. Only two additional views may be
        pushed after opening a Modal. Use when responding to a views_submission request (i.e., when a
        view payload includes any input blocks).
        :param ack: the ack() function received from the Slack Bolt for Python framework
        :return: Slack API response
        """
        result = ack(response_action="push", view=self.build_to_json())
        return result
