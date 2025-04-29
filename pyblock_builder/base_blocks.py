from typing import Protocol, List

class Buiildable(Protocol):
    def build_to_json(self):
        pass


class Block(Protocol):
    type: str| None
    block_id: str| None

    def build_to_json(self):
        pass


class Element(Protocol):
    type: str| None
    action_id: str| None

    def build_to_json(self):
        pass


class Surface(Protocol):
    blocks: List[Block] | None

    def add_blocks(self, *blocks: List[Block]):
        pass
