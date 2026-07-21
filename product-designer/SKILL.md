---
name: product-designer
description: >-
    Produce and refine product-design briefs — the document that turns a rough product
    idea into a buildable MVP spec: vision, personas, jobs-to-be-done, goals/non-goals,
    numbered functional requirements, key screens, data model, user stories with
    acceptance criteria, user journeys, success metrics, risks, and milestones, all
    grounded in human-centered-design principles. Use this skill WHENEVER the user wants
    to write, expand, critique, or restructure a product brief, MVP plan, PRD, feature
    spec, or set of user stories — including phrasings like "write a product spec for X",
    "turn this idea into an MVP plan", "draft the requirements", "write user stories with
    acceptance criteria", "design this feature", "what should the MVP scope be", "critique
    this product plan", or "make a PRD". Also use it proactively when a user describes a
    product idea and asks how to scope or structure it. The skill enforces HCD principles
    (visible constraints, reversibility, informative feedback, traceability) and that every
    requirement is testable and tied to a real user need.
---

# Product Designer

This skill is for producing a **product-design brief**: the document that takes a product
idea from a sentence to something a team can build, scope, and validate. It is not a
marketing one-pager and not an engineering design doc — it is the bridge between a user
need and a buildable MVP, written so a designer, an engineer, and a founder all read the
same intent.

A good brief has four properties (this is the bar to hit):

1. **Every requirement traces to a real user need.** A feature exists because a named
   persona has a job to do, not because it's clever or because competitors have it. If you
   can't name whose problem a requirement solves, it doesn't belong in the MVP.
2. **Requirements are testable.** Each functional requirement and user story is concrete
   enough that someone can later say "yes, this is built and correct" or "no, it isn't."
   Vague verbs ("support", "handle", "manage") hide undecided behavior — replace them with
   the observable outcome.
3. **Scope is decided, not implied.** The brief states up front what is locked, what is in
   the MVP, and — explicitly — what is *out*. A non-goals list is as important as the goals;
   it's what stops the MVP from sprawling.
4. **It is human-centered.** The design respects how people actually perceive, act, and
   recover from mistakes. Constraints are visible before errors happen, destructive actions
   are reversible and show their consequences, feedback is informative, and the system's
   structure matches a model the user can hold in their head. See `references/hcd-principles.md`.

## Operating principles (non-negotiable)

- **Start from the user, not the feature.** Before writing a single requirement, establish
  the personas and their jobs-to-be-done. Every later section answers back to these. A
  requirement with no persona behind it is a candidate for the non-goals list.
- **Lock the big decisions first.** Platform, core value proposition, account/data model,
  and the central interaction paradigm are decided up front and stated as "locked product
  decisions." Everything downstream depends on them; leaving them implicit produces a brief
  that quietly contradicts itself.
- **Make requirements observable.** "FR7 — Search" is a title, not a requirement. Spell out
  *what* is searched, *what the user sees*, and *how the control names itself*. The test is:
  could a QA engineer write a pass/fail check from this sentence alone?
- **Write acceptance criteria as conditions, not aspirations.** Each user story carries
  Given/When/Then-style criteria that pin the behavior. "It should be easy to search" is not
  a criterion; "the active scope is shown on the selector and matches are highlighted" is.
- **Name what's out of scope.** Maintain an explicit non-goals list and defer post-MVP ideas
  by name (e.g. "flashcards — post-MVP"). Scope creep enters through silence, not through
  decisions.
- **Apply HCD as a checklist, not a vibe.** For every destructive, irreversible, or
  structure-changing action, walk the HCD checklist (`references/hcd-principles.md`):
  Is the consequence shown before it happens? Is it reversible? Is there immediate feedback?
  Does the control name what it does? A surprising number of requirements change once you do.
- **Earn trust explicitly.** When the product makes claims, generates content, or modifies
  the user's data, build in traceability (citations, "what changed", version history) and
  never fabricate. Call these out as "trust beats" in the journeys.
