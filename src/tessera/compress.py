"""Block compression codecs for Tessera postings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Block:
    """A monotone list of document ids with a shared base."""

    base: int
    deltas: List[int]

    @classmethod
    def from_ids(cls, ids: List[int]) -> "Block":
        if not ids:
            return cls(base=0, deltas=[])
        ordered = sorted(set(ids))
        base = ordered[0]
        return cls(base=base, deltas=[b - a for a, b in zip(ordered, ordered[1:])])

    def to_ids(self) -> List[int]:
        if not self.deltas:
            return [self.base]
        out = [self.base]
        for delta in self.deltas:
            out.append(out[-1] + delta)
        return out

    def nbytes(self) -> int:
        return 8 + sum(1 if d < 256 else 2 for d in self.deltas)


def encode_blocks(postings: dict[str, List[int]], block_size: int = 128) -> dict[str, List[Block]]:
    encoded: dict[str, List[Block]] = {}
    for term, ids in postings.items():
        encoded[term] = [
            Block.from_ids(ids[i : i + block_size]) for i in range(0, len(ids), block_size)
        ]
    return encoded
