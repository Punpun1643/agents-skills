# Product brief — section template

A reusable skeleton for a product-design brief. Each section lists its **purpose** (the
question it answers) and what **good** looks like. Drop sections that don't apply to a
small single-feature spec, but never drop functional requirements, non-goals, acceptance
criteria, or the HCD pass.

Open with a one-line status (`draft for review`) so readers know how settled it is.

---

## 1. Context & locked decisions
**Purpose:** what already exists, what's being built, and the decisions everything else
depends on. **Good:** the "locked product decisions" are stated as a short bullet list —
platform, core value proposition, account/data model, and the central interaction
paradigm — so no later section can quietly contradict them.

## 2. Vision & target users
**Purpose:** who this is for and the future it creates. **Good:** one memorable vision
sentence; two or three *named* personas with their concrete situation; jobs-to-be-done
phrased in the user's own voice ("When I…, I want to…, so I can…"). Generic "users" is a
smell — name them.

## 3. Goals & non-goals
**Purpose:** the bounded set of outcomes the MVP commits to. **Good:** a short numbered
goals list, each tracing to a persona need; an explicit **non-goals** list with post-MVP
items named ("flashcards — post-MVP"). The non-goals list is what stops scope creep.

## 4. Functional requirements (FR1, FR2, …)
**Purpose:** the testable capabilities — the spine. **Good:** each FR is one numbered,
self-contained, observable capability (what the user does → what the system does → what
the user sees). Many sharp FRs beat a few fuzzy ones. Run each through the QA test and the
HCD test.

## 5. Key screens (wireframe-level)
**Purpose:** the surfaces the user moves through. **Good:** each screen named with its
*job* ("Empty wiki — 'Upload your first PDF' drop zone"), not pixel layout. Note key
toggles/modes and where global actions live.

## 6. Core system behavior (pipelines / state)
**Purpose:** the non-trivial logic behind the screens — ingestion pipelines, matching,
state machines. **Good:** numbered steps for the primary path; an explicit description of
the *repeat/incremental* path (what reconciles against existing data); and the *failure*
path (what happens to a bad input, surfaced not silently dropped).

## 7. Information architecture / data model
**Purpose:** the entities and their invariants. **Good:** each entity with its key fields;
invariants called out explicitly (what's immutable, what's append-only, how references
resolve — by stable id/name, not by path). Wrong invariants here make later requirements
impossible.

## 8. Non-functional requirements
**Purpose:** the qualities, limits, and constraints. **Good:** concrete limits (size, count,
latency targets); async/background behavior; privacy and data-handling; reliability
(idempotent, retry-safe, never-silently-dropped); cost control. Critically: limits the user
hits must be **visible up front** (HCD), not enforced only as after-the-fact errors.

## 9. User stories (epics + acceptance criteria)
**Purpose:** the requirements re-expressed from the user's seat, with pass/fail conditions.
**Good:** stories grouped into epics that follow the user's phases; each story has the
mandatory *so that* benefit, Given/When/Then criteria, at least one edge/failure criterion,
and a parenthetical naming any HCD principle it embodies.

## 10. User journeys
**Purpose:** the end-to-end narrative arcs. **Good:** at least three — first-time use,
repeat use, and an unhappy path — each as numbered steps annotated with **aha moments**
(where value lands) and **trust beats** (where the product proves it's trustworthy).

## 11. Success metrics
**Purpose:** how you'll know it works. **Good:** one **activation north-star** (the
single event that means a user got value), the funnel leading to it, retention, and
engagement/quality proxies. Every metric must be derivable from product events.

## 12. Risks & mitigations
**Purpose:** what could break the value, and the plan. **Good:** each risk paired with a
concrete mitigation already reflected in the requirements (not a vague "we'll be careful").

## 13. Milestones
**Purpose:** the build order. **Good:** M0…Mn, each a coherent, demoable slice
(M0 skeleton → first end-to-end value → incremental/maintain → trust → advanced). Post-MVP
items listed separately.

## 14. Suggested stack (non-prescriptive)
**Purpose:** a starting technical direction. **Good:** explicitly labeled a suggestion, not
a requirement — the brief owns *what* and *why*, the team owns *how*.

## 15. Open questions
**Purpose:** the decisions still genuinely undecided. **Good:** crisp either/or questions,
with resolved ones struck through and the resolution noted, so the brief shows its own
history of decisions.

## 16. Recommended next step
**Purpose:** the action that de-risks the biggest assumption. **Good:** usually the cheapest
real test — a small usability study with target users on *their own* data, walking the key
journeys, measuring the activation funnel — to settle the open questions before committing
to a build.
