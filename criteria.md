# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Four of my five questions are answerable from a single
town's own guide (e.g. Brightwater's kitchen hours, Thornby Wells being the
easiest town for limited mobility), where the fact sits in one file with
nothing competing for the embedding. My Marchwood question, though, draws its
answer from `guide_eating.md`, a cross-cutting document that discusses seven
other towns in the same section — Brightwater, Halden Bay, Pellew Sands and
more all appear near the Marchwood sentence. I expect that one to be harder to
retrieve cleanly, so I'm not requiring 5 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** Every document in `city_guides` is its own file
(`guide_brightwater.md`, `guide_eating.md`, etc.), and each chunk carries its
`source` label straight from the file it was split from — attribution is
mechanical, not something the model has to infer or guess at. There's no
step in the pipeline where a chunk could reach the answer without its source
attached, so anything less than 100% would point to a pipeline bug, not a
hard question, which is why I'm not giving this one slack the way I did for
criterion 1.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** My five out-of-scope questions (Mongolia's capital,
diesel oil changes, the 1994 World Cup, ibuprofen dosage, a Rust for-loop)
share essentially no vocabulary with a corpus of travel guides for a
fictional English-style region, so I expect their embedding distances to sit
well clear of anything real. I'm holding back from 5 of 5 because I haven't
run Milestone 4 yet and don't know if any of my out-of-scope questions
accidentally borrow guide-like phrasing — "when should I go" echoing a
"When to go" heading, for instance — that could pull one distance closer to
the cutoff than I'd like.

---

## 4. Something about your chunks

Splitting on the towns' own section headings (Getting there, Getting around,
Eat and drink, What to see, Where to stay, When to go, Practical notes), at
least 4 of 5 sampled chunks contain exactly one complete section — starting
at a heading and ending before the next one — with no heading's content
spilling into a neighboring chunk.

**Why this target:** Reading three town guides in Milestone 1, each is built
from six or seven of these labelled sections, most in the 150–400 character
range, well under the starter's 800-character fixed window. A chunker that
splits on headings should keep the great majority of sections whole; I'm
allowing one miss per five because a couple of towns (Halden Bay, Kestrelford)
pack more sentences into a single section than the others, and a section that
long might still need splitting on its own.

---

## 5. Your choice

For at least 4 of my 5 test questions, the source document named in the
answer is the one that actually contains the `expects` phrase for that
question — not merely any document from the corpus.

**Why this target:** Criterion 2 only checks that a source is *named*, which
`guide_eating.md` makes easy to satisfy without being right — it mentions
Brightwater, Marchwood, Halden Bay and five other towns by name in a single
document, so a system could cite a plausible-sounding but wrong town guide
and still "name a source." I care about attribution being correct, not just
present, since a confidently wrong citation is worse than no citation at all.
I'm setting 4 of 5 rather than 5 of 5 because my Marchwood question is the one
most likely to get misattributed to a town guide it merely mentions in
passing, for the same reason it's the hard case in criterion 1.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
