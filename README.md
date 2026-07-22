# claude-skills

A personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) Agent Skills — reusable, model-invoked playbooks that teach Claude how to perform specific documentation and workflow tasks to a consistent standard.

## Skills

Each skill triggers automatically when a request matches its description, or explicitly via its slash command (e.g. `/git-commit`). See [Usage](#usage) for details.

| Skill                                           | What it does                                                                                                                        | Credit                                                                                                             |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [`dev-guide`](dev-guide/SKILL.md)               | Create and maintain a repo's developer/architecture guide, grounded in real code with the right diagram type for each idea.         | —                                                                                                                  |
| [`excalidraw`](excalidraw/SKILL.md)             | Generate architecture diagrams as `.excalidraw` files from codebase analysis, with optional PNG/SVG export.                         | Adapted from [ooiyeefei/ccc](https://github.com/ooiyeefei/ccc/tree/main/skills/excalidraw)                         |
| [`git-commit`](git-commit/SKILL.md)             | Write commit messages in the Conventional Commits style and split a working tree into clean, independent commits.                   | Based on [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)                                    |
| [`product-designer`](product-designer/SKILL.md) | Turn a rough product idea into a buildable MVP brief — requirements, user stories, data model, metrics — via human-centered design. | HCD principles from [_The Design of Everyday Things_](https://en.wikipedia.org/wiki/The_Design_of_Everyday_Things) |
| [`readme-writer`](readme-writer/SKILL.md)       | Write, overhaul, or fix a project's README by the reader-involvement gradient, never fabricating commands or badges.                | Based on [makeareadme.com](https://www.makeareadme.com)                                                            |

---

### [dev-guide](dev-guide/)

Create and maintain a repository's developer/architecture guide.

- Grounds every description in the actual code.
- Picks the correct diagram type for what each diagram shows.
- Enforces tables for field/attribute/column lists.
- Reference material: component [`structure`](dev-guide/references/structure.md), [`diagrams`](dev-guide/references/diagrams.md).

_Invoke:_ `/dev-guide`, or "update the dev guide", "document this module".

---

### [excalidraw](excalidraw/)

Generate architecture diagrams as `.excalidraw` files from codebase analysis.

- Produces editable `.excalidraw` JSON, with optional PNG/SVG export via Playwright.
- Cloud-provider color palettes (AWS, Azure, GCP, Kubernetes).
- Handles arrow routing, bindings, and staggering to avoid overlap.
- Reference material for [JSON format](excalidraw/references/json-format.md), [arrows](excalidraw/references/arrows.md), [colors](excalidraw/references/colors.md), [examples](excalidraw/references/examples.md), [validation](excalidraw/references/validation.md), and [export](excalidraw/references/export.md).

_Invoke:_ `/excalidraw`, or "create an architecture diagram", "export this to PNG".

---

### [git-commit](git-commit/)

Write Conventional Commits messages and structure a working tree into clean commits.

![Real `git log` from this repo after running the git-commit skill](assets/git-commit.png)

_A real capture of this repository's history — the commits above were written by this skill._

- Reads the actual diff before composing — message reflects the change, not the prompt.
- Splits a mixed working tree into the smallest set of independent, self-contained commits.
- Applies the full type/scope/breaking-change convention and its semver mapping.

_Invoke:_ `/git-commit`, or "commit this", "write a commit message".

---

### [product-designer](product-designer/)

Turn a rough product idea into a buildable MVP brief.

- Produces vision, personas, jobs-to-be-done, numbered functional requirements, data model, user stories with acceptance criteria, metrics, risks, and milestones.
- Enforces human-centered-design principles and testable, traceable requirements.
- Reference material: [`brief-template`](product-designer/references/brief-template.md), [`hcd-principles`](product-designer/references/hcd-principles.md).

_Invoke:_ `/product-designer`, or "write a PRD", "turn this idea into an MVP plan".

---

### [readme-writer](readme-writer/)

Write, overhaul, or fix a project's README.

- Orders content by the reader-involvement gradient (identity → proof → quickstart → depth).
- Never fabricates commands, badges, or output — unverifiable claims become visible TODOs.
- Variant guidance for libraries, CLIs, research/ML repos, and web apps/services.
- Reference material: [`examples`](readme-writer/references/examples.md), [`section-checklist`](readme-writer/references/section-checklist.md).

_Invoke:_ `/readme-writer`, or "make a readme", "document this project".

---

## Install

These are [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills). Claude Code discovers a skill when its directory lives under a skills folder it scans — `~/.claude/skills/` for personal skills, or `.claude/skills/` inside a project.

Clone the repo and create your personal skills directory:

```sh
git clone https://github.com/Punpun1643/claude-skills.git
cd claude-skills
mkdir -p ~/.claude/skills
```

Then pick one of the two install methods below.

### Option 1: Symlink (tracks your clone)

The installed skill points back at your clone, so a `git pull` updates it automatically. Best if you want your installed skills to always stay up to date.

Install one skill:

```sh
ln -s "$PWD/readme-writer" ~/.claude/skills/readme-writer
```

Install all skills:

```sh
for d in dev-guide excalidraw git-commit product-designer readme-writer; do
  ln -s "$PWD/$d" ~/.claude/skills/"$d"
done
```

### Option 2: Copy (pins a fixed version)

The installed skill is an independent copy frozen at the current state (updating the clone won't change it until you copy again). Best if you want a stable snapshot.

Install one skill:

```sh
cp -r "$PWD/readme-writer" ~/.claude/skills/readme-writer
```

Install all skills:

```sh
for d in dev-guide excalidraw git-commit product-designer readme-writer; do
  cp -r "$PWD/$d" ~/.claude/skills/"$d"
done
```

## Usage

Skills are invoked two ways:

- **Automatically** — Claude reads each skill's `description` and triggers the matching one when your request fits. Ask "write a commit message for this" and `git-commit` engages; "make a readme for this repo" pulls in `readme-writer`.
- **Explicitly** — call it as a slash command, e.g. `/readme-writer` or `/git-commit`.

## License

Released under the [MIT License](LICENSE).
