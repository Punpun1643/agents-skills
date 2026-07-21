---
name: readme-writer
description: Write, generate, overhaul, or fix a project's README.md (or any "readme", repo front page, or top-level project documentation). Use this skill whenever the user wants to create or improve a README, document a repo, or figure out how to present a codebase to readers — covering libraries and packages, CLI tools, research/ML repos, web apps, services, and developer tooling. Trigger even when the user only says things like "document this project", "write docs for my repo", "make a readme", or points at a codebase and asks how to present it, even if the word "README" never appears.
---

# README Writer

A skill for writing a README that does its real job: getting the right reader to the right action as fast as possible. A README is the front door to a project — most people decide whether to keep going based on the first screen. Treat it as a designed object, not a form to fill in.

## The rule that matters most: never fabricate

The dominant failure mode when an AI writes a README is confident, plausible, wrong content — an `npm install` for a package that isn't published, a badge pointing at CI that doesn't exist, a usage snippet calling functions that aren't exported, a config key that was never read from anywhere. A wrong install command is worse than no install section, because it spends the reader's trust on the very first thing they try.

So: every concrete claim in the README must trace back to something real in the project.

- **Install / run commands**: derive from the actual package manifest and entry points (package.json scripts, pyproject.toml / setup.py, requirements.txt, Cargo.toml, go.mod, Makefile, Dockerfile). Don't assume a package is published to a registry unless you can confirm it.
- **Dependencies / requirements**: read them from the manifest; don't guess versions.
- **Usage examples**: use real, exported, importable names. If you show example output, it should be the output the code would actually produce — not an idealized version.
- **Badges**: include a badge only if the thing it reports on exists (a real CI workflow, a real published version, a real license file). Decorative fake badges erode credibility.
- **Config / env vars**: list only keys the code actually reads.

When you genuinely can't verify something, do not paper over it. Insert a clearly marked placeholder like `<!-- TODO: confirm install command -->` or `[YOUR_REPO_URL]` and call it out to the user, so they fill the gap instead of shipping a confident error.

## Before writing: gather the facts

Prefer reading the repository over interrogating the user. Most of a good README can be reconstructed from the code itself. Pull together:

- **One-sentence identity**: what the project does, in plain language, for whom.
- **Language / runtime / platform** and minimum versions.
- **How it's actually installed and run** — the real commands, from manifests and entry points.
- **Real dependencies** and any non-obvious system requirements.
- **One minimal, real usage example** plus the output it produces.
- **License** (from the LICENSE file) and **project status** (active, experimental, archived).

Ask the user only for what the code can't tell you: the *why this exists* framing, the intended audience, differentiators versus alternatives, and anything about roadmap or status. Those judgments aren't in the source.

## The organizing principle: the involvement gradient

A README is read top-to-bottom by an audience that shrinks and deepens as it goes — many people skim the first screen, fewer install it, fewer still contribute. Order the content to match that funnel, so the most-skimmed information sits highest and the deepest material lowest:

1. **Identity** — name, one-line description, what + why. (Everyone reads this.)
2. **Proof** — a screenshot, GIF, or short demo that shows it working. A 5-second GIF beats three paragraphs.
3. **Quickstart** — install + the smallest real example that does something. Get them to a win fast.
4. **Depth** — fuller usage, configuration, API / reference, options.
5. **Contribution / internals** — dev environment setup, running tests, architecture notes.
6. **Meta** — license, acknowledgements, citation.

The most common structural mistake is burying "what is this even" under a wall of badges and a table of contents. Lead with meaning.

## Default structure

Use this as the baseline and cut sections that don't apply — a short README beats a padded one:

```markdown
# Project Name

<!-- status callout at the VERY top ONLY if development has slowed/stopped or maintainers are wanted -->

One sentence on what it does and who it's for.

<!-- badges: only real ones — version, build, license -->

![demo](path-or-link)   <!-- screenshot or GIF if the project has a visible/runnable output -->

## Features            <!-- optional: a tight bulleted list of what it actually does -->

## Install
    exact, verified command(s)

## Usage
    smallest real example
    + the output it produces

## Configuration       <!-- optional: real env vars / options, in a table -->

## Support             <!-- optional: where to get help — issue tracker, chat, email -->

## Roadmap             <!-- optional: planned releases / direction, if any exist -->

## Contributing        <!-- optional: dev setup, tests; or link to CONTRIBUTING.md -->

## Authors & acknowledgment  <!-- optional: credits for contributors / prior art -->

## License

State the license in one line; full text lives in LICENSE.
```

Keep headings consistent and don't skip levels (`##` → `####` reads as a mistake). Put spacing between sections so it isn't a wall of text.

## Variant adjustments

Start from the default, then layer on the variant that fits:

**Library / package** — Lead with install-from-registry and a copy-paste import example. Document the public API surface (or link to generated docs). A "why this over alternatives" line earns its place here. Show the smallest meaningful call, not a kitchen-sink example.

**CLI tool** — A terminal GIF is worth more than prose; show the tool actually running. Include the canonical invocation, the most-used flags, and example output. Note install per platform if it differs (Homebrew / cargo / npx / binary download).

**Research / ML repo** — Reproducibility is the whole game. Include: a one-command environment setup (exact versions; ideally a lockfile or `environment.yml`), how to get the data (with licensing / access notes), seeds or determinism caveats, where the weights / checkpoints live (e.g. a model hub link), and an expected-results table so readers can confirm they reproduced it. Add a citation block (BibTeX) if there's a paper or the work is meant to be cited. State clearly what's released versus withheld.

**Web app / service** — Cover local dev setup, required environment variables (in a table, names only — never real secrets), how to run it (dev + build), and a brief architecture or "how it works" note. A deployment section or link helps. If there's a live demo, link it near the top.

