import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class AppHome:
    """
    A Python class representing an App Home surface from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._type = "home"
        self._callback_id = ""
        self.blocks = []
        self._private_metadata = ""
        self._external_id = ""
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
        (Optional) Sets an optional string that will be sent to your app in views_submission and block_actions
        events
        :param metadata: String; max 3,000 chars
        :return: self
        """
        self._private_metadata = metadata
        self.view["private_metadata"] = self._private_metadata
        return self

    def add_blocks(self, *blocks) -> Self:
        """
        (Required) Adds the blocks that define the content of the View.
        :param blocks: One or more blocks; max 100
        :return: self
        """
        for block in blocks:
            self.blocks.append(block.block)
        self.view["blocks"] = self.blocks
        return self

    def publish_view(self, slack_client, payload, logger):
        """
        Uses the attributes set on the class to generate a view payload and passes it to the views.publish Web API
        methods of the Slack Bolt for Python client.
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :param payload: the event or other API response payload passed to the app from the Slack API
        :param logger: instance of logger to correctly log API errors
        :return: nothing
        """
        if payload["type"] == "app_home_opened":
            user_id = payload["user"]
        else:
            user_id = payload["user"]["id"]
        try:
            slack_client.views_publish(
                user_id=user_id,
                view=self.view
            )
        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")
