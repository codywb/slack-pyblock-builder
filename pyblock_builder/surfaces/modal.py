import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pyblock_builder.objects.text import Text


class Modal:
    """
    A Python class representing a Modal surface from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._type = "modal"
        self._callback_id = ""
        self.blocks = []
        self._private_metadata = ""
        self._external_id = ""
        self._title = {}
        self._submit = None
        self._close = None
        self._clear_on_close = False
        self._notify_on_close = False
        self._submit_disabled = False
        self.view = {
            "type": self._type,
            "callback_id": self._callback_id,
            "blocks": self.blocks
        }

    def set_callback_id(self, callback_id: str) -> Self:
        """
        (Optional) Sets an identifier to recognize interactions and submissions of this particular view. Don't use to
        store sensitive information (use private_metadata instead).
        :param callback_id: String; max 255 chars
        :return: self
        """
        self._callback_id = callback_id
        self.view["callback_id"] = self._callback_id
        return self

    def set_external_id(self, external_id: str) -> Self:
        """
        (Optional) Sets a custom identifier that must be unique for all views on a per-team basis
        :param external_id: String; max 255 chars
        :return: self
        """
        self._external_id = external_id
        self.view["external_id"] = self._external_id
        return self

    def set_private_metadata(self, metadata: str) -> Self:
        """
        (Optional) Sets an optional string that will be sent to your app in views_submission and block_actions events
        :param metadata: String; max 3,000 chars
        :return: self
        """
        self._private_metadata = metadata
        self.view["private_metadata"] = self._private_metadata
        return self

    def add_blocks(self, *blocks) -> Self:
        """
        (Required) Adds the blocks that define the content of the View
        :param blocks: One or more blocks; max 100; use * when passing a list
        :return: self
        """
        for block in blocks:
            self.blocks.append(block.block)
        self.view["blocks"] = self.blocks
        return self

    def set_title(self, title_text: str) -> Self:
        """
        Sets the title that appears in the top-left corner of the Modal
        :param title_text: String; max 24 chars
        :return: self
        """
        self._title = Text().set_text(title_text)
        self.view["title"] = self._title.json
        return self

    def set_submit_label(self, submit_text: str) -> Self:
        """
        (Optional) Sets a custom label for the submit button at the bottom-right of the view. Required when an Input
        block is included in blocks.
        :param submit_text: String; max 24 chars
        :return: self
        """
        self._submit = Text().set_text(submit_text)
        self.view["submit"] = self._submit.json
        return self

    def set_close_label(self, close_text: str) -> Self:
        """
        (Optional) Sets a custom label for the close button at the bottom-right of the view
        :param close_text: String; max 24 chars
        :return: self
        """
        self._close = Text().set_text(close_text)
        self.view["close"] = self._close.json
        return self

    def clear_on_close(self) -> Self:
        """
        (Optional) When set to True, clicking on the close button will clear all views in a modal and close it
        :return: self
        """
        self._clear_on_close = True
        self.view["clear_on_close"] = self._clear_on_close
        return self

    def notify_on_close(self) -> Self:
        """
        (Optional) Indicates whether Slack will send your request URL a view_closed event when a user clicks the
        close button
        :return: self
        """
        self._notify_on_close = True
        self.view["notify_on_close"] = self._notify_on_close
        return self

    def submit_disabled(self) -> Self:
        """
        (Optional) When set to True, disables the submit button until the user has completed one or more inputs.
        This property is for configuration Modals.
        :return: self
        """
        self._submit_disabled = True
        self.view["submit_disabled"] = self._submit_disabled
        return self

    def open_view(self, request_body, slack_client):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.open Web API method
        of the Slack Bolt for Python client.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: nothing
        """
        slack_client.views_open(
            trigger_id=request_body["trigger_id"],
            view_id=request_body["view"]["id"],
            hash=request_body["view"]["hash"],
            view=self.view
        )

    def update_view(self, request_body, slack_client):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.update Web API method
        of the Slack Bolt for Python client.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: nothing
        """
        slack_client.views_update(
            view_id=request_body["view"]["id"],
            hash=request_body["view"]["hash"],
            view=self.view
        )

    def push_view(self, request_body, slack_client):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.push Web API method
        of the Slack Bolt for Python client. Only two additional views may be pushed after opening a Modal.
        :param response_body: the response passed to the app from the Slack API
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: nothing
        """
        slack_client.views_push(
            trigger_id=request_body["trigger_id"],
            view_id=request_body["view"]["id"],
            hash=request_body["view"]["hash"],
            view=self.view
        )

    def update_view_from_submission(self, ack):
        """
        Uses the attributes set on the class to generate a view payload and update a view by passing a response_action
        of type "update" with a newly composed view. Use when responding to a views_submission request (i.e., when a
        views payload includes any input blocks).
        :param ack: the ack() function received from the Slack Bolt for Python framework
        :return: nothing
        """
        ack(response_action="update", view=self.view)

    def push_view_from_submission(self, ack):
        """
        Uses the attributes set on the class to generate a view payload and push a new view on top of an existing view
        by passing a response_action of type "push" with the newly composed view. Only two additional views may be
        pushed after opening a Modal. Use when responding to a views_submission request (i.e., when a
        views payload includes any input blocks).
        :param ack: the ack() function received from the Slack Bolt for Python framework
        :return: nothing
        """
        ack(response_action="push", view=self.view)