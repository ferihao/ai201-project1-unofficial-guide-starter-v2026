# The Unofficial Guide

Feriha Ozturk — `city_guides` corpus.

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a retrieval-augmented question-answering system over `city_guides`,
fourteen long travel guides for a fictional English-style region — nine
towns plus five cross-cutting guides (eating, walking, regional transport,
seasons, accessibility). Ask it something a guide would actually cover —
when a town's kitchens stop serving, which town is easiest to get around
with limited mobility, why Marchwood's good restaurants are a tram ride
away — and it retrieves the relevant passage, cites the file it came from,
and answers only from that text. Ask it something the guides don't cover
(capital cities, medication dosages, programming syntax) and it says so
instead of guessing.

## Chunking Strategy

**Chunk size:** 900 characters (cap, not a fixed window)
**Overlap:** 100 characters (only used if a section exceeds the cap)


## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

## Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
## When to go

May to September. Outside those months the pub in the third village closes, the farm shop reduces its hours, and several footpaths become genuinely boggy rather than merely wet. The road is not gritted above the second village and is impassable in snow.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
## Eat and drink

A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
## Where to stay

Two inns on the square and a handful of rooms above the pubs. Booking ahead matters between May and September and not at all otherwise. There is no accommodation of any kind within four miles of the town in either direction.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Why does the good food in Marchwood require a tram ride instead of just walking one street over?

**Answer:**

```
According to `guide_eating.md`, Marchwood is the exception to the region's
pattern because its good district—Northgate—is a tram ride away rather than
a street away, and the area immediately around the station is uniformly poor.

Sources retrieved: guide_accessibility.md, guide_eating.md, guide_kestrelford.md, guide_marchwood.md, guide_pellew_sands.md, guide_thornby_wells.md
```

**My relevance cutoff:** 0.64

In-corpus questions topped out at 0.467; out-of-scope questions bottomed out
at 0.813 — a clean 0.346-wide gap with nothing from either group anywhere
near the middle. This corpus's vocabulary (town names, "tram," "kitchen,"
"seafront") apparently shares almost nothing with the out-of-scope topics, so
the two groups separated cleanly rather than crowding the cutoff. I set the
threshold at the midpoint of the gap, 0.64, so an unusually weak in-corpus
match and an unusually close out-of-scope match both still have equal
(0.17) margin before they'd flip the gate's decision.

| Question | In corpus? | Best distance |
|---|---|---|
| What time do kitchens in Brightwater stop serving food, and how does that differ from what visitors expect? | Yes | 0.467 |
| Which town in the region is the easiest to get around with limited mobility? | Yes | 0.452 |
| Why does the good food in Marchwood require a tram ride instead of just walking one street over? | Yes | 0.321 |
| How often does the local bus run in Brightwater, and does it operate on Sundays? | Yes | 0.263 |
| What happened to the mill building in Brightwater, and how long should a visit take? | Yes | 0.337 |
| What is the capital of Mongolia? | No | 0.827 |
| How do I change the oil in a diesel engine? | No | 0.903 |
| Who won the 1994 World Cup? | No | 0.975 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.846 |
| How do I write a for loop in Rust? | No | 0.813 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write `chunker.py::split_documents` to split on the
towns' own `##` headings instead of the fixed 800-character window, after we
measured that the corpus's 98 sections run 23-711 characters. It wrote the
splitter correctly, but I didn't catch that it never re-ran `python app.py
index` afterward — so when I asked it to run Milestone 4's retrieval tests
right after, the results were quietly coming from the *old* index, built by
the original fixed-size chunker, not the new one. The chunk previews didn't
match what the new function should have produced, which is what gave it
away. It re-ran `index` to rebuild the embeddings from the new chunks, and
the retrieval numbers changed once it did — one of the three test questions
went from a broken result (the correct chunk not among the top matches) to
finding it exactly, once it was actually querying the right index.

**2.** I asked Claude to pick `TOP_K` and the relevance threshold. Rather
than just taking the starter's suggested "start at 4 or 5," it tested 5, 6,
7, and 8 against my actual test questions and found that at 5, one town's
own "Eat and drink" section never came back at all — it was crowded out by
near-identical sections from other towns that share the same heading and
vocabulary. It picked 7 as the minimum value that fixed that one case
without adding much extra noise to the other questions, instead of just
raising it arbitrarily. For the threshold, it ran all five in-corpus and
five out-of-scope questions and set the cutoff at the midpoint of the actual
gap between them (0.64) rather than leaving the starter's default in place.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
