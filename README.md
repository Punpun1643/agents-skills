# claude-skills

A personal collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) Agent Skills — reusable, model-invoked playbooks that teach Claude how to perform specific documentation and workflow tasks to a consistent standard.

Each skill is a directory containing a `SKILL.md` (instructions + a description that tells Claude when to trigger it) and, optionally, a `references/` folder with deeper material Claude reads on demand.

## Skills

| Skill | What it does |
|-------|--------------|
| [`dev-guide`](dev-guide/SKILL.md) | Create and maintain a repository's developer/architecture guide, grounded in the actual code, with the correct diagram type for each idea. |
| [`excalidraw`](excalidraw/SKILL.md) | Generate architecture diagrams as `.excalidraw` files from codebase analysis, with optional PNG/SVG export. |
| [`git-commit`](git-commit/SKILL.md) | Write Conventional Commits messages and split a working tree into clean, independent commits. |
| [`product-designer`](product-designer/SKILL.md) | Turn a rough product idea into a buildable MVP brief — requirements, user stories, data model, metrics — using human-centered-design principles. |
| [`readme-writer`](readme-writer/SKILL.md) | Write, overhaul, or fix a project's README, ordered by the reader-involvement gradient and never fabricating commands or badges. |

## Install

These are [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills). Claude Code discovers a skill when its directory lives under a skills folder it scans — `~/.claude/skills/` for personal skills, or `.claude/skills/` inside a project.

Clone the repo and link the skills you want into your personal skills directory:

```sh
git clone https://github.com/Punpun1643/claude-skills.git
cd claude-skills

mkdir -p ~/.claude/skills
# Link a single skill…
ln -s "$PWD/readme-writer" ~/.claude/skills/readme-writer
# …or link them all
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
