---
name: dev-guide
description: >-
    Create and maintain a repository's developer guide — the document that explains
    the system's architecture, components, data flow, and design decisions to new
    contributors. Use this skill WHENEVER the user wants to write, update, regenerate,
    fact-check, or extend developer/architecture documentation, including phrasings
    like "update the dev guide", "the architecture doc is out of date", "document this
    module", "add X to the developer guide", "the DG", "regenerate the architecture
    docs", or "make a developer guide for this repo". Also use it proactively after
    significant structural code changes (new / removed / renamed components, reworked
    data flow) when the user mentions docs. The skill enforces that every description
    is grounded in the actual code and that diagrams use the correct type for what
    they illustrate.
---

# Developer Guide

This skill is for producing and maintaining a **developer guide**: the document a new
contributor reads to understand how the system is built well enough to change it. It is
not user-facing documentation and not an API reference dump — it is the mental model of
the codebase.

A good developer guide has three properties (this is the bar to hit):

1. **It is accurate.** The architecture and component descriptions reflect how the code
   _actually_ works, not how it was once intended to work. An inaccurate guide is worse
   than no guide because it confidently misleads.
2. **Every component is explained by its responsibility**, not just named. The reader
   learns _what each part is for_ and _how the parts connect_, in plain language.
3. **Flows are shown with the right kind of diagram.** Structure, sequence, and data
   pipelines each call for a different diagram type, and the guide uses the correct one.

A good starting point is to start with a top-level architecture
diagram, then one section per major component, each stating a single responsibility,
listing its parts as one-line descriptions linked to source, and tracing processes as
numbered steps.

## Operating principles (non-negotiable)

- **Ground everything in code you have actually read.** Never describe a component from
  its name, from a typical pattern, or from memory of how similar systems work. Open the
  file and confirm. This is the whole value of the guide.
- **Document responsibility, not existence.** "`AuthParser` parses auth config" is filler.
  "`AuthParser` turns the raw `auth.yaml` into a validated `AuthConfig`, rejecting unknown
  providers so the rest of the system can assume the config is well-formed" is useful.
- **Link every component to its source.** A name without a path can't be verified or
  navigated. Use relative repo paths or source-host URLs, matching whatever the repo
  already does.
- **Trace real flows.** When you describe how a request or a piece of data moves through
  the system, follow the actual call chain in the code — don't reconstruct a plausible one.
- **One diagram, one idea, right type.** Pick the diagram type that matches the question
  the reader is asking (see _Choosing a diagram_). Don't cram a sequence into a box-and-arrow
  graph or vice versa.
- **Keep it in sync.** When code changes, the prose, the source links, the numbered flows,
  the diagrams, and the cross-references all have to move together. Stale fragments are how
  guides rot.
- **Write for someone who needs to change the code**, not someone evaluating whether to use
  it. Explain the _why_ behind non-obvious design decisions; that's what a contributor can't
  recover from reading the code alone.

## Step 0 — Determine the mode and locate the guide

Before doing anything, work out which of three situations you're in, because the work differs:

- **Create** — no developer guide exists yet. You'll survey the codebase and build the whole
  structure. See `references/structure.md` for the template and section-by-section guidance.
- **Update** — a guide exists and the code has moved on. You'll detect drift and reconcile.
  This is the common case for maintenance; see _Maintaining an existing guide_ below.
