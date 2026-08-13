# Human-centered design checklist

Run every requirement that touches a **constraint**, a **destructive or irreversible
action**, or **generated/uncertain content** through this list. Each principle below
states the rule, the smell that violates it, and a concrete "before → after" of how it
changes a requirement. These are the heuristics that separate a feature that technically
works from one a person can actually trust and use.

---

## 1. Knowledge in the world (visible constraints)
**Rule:** put the information needed to act correctly *in front of the user*, before they
act — don't rely on them remembering it or discovering it via an error.
**Smell:** a limit enforced only as an after-the-fact rejection ("File too large").
**Before → after:** "Reject PDFs over 50 MB." → "The drop zone states the accepted type
and limits up front ('PDF · ≤ 50 MB · ≤ ~300 pages'); a file violating a limit is rejected
at *selection* time with the specific reason, before any processing starts."

## 2. Informative feedback
**Rule:** every action gets immediate, meaningful feedback; long operations expose *what
stage* they're at, not just that they're busy.
**Smell:** an undifferentiated spinner; a control that looks active but gives no response.
**Before → after:** "Show a loading state during processing." → "Progress is shown as named
stages (extracting text → finding concepts → writing pages → linking) with a rough estimate
that updates as work proceeds." And: every flag/bookmark/tag action produces an immediate
toast *and* a persistent indicator.

## 3. Reversibility
**Rule:** prefer undo over confirm-only; make recovery from mistakes cheap, especially when
an action modifies existing user data in place.
**Smell:** a one-way destructive action guarded only by an "Are you sure?" dialog.
**Before → after:** "Confirm before deleting a source." → "Removing a source is reversible
immediately afterwards (undo); and because incremental ingest modifies pages in place, every
ingest writes a new version per affected page so any page can be restored to its pre-ingest
state from its history."

## 4. Show consequences before destructive actions
**Rule:** before an irreversible or far-reaching action, show its *full* blast radius in
plain language.
**Smell:** "Delete" that silently cascades, or a dialog full of jargon ("this will create a
redirect").
**Before → after:** "Delete source." → "Before removing, the student is shown the
consequences (how many pages and links will go)." And for a merge: "the dialog states the
outcome in plain language, per page — which page is kept and gains the other's notes, and
that the other stops being separate — with no jargon like 'redirect'."

## 5. Close the Gulf of Evaluation (direct attention)
**Rule:** when the system makes many automatic decisions, don't ask the user to audit all of
them — surface *only* the ones likely to be wrong.
**Smell:** "the user can review all placements" (so they review none).
**Before → after:** "Let the user check where pages were placed." → "After an ingest, a
'Review placement' panel lists *only* the low-confidence placements, each with a
plain-language reason and one-tap Merge / Keep actions; it's non-blocking and dismissible."
This requires the system to record a **confidence** per automatic decision.

## 6. A conceptual model the user can hold (system image)
**Rule:** the structure the system presents must match a model the user can understand and
accept; surprising organization must be traceable to *why*.
**Smell:** generic labels ("Section 1") and groupings the user can't explain.
**Before → after:** "Group pages into sections." → "Topic sections are named in the
subject's own vocabulary, not generic labels; each section/page makes visible the source(s)
and concepts it was derived from, so a surprising grouping can be traced back and judged."

## 7. Direct manipulation
**Rule:** let users fix structure by acting on the thing itself, with a preview before
commit — not by filing a request or editing config.
**Smell:** structural changes that are hard, hidden, or only possible at ingest time.
**Before → after:** "Support reorganizing pages." → "From any page, 'Merge into…' opens an
editable preview of the combined content (Edit/Preview tabs) the user adjusts before
committing; the merge is recorded in history and is reversible."

## 8. Traceability & never fabricate (trust)
**Rule:** when the product asserts facts, generates content, or answers questions, every
claim must be traceable to its source, and the system must say "I don't know" rather than
invent.
**Smell:** generated answers with no provenance; a confident answer when nothing relevant
exists.
**Before → after:** "The chatbot answers questions about the notes." → "Answers are grounded
*only* in this wiki; each claim is followed by an inline citation chip to the page it came
from; when nothing relevant is found it says so plainly rather than inventing an answer."

## 9. Match feedback to the user's relationship with the artifact
**Rule:** the controls you offer must fit what the thing *is* to the user — don't import
patterns from a different context.
**Smell:** a 👍/👎 accuracy rating on content that is the user's *own* private notes (there's
no external party receiving the feedback).
**Before → after:** "Add thumbs-up/down so users can rate page quality." → "Because the wiki
is the student's own notes, there are no accuracy ratings; instead they organize and
prioritize with bookmarks and free-text tags (their own categorization overlaid on the AI's
sections)."

---

## How to use this in a brief
- For each FR and user story touching one of the categories above, name the principle in a
  parenthetical so the *why* survives review (e.g. "(HCD: reversibility — incremental ingest
  modifies pages in place)").
- When a requirement fails a check, **rewrite the requirement** — don't just annotate it.
- In the user journeys, mark the moments these principles pay off as explicit **trust beats**.