## Element palette

Distilled from surveying the most-admired READMEs in the wild (the awesome-readme collection of ~85 hand-picked examples). Treat this as a palette, not a checklist: pull the elements that fit the project's type and maturity, place them according to the involvement gradient above, and — per the rule at the top — never fake any of them (no badge without a real service behind it, no contributor wall on a one-person repo).

**Table stakes** — almost every great README has these:

- **One-line description** of what it does and who it's for, directly under the title. The best are legible to someone brand new to the product.
- **Visual identity** — a logo or banner at the very top. A small logo for libraries/tools; a hero banner (sometimes an animated one) for larger projects.
- **A demo** — the single highest-leverage element. If the project produces any visible or runnable output, show it: an animated GIF or screenshot near the top beats paragraphs of prose. For CLIs/terminal tools, record the terminal (tools: `vhs`, `terminalizer`, `ScreenToGif`, `asciinema`).
- **Meaningful badges** — version, build/CI, coverage, downloads, license. Include only ones backed by something real, and only those that inform the reader.
- **Install** — copy-pasteable, step-by-step, verified against the real manifest.
- **Usage** — the smallest real example (ideally with its output), plus a fuller examples section.
- **Feature list** — a tight bulleted inventory of what it actually does.
- **License** — one line; full text in LICENSE.

**High-leverage additions** — common in the best, include when they fit:

- **Quickstart** — the fastest path from zero to a working result, near the top.
- **A diagram** — for anything non-trivial (infra, ML, frameworks), one picture conveying "what this is / how it works at a glance" carries enormous weight. Mermaid renders natively on GitHub; deeper architecture notes can live in a dedicated `ARCHITECTURE.md`.
- **"Why this exists" / motivation** — a short section on the problem and how this differs from alternatives. Recurs constantly in well-loved projects ("why another X", "motivation to create").
- **Further-reading links** — a cluster pointing to the website, full docs, community (Discord/Slack), and live demo; often placed near the top as quick links.
- **Live demo / playground** — a link to try it without installing (hosted demo, Storybook, online sandbox).
- **Support** — where to go for help: issue tracker, chat room (Discord/Slack), mailing list, or email. Point people to one obvious place rather than making them guess.
- **Roadmap** — planned releases or direction, when concrete plans exist. Skip it rather than inventing aspirational filler.
- **Contribution** — dev setup, running tests, how to contribute; or a link to `CONTRIBUTING.md`. Make the get-started steps explicit (setup script, env vars, lint/test commands) — future-you benefits too.
- **FAQ** — for projects that field the same questions repeatedly.
- **Credits / acknowledgements / prior art** — attribution plus a nod to alternatives.

**Status callout** — for maintenance reality, placed at the very top:

- **Project status** — if development has slowed or stopped, say so at the *top* of the README (a maintainer may fork or step in). Likewise flag experimental / pre-1.0 / archived status, or an explicit "seeking maintainers" request. This is one of the few things that belongs above identity, because it changes whether the reader should invest at all.

**Navigation aids** — once the README is long enough to need them:

- **Table of contents** — when the page genuinely warrants it (and not before).
- **Collapsible sections** — wrap long blocks (extended config, verbose examples) in `<details>` so the page stays scannable.
- **Back-to-top links** — small anchors after long sections.

**Polish / social proof** — for established or community projects; skip on a brand-new repo:

- Contributor avatars, stargazers, and star-history charts.
- Tasteful, *consistent* section emojis or custom icons — an accepted convention when applied uniformly; noise when scattered.
- Multi-language switcher / i18n, or per-language code docs for polyglot libraries.
- Versioning or status callout (e.g. distinguishing a current v2 from a v1 maintenance line).
- Folder-structure / file inventory — especially useful in research and data repos where readers navigate many files.

The through-line: scale the README to the project. A solo utility wants identity + demo + install + usage and little else; a flagship framework earns the diagrams, philosophy, contributor walls, and i18n. Adding elements a project hasn't earned reads as cargo-culting, not care.

## Quality bar

A README passes when:

- A newcomer learns what the project is and whether it's for them within the first screen.
- Every command shown actually works as written.
- There is at least one real, runnable usage example.
- If the project has any visible or runnable output, there's a demo (GIF or screenshot) near the top.
- Nothing decorative is faked (badges, output, stats).
- Headings are consistent and the document scans without reading every word.
- Anything unverifiable is a visible TODO, not a confident guess.

## Anti-patterns to avoid

- No description, or a description that doesn't say what the thing *does*.
- A wall of badges above the fold, before the reader knows what they're looking at.
- Install or usage steps that reference scripts, packages, or functions that don't exist.
- Walls of unbroken text; no headings, no spacing.
- An overly casual throwaway tone ("just something I hacked together lol") that undersells real work.
- Padding sections for the sake of completeness — length is not a proxy for quality.
- Cargo-culting elements the project hasn't earned — contributor walls, star-history charts, or i18n switchers on a brand-new solo repo.
- A table of contents on a README short enough not to need one.

## Tone and craft

Favor precision and restraint over decoration. Active voice; concrete over vague ("processes 10k rows/sec" beats "blazingly fast"); every section earning its place. Think of the README as having affordances — the reader should be able to tell at a glance what they can *do* here: try it, install it, read more, contribute. Decoration that doesn't help the reader act is noise. Match the project's seriousness: a research artifact and a weekend toy want different registers, but both want clarity.

## Worked examples

For two complete, filled-in READMEs to use as models — one library, one research/ML repo — read `references/examples.md`.

For the canonical section-by-section checklist (Name, Description, Badges, Visuals, Installation, Usage, Support, Roadmap, Contributing, Authors & acknowledgment, License, Project status) with the purpose and gotchas of each, read `references/section-checklist.md`.
