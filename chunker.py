"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_sections(text: str) -> list[str]:
    """
    Break one document's text on its `##` headings.

    The bare title before the first `##` (e.g. "# Walking in the region",
    23-27 characters in this corpus) carries no content on its own, so it is
    merged onto the front of the first real section instead of becoming its
    own fragment.
    """
    pieces = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    pieces = [p.strip() for p in pieces if p.strip()]

    if len(pieces) > 1 and not pieces[0].startswith("##"):
        pieces[1] = pieces[0] + "\n\n" + pieces[1]
        pieces = pieces[1:]

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on the town guides' own `##` section headings.

    Milestone 1 read three guides and found each one built from 6-7 labelled
    sections (Getting there, Eat and drink, When to go, ...). Measuring all 98
    sections across the corpus put them between 23 and 711 characters, average
    293 — comfortably inside a single chunk. A fixed 800-character window (the
    fallback) ignores those headings and slices straight through them instead.

    CHUNK_SIZE (900) is a cap, not a target: it sits above the longest section
    actually observed (711), so no real section gets split. It only bites if a
    section runs longer than anything seen so far, in which case it falls back
    to a character-window split with CHUNK_OVERLAP (100) so a sentence caught
    at the cut keeps a little context on both sides.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks: list[Chunk] = []
    for doc in documents:
        index = 0
        for section in _split_sections(doc.text):
            if len(section) <= chunk_size:
                chunks.append(
                    Chunk(
                        text=section,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
                continue

            # An outsized section: fall back to a character window so it
            # still gets chunked, rather than shipped as one huge blob.
            start = 0
            while start < len(section):
                piece = section[start : start + chunk_size].strip()
                if piece:
                    chunks.append(
                        Chunk(
                            text=piece,
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                start += chunk_size - overlap

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