- **Targeted edit** — the user points at one component or section ("document the new caching
  layer", "the auth section is wrong"). Scope tightly to that, but still update any diagrams
  and cross-references the change touches.

Locate the guide. Common locations: `docs/developer-guide.md`, `docs/dg/`, `DEVELOPER.md`,
`docs/architecture.md`, or a wiki. If unsure, search the repo for an architecture doc before
assuming none exists. If creating one and the repo has a `docs/` convention, follow it; a
single file is fine for small/medium projects, a `docs/dg/` folder split by topic suits large
ones (the structure reference explains when to split).

Also check what the repo already uses for diagrams (Mermaid, PlantUML, committed images). Match
it. For new diagrams with no existing convention, default to **Mermaid** — it lives in the
markdown as text, diffs cleanly in pull requests, renders on most hosts, and can be edited in
the same pass as the prose, so it stays in sync. Exported images silently go stale.

## The grounding discipline

This is the step people skip and it is the most important one. Before writing or revising any
description:

1. **Map the repository.** Get the directory tree, identify the entry point(s) (`main`, server
   bootstrap, CLI handler, `index.*`), and read the build/config manifest (`package.json`,
   `pom.xml`, `pyproject.toml`, `go.mod`, etc.) to learn the real module boundaries and
   dependencies.
2. **For each component you'll document, open its source and read enough to state its real
   responsibility** in one sentence. If you can't write that sentence from what you read, you
   haven't read enough yet.
3. **Trace flows by following actual calls.** To describe "what happens when a report is
   generated", start at the entry function and follow it through — note the order of calls and
   the data type produced at each hop.
4. **Verify as you go.** Every source path you cite should point at a file that exists. Every
   component you name should be a real construct in the code.

If the codebase is large, it's fine to document the significant components and explicitly note
the guide's scope rather than fabricate coverage of everything.

## Let the project shape the emphasis

Once you've mapped the repo, classify what kind of system it is and let that decide which diagrams
and sections carry the weight. The component pattern and the quality bar are identical for every
project; what changes is _where the explanatory effort goes_. This applies in both create and update
modes — when adding or reworking a section, reach first for the diagram type that fits the project's
shape.

| Project type             | Lead with                                    | Favor these diagrams                                                     | Sections that matter most                                      |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Library / SDK            | the public API surface and core abstractions | `classDiagram` — the types _are_ the architecture                        | data model / core types; design decisions                      |
| Service / backend        | the request lifecycle and the layering       | `sequenceDiagram` for request flow, `erDiagram` for schema               | cross-cutting concerns (auth, errors, concurrency); data model |
| CLI / batch tool         | the processing pipeline, entry to output     | `flowchart LR` pipeline                                                  | component sections in pipeline order; configuration            |
| Frontend app             | the component tree and data-loading flow     | component tree (`flowchart TD`); reuse the framework's lifecycle diagram | state management / data flow                                   |
| Monorepo / multi-service | how the services interact                    | top-level `flowchart TD` of services, then per-service diagrams          | one page per service (split into `docs/dg/`)                   |

This is emphasis, not exclusion: a backend still gets a top-level component diagram, and a library
still traces flows where real sequences exist. For a mixed project — say a service that ships a CLI
and a frontend — apply the relevant lens to each part rather than forcing one over the whole. The
fuller per-type treatment (what to document for each) is in `references/structure.md` under
"Adapting to project type".

## Producing the guide structure

The full template, section ordering, and a worked example live in **`references/structure.md`** —
read it before laying out a new guide or when deciding where a new section belongs. In short, a
guide flows top-down:

- a one-paragraph overview of what the system does and for whom;
- an **architecture overview** — one diagram of the major components plus a paragraph naming them
  and how they fit together;
- **one section per major component** (the pattern below);
- a **data model / shared structures** section if the system has core types passed between
  components (document each: what it holds, who uses it, for what);
- **cross-cutting concerns** (config, logging, error handling, concurrency, auth) where relevant;
- optionally, **key design decisions and their rationale**, and a short **conventions / gotchas**
  section.

Match the repo's existing heading style and tone if a partial guide already exists.

## Documenting a component (the core pattern)

Each component section states a single responsibility, lists its parts as one-liners linked to
source, traces its process as numbered steps when there is one, and names its connections to other
components. The shape:

```markdown
## ReportGenerator

`ReportGenerator` ([src/report/ReportGenerator.ext](path)) is responsible for turning the
analyzed repository data into the final JSON files the frontend consumes.

It coordinates these parts:

- `CommitsReporter` ([path]): analyzes commit history into a `CommitSummary`.
- `AuthorshipReporter` ([path]): traces per-line authorship into an `AuthorshipSummary`.
- `TemplateCopier` ([path]): copies the static report shell into the output directory.

How it works:

1. clones the target repositories via `GitClone`, using a thread pool (default: 4 threads).
2. runs `CommitsReporter` and `AuthorshipReporter` per repository to produce the two summaries.
3. serializes both summaries into the `*.json` files under the output directory.

`ReportGenerator` is invoked by the CLI entry point once `ConfigParser` has produced a valid
`RepoConfiguration`, and it depends on `System/CommandRunner` to execute the underlying git
commands.
```

Notes on the pattern:

- **The responsibility sentence is mandatory and comes first.** It's the one thing the reader
  must take away.
- **One line per part**, each describing what it does and (where useful) what type it produces.
  Resist the urge to expand into paragraphs here — depth goes into the numbered flow or a
  sub-section.
- **Use a numbered flow only when there is an actual sequence.** A bag of unrelated helpers
  (e.g. a `util` package) is better as a bulleted list, not fake steps.
- **End with connections.** "Used by X to do Y; depends on Z for W." This is what lets a reader
  navigate outward from any component, and it's the first thing that goes stale on a refactor.
- Add a diagram to the section only when the interaction is non-trivial enough that prose alone
  is hard to follow.

## Choosing a diagram

Pick the type by the question the reader is asking. Full Mermaid examples, per-type "use when /
avoid when", and hygiene rules are in **`references/diagrams.md`** — read it before authoring or
editing any diagram. Quick selector:

| The reader wants to understand…                                                    | Use                        | Mermaid           |
| ---------------------------------------------------------------------------------- | -------------------------- | ----------------- |
| How the major components fit together (the system)                                 | Component / architecture   | `flowchart TD`    |
| The ordered interaction between parts over time (a request lifecycle, a call path) | Sequence                   | `sequenceDiagram` |
| How data is transformed through stages (a pipeline)                                | Data-flow pipeline         | `flowchart LR`    |
| The states something moves through                                                 | State machine              | `stateDiagram-v2` |
| How key types/classes relate                                                       | Class / type relationships | `classDiagram`    |
| The database / entity schema                                                       | Entity-relationship        | `erDiagram`       |

The two most common mistakes: using a static box-and-arrow graph to describe something that is
fundamentally a _sequence in time_ (use `sequenceDiagram`), and drawing a 25-node diagram of the
entire system (split it; one diagram should hold ~5–9 nodes and convey one idea).

## Maintaining an existing guide

This is the heart of ongoing use. A diff tells you which lines changed; it does **not** tell you
what a component now _does_ as a whole — so reconcile against the current code, never from the diff
alone.

1. **Find what moved.** If the repo uses git, find when the guide was last meaningfully updated and
   review what changed in the code since (`git log`, changed files, renamed/added/deleted modules).
   This focuses the effort; it does not replace reading.
2. **Reconcile component by component.** For each documented component, confirm it still exists and
   that its responsibility sentence still matches the code (open the source). Three drift cases to
   hunt for:
    - **Documented but gone / renamed** — the code construct no longer exists. Remove or rename it,
      and fix every cross-reference and diagram node that pointed at it.
    - **Changed behavior** — the component still exists but does something different now. Rewrite the
      responsibility sentence, the part list, and the numbered flow to match.
    - **Significant but undocumented** — a real component the guide never covered. Decide whether it
      warrants a section (does a contributor need to understand it to make changes?) and add one if so.
3. **Re-sync diagrams.** If components were added, removed, or re-wired, update the architecture
   diagram and any flow diagram the change touches. A diagram that contradicts the current code is a
   bug.
4. **Fix the source links.** Renamed or moved files break links; confirm each cited path still
   resolves.
5. **Preserve human-authored rationale.** Design-decision notes and "why we did it this way" prose a
   person wrote are high-value and not recoverable from code. Update around them; don't flatten them.

Optionally, when creating or substantially updating a guide, add a short "How this guide is
maintained" note (where the guide lives, what diagram tool it uses, the conventions above) so the
next maintenance pass — by a person or by you — starts grounded.

## Quality checklist

Before declaring the guide done or updated, verify:

- [ ] Every component described maps to a real construct you opened and read.
- [ ] Every component section leads with a one-sentence responsibility.
- [ ] Every source link resolves to an existing path.
- [ ] Every diagram is the correct type for what it shows, holds one idea, and matches current code.
- [ ] Every documented flow traces the actual call chain.
- [ ] No documented-but-deleted components remain; no architecturally significant component is
      silently missing.
- [ ] Cross-references ("used by", "depends on") are consistent in both directions.
- [ ] A new contributor could read it and know where in the code to make a given change.
