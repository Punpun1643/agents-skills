# claude-skills

A personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) Agent Skills — reusable, model-invoked playbooks that teach Claude how to perform specific documentation and workflow tasks to a consistent standard.

Each skill is a directory containing a `SKILL.md` (instructions + a description that tells Claude when to trigger it) and, optionally, a `references/` folder with deeper material Claude reads on demand.

## Skills

Each skill triggers automatically when a request matches its description, or explicitly via its slash command (e.g. `/git-commit`). See [Usage](#usage) for details.

| Skill | What it does | Credit |
|-------|--------------|--------|
| [`dev-guide`](dev-guide/SKILL.md) | Create and maintain a repo's developer/architecture guide, grounded in real code with the right diagram type for each idea. | — |
| [`excalidraw`](excalidraw/SKILL.md) | Generate architecture diagrams as `.excalidraw` files from codebase analysis, with optional PNG/SVG export. | Adapted from [ooiyeefei/ccc](https://github.com/ooiyeefei/ccc/tree/main/skills/excalidraw) |
| [`git-commit`](git-commit/SKILL.md) | Write Conventional Commits messages and split a working tree into clean, independent commits. | — |
| [`product-designer`](product-designer/SKILL.md) | Turn a rough product idea into a buildable MVP brief — requirements, user stories, data model, metrics — via human-centered design. | — |
| [`readme-writer`](readme-writer/SKILL.md) | Write, overhaul, or fix a project's README by the reader-involvement gradient, never fabricating commands or badges. | — |

### `dev-guide`

Create and maintain a repository's developer/architecture guide. [`SKILL.md`](dev-guide/SKILL.md)

- Grounds every description in the actual code — no invented components or flows.
- Picks the correct diagram type for what each diagram shows.
- Enforces tables (not inline runs) for field/attribute/column lists.
- Reference material: component [`structure`](dev-guide/references/structure.md), [`diagrams`](dev-guide/references/diagrams.md).

*Invoke:* `/dev-guide`, or "update the dev guide", "document this module".

### `excalidraw`

Generate architecture diagrams as `.excalidraw` files from codebase analysis. [`SKILL.md`](excalidraw/SKILL.md)

- Produces editable `.excalidraw` JSON, with optional PNG/SVG export via Playwright.
- Cloud-provider color palettes (AWS, Azure, GCP, Kubernetes).
- Handles arrow routing, bindings, and staggering to avoid overlap.
- Reference material for [JSON format](excalidraw/references/json-format.md), [arrows](excalidraw/references/arrows.md), [colors](excalidraw/references/colors.md), [examples](excalidraw/references/examples.md), [validation](excalidraw/references/validation.md), and [export](excalidraw/references/export.md).

*Invoke:* `/excalidraw`, or "create an architecture diagram", "export this to PNG".

### `git-commit`

Write Conventional Commits messages and structure a working tree into clean commits. [`SKILL.md`](git-commit/SKILL.md)

![Real `git log` from this repo after running the git-commit skill](assets/git-commit.png)

*A real capture of this repository's history — the commits above were written by this skill.*

- Reads the actual diff before composing — message reflects the change, not the prompt.
- Splits a mixed working tree into the smallest set of independent, self-contained commits.
- Applies the full type/scope/breaking-change convention and its semver mapping.

*Invoke:* `/git-commit`, or "commit this", "write a commit message".

### `product-designer`

Turn a rough product idea into a buildable MVP brief. [`SKILL.md`](product-designer/SKILL.md)

- Produces vision, personas, jobs-to-be-done, numbered functional requirements, data model, user stories with acceptance criteria, metrics, risks, and milestones.
- Enforces human-centered-design principles and testable, traceable requirements.
- Reference material: [`brief-template`](product-designer/references/brief-template.md), [`hcd-principles`](product-designer/references/hcd-principles.md).

*Invoke:* `/product-designer`, or "write a PRD", "turn this idea into an MVP plan".

### `readme-writer`

Write, overhaul, or fix a project's README. [`SKILL.md`](readme-writer/SKILL.md)

- Orders content by the reader-involvement gradient (identity → proof → quickstart → depth).
- Never fabricates commands, badges, or output — unverifiable claims become visible TODOs.
- Variant guidance for libraries, CLIs, research/ML repos, and web apps/services.
- Reference material: [`examples`](readme-writer/references/examples.md), [`section-checklist`](readme-writer/references/section-checklist.md).

*Invoke:* `/readme-writer`, or "make a readme", "document this project".

## Install

These are [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills). Claude Code discovers a skill when its directory lives under a skills folder it scans — `~/.claude/skills/` for personal skills, or `.claude/skills/` inside a project.

Clone the repo, then link the skills you want into your personal skills directory:

```sh
git clone https://github.com/Punpun1643/claude-skills.git
cd claude-skills
mkdir -p ~/.claude/skills
```

### Install one skill

```sh
ln -s "$PWD/readme-writer" ~/.claude/skills/readme-writer
```

### Install all skills

```sh
for d in dev-guide excalidraw git-commit product-designer readme-writer; do
  ln -s "$PWD/$d" ~/.claude/skills/"$d"
done
```

Symlinking keeps the installed skills tracking your local clone; copy the directories instead (`cp -r`) if you'd rather pin a fixed version.

## Usage

Skills are invoked two ways:

- **Automatically** — Claude reads each skill's `description` and triggers the matching one when your request fits. Ask "write a commit message for this" and `git-commit` engages; "make a readme for this repo" pulls in `readme-writer`.
- **Explicitly** — call it as a slash command, e.g. `/readme-writer` or `/git-commit`.

## Repository structure

```
.
├── dev-guide/          # skill: developer/architecture guides
│   └── references/
├── excalidraw/         # skill: excalidraw architecture diagrams
│   └── references/
├── git-commit/         # skill: conventional commits
├── product-designer/   # skill: product-design briefs
│   └── references/
└── readme-writer/      # skill: READMEs
    └── references/
```

Each `SKILL.md` opens with YAML frontmatter (`name`, `description`) followed by the instructions Claude follows. `references/` files are loaded only when a skill needs them, keeping the main instructions lean.

## License

Released under the [MIT License](LICENSE).
