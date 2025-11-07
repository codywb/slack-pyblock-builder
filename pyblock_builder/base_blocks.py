import sys

if sys.version_info >= (3, 11):
    from typing import Protocol, List, Literal, runtime_checkable, Self
else:
    from typing_extensions import Protocol, List, Literal, runtime_checkable, Self

class Buiildable(Protocol):
    def build_to_json(self) -> str:
        pass

@runtime_checkable
class Block(Protocol):
    type: str| None
    block_id: str| None

    def build_to_json(self) -> str:
        pass

    def set_block_id(self, block_id: str) -> Self:
        pass

@runtime_checkable
class Element(Protocol):
    type: str | None
    action_id: str| None

    def build_to_json(self) -> str:
        pass

    def set_action_id(self, action_id: str) -> Self:
        pass

@runtime_checkable
class Surface(Protocol):
    blocks: List[Block] | None

    def add_blocks(self, *blocks: List[Block]) -> Self:
        pass

@runtime_checkable
class RichTextElement(Protocol):
    type: str = Literal["broadcast", "color", "channel", "date", "emoji", "link", "text", "user", "usergroup"]

    def build_to_json(self) -> str:
        pass

@runtime_checkable
class RichTextObject(Protocol):
    type: str = Literal["rich_text_section", "rich_text_list", "rich_text_preformatted", "rich_text_quote"]
    elements: list | None

    def add_elements(self, *elements) -> Self:
        pass

    def build_to_json(self) -> str:
        pass