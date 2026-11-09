"""Segment layout and query execution for Tessera-Retrieval."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .compress import Block, encode_blocks


@dataclass
class Segment:
    name: str
    postings: Dict[str, List[int]] = field(default_factory=dict)
    shared_meta: Dict[str, int] = field(default_factory=dict)

    def add(self, doc_id: int, text: str) -> None:
        for token in text.lower().split():
            self.postings.setdefault(token, []).append(doc_id)

    def finalise(self) -> "Segment":
        self.shared_meta["terms"] = len(self.postings)
        self.shared_meta["postings"] = sum(len(v) for v in self.postings.values())
        return self

    def search(self, term: str) -> List[int]:
        blocks = encode_blocks({term: self.postings.get(term, [])}).get(term, [])
        results: List[int] = []
        for block in blocks:
            results.extend(block.to_ids())
        return results


def load_corpus(path: str) -> Segment:
    segment = Segment(name=Path(path).stem)
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            segment.add(int(row["id"]), row["text"])
    return segment.finalise()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    segment = load_corpus(args.corpus)
    print({"term": args.query, "hits": segment.search(args.query), "meta": segment.shared_meta})


if __name__ == "__main__":
    main()
