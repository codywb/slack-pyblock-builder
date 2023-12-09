import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from datetime import datetime

class Message:
    """
    A Python class representing a Message surface from the Slack API
    """
    def __init__(self):
        self._channel = ""
        self._user = ""
        self._text = ""
        self.blocks = []
        self.attachments = []
        self._ts = ""
        self._thread_ts = ""
        self._mrkdwn = True
        self._as_user = None
        self._post_at = ""
        self._icon_emoji = ""
        self._icon_url = ""
        self._link_names = None
        self._metadata = ""
        self._parse = ""
        self._reply_broadcast = False
        self._service_team_id = ""
        self._unfurl_links = None
        self._unfurl_media = None
        self._username = ""
        self._is_ephemeral = False

    def set_channel(self, channel_id: str) -> Self:
        """
        (Required) Set the id of the channel you want to post message to.
        :param channel_id: String; for DM/IMs, use the user's ID.
        :return: self
        """
        self._channel = channel_id
        return self

    def set_user(self, user_id: str) -> Self:
        """
        (Required for ephemeral messages) Sets the id of the user who will receive the message. The user must be in the
        channel specified using set_channel().
        :param user_id: String; Slack user ID
        :return: self
        """
        self._user = user_id
        return self

    def set_text(self, message_text: str) -> Self:
        """
        (Required) If using blocks, this is used to set a fallback string to display in notifications. If not, this is the
        main body text of the message. Can be formatted with as plain text, or with mrkdwn. Not enforced as required
        when using blocks but highly recommended to include as the aforementioned fallback.
        :param message_text: String
        :return: self
        """
        self._text = message_text
        return self

    def add_blocks(self, *blocks) -> Self:
        """
       (Optional) Adds one or more layout blocks to the message.
       :param blocks: One or more Block objects, e.g. Actions, Sections, Inputs
       :return: self
       """
        for block in blocks:
            self.blocks.append(block.block)
        return self

    def add_attachments(self, *attachments) -> Self:
        """
       (Optional) Adds one or more legacy secondary attachments to the message. Use of blocks is recommended.
       :param attachments: A list of one or more attachments
       :return: self
       """
        for attachment in attachments:
            self.attachments.append(attachment)
        return self

    def set_thread_ts(self, thread_ts: str) -> Self:
        """
        (Optional) Sets the ID of another un-threaded message to reply to. Avoid using a reply's ts value; use its
        parent instead!
        :param thread_ts: String
        :return: self
        """
        self._thread_ts = thread_ts
        return self

    def set_ts(self, ts: str) -> Self:
        """
        (Optional) Sets the ID of the message to update or delete.
        :param ts: String
        :return: self
        """
        self._ts = ts
        return self

    def disable_mrkdwn(self) -> Self:
        """
        (Optional) Determines whether the text field is rendered according to mrkdwn formatting or not.
        :return: self
        """
        self._mrkdwn = False
        return self

    def deliver_ephemeral(self) -> Self:
        """
        (Optional) Determines whether the message will be visible only to the recipient or not.
        :return: self
        """
        self._is_ephemeral = True
        return self

    def as_user(self) -> Self:
        """
        (Optional - Legacy) Posts the message as the authed user instead of as a bot. Defaults to False.
        Can only be used by classic Slack apps.
        :return: self
        """
        self._as_user = True
        return self

    def post_at(self, post_at: str | datetime) -> Self:
        """
        (Optional) Sets the date and time for a scheduled message to be posted.
        :param post_at: String with a Unix timestamp or Python datetime object
        :return: self
        """
        if isinstance(post_at, datetime):
            self._post_at = post_at.timestamp()
        else:
            self._post_at = post_at
        return self

    def set_icon_emoji(self, emoji_string: str) -> Self:
        """
        (Optional) Sets the emoji to use as the icon for this message. Overrides icon_url.
        :param emoji_string: String with emoji available in installed workspace, i.e. ":smile:"
        :return: self
        """
        self._icon_emoji = emoji_string
        return self

    def set_icon_url(self, icon_img_url: str) -> Self:
        """
        (Optional) Sets the url to an image for use as the icon for this message.
        :param icon_img_url: String of url to image
        :return: self
        """
        self._icon_url = icon_img_url
        return self

    def link_names(self) -> Self:
        """
        (Optional) Find and link user groups. No longer supports linking individual users; use <@user_id> syntax instead.
        :return: self
        """
        self._link_names = True
        return self

    def add_metadata(self, metadata: str) -> Self:
        """
        (Optional) Add JSON object with event_type and event_payload fields, presented as a URL-encoded string. Metadata
        posted to Slack is accessible to any app or user who is a member of that workspace. WARNING: Setting this
        attribute will prevent a scheduled message from being posted.
        :param metadata: JSON object as URL-encoded string
        :return: self
        """
        self._metadata = metadata
        return self

    def disable_auto_parsing(self) -> Self:
        """
        (Optional) Disables automatic parsing of mrkdwn, URLs, and mentions in the message text.
        :return: self
        """
        self._parse = "none"
        return self

    def broadcast_reply_to_channel(self) -> Self:
        """
        (Optional) Posts message simultaneously to the whole channel for improved visibility. Requires that thread_ts
        also be set to function correctly.
        :return: self
        """
        self._reply_broadcast = True
        return self

    def set_service_team_id(self, team_id: str) -> Self:
        """
        (Optional) Sets the Team ID corresponding to the selected app installation for messages in App Home.
        :param team_id: String
        :return: self
        """
        self._service_team_id = team_id
        return self

    def unfurl_links(self) -> Self:
        """
        (Optional) Enable unfurling of links to primarily text-based content. By default, links to media are unfurled
        but links to text content are not.
        :return: self
        """
        self._unfurl_links = True
        return self

    def disable_unfurl_media(self) -> Self:
        """
        (Optional) Disable unfurling of links to media content. By default, links to media are unfurled but links to
        text content are not.
        :return: self
        """
        self._unfurl_media = False
        return self

    def set_username(self, username: str) -> Self:
        """
        (Optional) Set the username of the bot sending the message.
        :param username: String
        :return: self
        """
        self._username = username
        return self

    def post(self, slack_client):
        """
        Uses the attributes set on the class to generate a message payload and passes it to either the chat.postMessage
        or chat.postEphemeral Web API methods of the Slack Bolt for Python client depending on the value of is_ephemeral
        OR to the chat.scheduleMessage Web API method if post_at is set.
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: Slack API response
        """
        payload = {}
        for k, v in self.__dict__.items():
            if v:
                payload[k.strip("_")] = v

        if self._is_ephemeral:
            result = slack_client.chat_postEphemeral(**payload)
        elif self._post_at:
            result = slack_client.chat_scheduleMessage(**payload)
        else:
            result = slack_client.chat_postMessage(**payload)
        return result

    def delete(self, slack_client):
        """
        Deletes an existing message
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: Slack API response
        """
        payload = {}
        for k, v in self.__dict__.items():
            if v:
                payload[k.strip("_")] = v

        result = slack_client.chat_delete(**payload)
        return result

    def update(self, slack_client):
        """
        Updates an existing message
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :return: Slack API response
        """
        payload = {}
        for k, v in self.__dict__.items():
            if v:
                payload[k.strip("_")] = v

        result = slack_client.chat_update(**payload)
        return result

    def get_list_of_scheduled_messges(self, slack_client, latest=None, oldest=None) -> list:
        """
        Fetches a list of all messages scheduled to be posted by the app.
        :param slack_client: an instance of the Slack Bolt for Python's app.client
        :param latest: (Optional) Ending date of range to look for scheduled messages as Unix timestamp  or Python datetime object
        :param oldest: (Optional) Starting  date of range to look for scheduled messages as Unix timestamp  or Python datetime object
        :return: A list of scheduled messages
        """
        result = slack_client.chat_scheduledMessages_list(
            channel=self._channel if self._channel else None,
            latest=latest if latest else None,
            oldest=oldest if oldest else None
        )
        return result
