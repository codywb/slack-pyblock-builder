def blockquote(text: str) -> str:
    """
    Converts a string into a blockquote.
    :param text: String
    :return: str
    """
    bq = []
    for line in text.split("\n"):
        bq.append(f">{line}")
    return ("\n").join(bq)

def bold(text: str) -> str:
    """
    Makes a string bold
    :param text: String
    :return: str
    """
    return f"*{text}*"

def italic(text: str) -> str:
    """
    Makes a string italic
    :param text: String
    :return: str
    """
    return f"_{text}_"

def strike(text: str) -> str:
    """
    Makes a string strikethrough text
    :param text: String
    :return: str
    """
    return f"~{text}~"

def inline_code(text: str) -> str:
    """
    Creates an inline block of code
    :param text: String
    :return: str
    """
    return f"`{text}`"

def codeblock(text: str) -> str:
    """
    Turns a string into a multi-line block of code.
    :param text: String
    :return: str
    """
    return f"```{text}```"

def dashed_list(items: str | list) -> str:
    """
    Creates a dashed list.
    :param items: String or List of Strings
    :return: str
    """
    if isinstance(items, list):
        dl = []
        for item in items:
            dl.append(f"- {item}")
        return "\n".join(dl)
    elif isinstance(items, str):
        return f"- {items}"
    else:
        return "Invalid type. Must be string or list."


def bullet_list(items: str | list) -> str:
    """
    Creates a bulleted list.
    :param items: String or List of Strings
    :return: str
    """
    if isinstance(items, list):
        bl = []
        for item in items:
            bl.append(f"• {item}")
        return "\n".join(bl)
    elif isinstance(items, str):
        return f"- {items}"
    else:
        return "Invalid type. Must be string or list."

def link(url: str, link_text=None) -> str:
    """
    Creates a clickable link from a url
    :param url: String
    :param link_text: String; Optional text to display instead of the url itself. If not provided, the url alone will
    be shown.
    :return: str
    """
    if link_text:
        return f"<{url}|{link_text}>"
    return f"<{url}>"

def mailto(email: str, link_text=None) -> str:
    """
    Creates a clickable link from an email address
    :param email: String; email address
    :param link_text: String; Optional text to display instead of the email address. If not provided, the address alone
    will be displayed.
    :return: str
    """
    if link_text:
        return f"<mailto:{email}|{link_text}>"
    return f"<mailto:{email}|{email}>"

def emoji(name: str) -> str:
    """
    Formats a string to create an emoji in Slack
    :param name: String; the name of the emoji to be created
    :return: str
    """
    return f":{name}:"

def user(user_id: str) -> str:
    """
    Mentions a user by their Slack ID
    :param user_id: String; Slack ID of the user to be mentioned
    :return: str
    """
    return f"<@{user_id}>"

def channel(channel_id: str) -> str:
    """
    Creates a clickable link to a Slack channel
    :param channel_id: String; ID of the Slack channel to which a link should be created
    :return: str
    """
    return f"<#{channel_id}>"

def group(group_id: str) -> str:
    """
    Mentions a Slack user group by ID
    :param group_id: String; Group ID of the Slack group to be mentioned. Can also be "here", "channel", or "everyone".
    :return: str
    """
    special = ["here", "channel", "everyone"]
    if group_id in special:
        return f"<!{group_id}>"
    return f"<!subteam^{group_id}>"