- **Keep the data model honest.** State the core entities and their invariants (what's
  immutable, what's append-only, how references resolve). A data model with the wrong
  invariants makes whole categories of requirements impossible later.
- **Stay non-prescriptive about the stack.** Suggest a technology direction if useful, but
  label it as a suggestion, not a requirement. The brief specifies *what* and *why*, not *how*.
- **End with validation, not certainty.** A brief is a hypothesis. Close with the open
  questions still to settle and the cheapest test (usually a small usability study on real
  users with real data) that would settle them.

## Process

Work through these in order; later sections feed on earlier ones. Ask the user for what you
genuinely can't infer — but propose a concrete default rather than interrogating them.

1. **Establish context and lock the big decisions.** What exists already, what's being built,
   and the locked choices (platform, core value, accounts/data, interaction model). If these
   aren't decided yet, surface the choice explicitly and recommend one.
2. **Write the vision and personas.** One memorable vision sentence. Two or three named
   personas with their situation and their jobs-to-be-done in their own words.
3. **Set goals and non-goals.** A short numbered goals list (each tied to a persona need) and
   an explicit non-goals list with post-MVP items named.
4. **Enumerate functional requirements (FR1, FR2, …).** One crisp, testable capability each.
   This is the spine of the brief. See *Writing requirements* below.
5. **Sketch the key screens** at wireframe level — what each screen is *for*, not pixels.
6. **Specify any core system behavior** (pipelines, algorithms, state machines) as numbered
   steps, including the incremental/repeat path and the failure path.
7. **Define the information architecture / data model** — entities, fields, and invariants.
8. **List non-functional requirements** — limits, latency, async behavior, privacy,
   reliability, cost. Make limits visible to the user (HCD), not just enforced server-side.
9. **Write user stories grouped into epics**, each with acceptance criteria. See below.
10. **Walk the user journeys** — the happy path, the repeat-use path, and at least one
    unhappy path — marking aha moments and trust beats.
11. **Choose success metrics** — a single activation north-star, the funnel around it, and
    engagement/quality proxies. Each metric must be measurable from product events.
12. **Capture risks & mitigations, milestones, suggested stack, and open questions.**
13. **Recommend the next step** — the validation that de-risks the biggest assumption.

You don't always need every section — a single-feature spec is lighter than a full MVP plan
— but FRs, acceptance criteria, non-goals, and an HCD pass are never optional.

## Writing requirements (the spine)

A functional requirement is a numbered, self-contained, testable capability. Pattern:

> **FR<n> — <Short name>.** <What the user can do>, <what the system does in response>,
> <what the user sees / how the control names itself>, <key edge or constraint>.

Two tests before a requirement is done:
- **The QA test:** could someone write a pass/fail check from this sentence alone?
- **The HCD test:** if it touches a constraint, a destructive action, or generated content,
  does it satisfy the relevant HCD principle (visible limit / shown consequence + undo /
  traceability)? If not, revise the requirement, don't just note it.

Prefer many small sharp FRs over a few broad fuzzy ones. When a requirement grows a list of
caveats, that's usually two or three requirements wearing one number.

## Writing user stories & acceptance criteria

Group stories into epics that mirror the user's mental phases (e.g. Accounts → Manage →
Create → Browse → Trust → Maintain → Ask). Each story:

> **<Epic><n>.** *As a <persona>, I want to <action> so that <benefit>.*
> - <Given a precondition, when an action, then an observable result.>
> - <Another observable condition — including the unhappy case.>

Rules: the benefit clause is mandatory (it's the trace back to the user need); at least one
criterion covers the failure/edge case; criteria describe what's *observable*, never internal
implementation. Where a story embodies an HCD decision, note the principle in one parenthetical
so the *why* survives (e.g. "(HCD: show consequences before a destructive action)").

## References

- `references/brief-template.md` — the full section-by-section skeleton of a product brief,
  with the purpose of each section and what "good" looks like. Start here when writing a new
  brief from scratch.
- `references/hcd-principles.md` — the human-centered-design checklist (visible constraints,
  reversibility, informative feedback, conceptual model, traceability, direct manipulation),
  each with a concrete example of how it changes a requirement. Run every destructive,
  irreversible, or content-generating requirement through this.

When critiquing an *existing* brief rather than writing one, read it against the four
properties and the HCD checklist, and report the specific requirements that fail a test —
with the rewrite, not just the objection.
