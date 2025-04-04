from typing import Protocol, List

class Buiildable(Protocol):
    def build_to_json(self):
        pass


class Block(Protocol):
    _type: str| None
    _block_id: str| None

    def build_to_json(self):
        pass


class Element(Protocol):
    _type: str| None
    _action_id: str| None

    def build_to_json(self):
        pass


class Surface(Protocol):
    _blocks: List[Block] | None

    def add_blocks(self, *blocks: List[Block]):
        pass
