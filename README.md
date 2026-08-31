# agents-skills

A collection of portable [Agent Skills](https://agentskills.io/) for Claude Code and Codex. Each skill is a reusable, model-invoked playbook for a focused documentation or development workflow.

## Skills

| Skill | What it does | Credit |
| --- | --- | --- |
| [`cognitive-map`](plugins/agents-skills/skills/cognitive-map/SKILL.md) | Build a goal-oriented map of a topic's core concepts, dependencies, branches, and learning paths. | — |
| [`dev-guide`](plugins/agents-skills/skills/dev-guide/SKILL.md) | Create and maintain a repository's developer or architecture guide, grounded in real code. | — |
| [`excalidraw`](plugins/agents-skills/skills/excalidraw/SKILL.md) | Generate architecture diagrams as editable `.excalidraw` files, with optional PNG/SVG export. | Adapted from [ooiyeefei/ccc](https://github.com/ooiyeefei/ccc/tree/main/skills/excalidraw) |
| [`git-commit`](plugins/agents-skills/skills/git-commit/SKILL.md) | Write Conventional Commits and split a working tree into clean, independent commits. | Based on [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) |
| [`product-designer`](plugins/agents-skills/skills/product-designer/SKILL.md) | Turn a rough product idea into a testable, buildable MVP brief. | HCD principles from [_The Design of Everyday Things_](https://en.wikipedia.org/wiki/The_Design_of_Everyday_Things) |
| [`readme-writer`](plugins/agents-skills/skills/readme-writer/SKILL.md) | Write or improve a project's README without fabricating commands, badges, or behavior. | Based on [makeareadme.com](https://www.makeareadme.com) |
| [`teach`](https://www.aihero.dev/skills-teach) | Turn the current directory into a stateful, multi-session learning workspace with short, citation-grounded lessons. | By Matt Pocock — [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) (MIT) |

---

### cognitive-map

Build a cognitive map that helps a learner get oriented in an unfamiliar subject.

- Identifies the central question and the smallest high-leverage conceptual spine.
- Shows prerequisites, relationships, major branches, and alternative learning paths.
- Includes misconceptions, negative expertise, and a practical learning frontier.

Invoke with `$cognitive-map` in Codex, `/agents-skills:cognitive-map` when installed as a Claude Code plugin, `/cognitive-map` as a standalone Claude skill, or ask to “map this topic for me.”

---

### dev-guide

Create and maintain a repository's developer or architecture guide.

- Grounds every description in code that was actually inspected.
- Chooses the correct diagram type for each idea.
- Links components to their source and traces real data and control flows.
- Includes references for [guide structure](plugins/agents-skills/skills/dev-guide/references/structure.md) and [diagrams](plugins/agents-skills/skills/dev-guide/references/diagrams.md).

Invoke with `$dev-guide` in Codex, `/dev-guide` in Claude Code, or ask to “update the dev guide” or “document this module.”

---

### excalidraw

Generate architecture diagrams as editable `.excalidraw` files from codebase analysis.

- Maps components, services, databases, APIs, and data flows.
- Uses cloud-provider color palettes for AWS, Azure, GCP, and Kubernetes.
- Handles arrow routing, bindings, and staggering to reduce overlap.
- Can export to PNG or SVG with Playwright.

Invoke with `$excalidraw` in Codex, `/excalidraw` in Claude Code, or ask to “create an architecture diagram.”

---

### git-commit

Write Conventional Commits and structure a working tree into clean commits.

![Real `git log` from this repository after using the git-commit skill](assets/git-commit.png)

_The commits in this capture were written using the skill._

- Reads the actual diff before composing a message.
- Splits mixed changes into independent, self-contained commits.
- Applies Conventional Commits types, scopes, breaking changes, and SemVer mapping.

Invoke with `$git-commit` in Codex, `/git-commit` in Claude Code, or ask to “commit this” or “write a commit message.”

---

### product-designer

Turn a rough product idea into a focused MVP brief.

- Produces personas, jobs-to-be-done, requirements, user stories, acceptance criteria, a data model, metrics, risks, and milestones.
- Makes requirements testable and traceable to user needs.
- Applies human-centered design principles throughout the workflow.

Invoke with `$product-designer` in Codex, `/product-designer` in Claude Code, or ask to “write a PRD” or “turn this idea into an MVP plan.”

---

### readme-writer

Write, overhaul, or fix a project's README.

- Orders content by the reader-involvement gradient: identity, proof, quickstart, depth.
- Verifies commands, examples, configuration, and badges against the repository.
- Adapts its structure for libraries, CLIs, research/ML projects, and web services.

Invoke with `$readme-writer` in Codex, `/readme-writer` in Claude Code, or ask to “make a README” or “document this project.”

## Install for Codex

The repository is packaged as a [Codex plugin](https://developers.openai.com/plugins/build/plugins), so all six skills can be installed together from its marketplace:

```sh
codex plugin marketplace add Punpun1643/agents-skills
codex plugin add agents-skills@Punpun1643
```

Start a new Codex session after installation. Run `/skills` to browse the installed skills, mention one explicitly with `$skill-name`, or let Codex select one automatically from your request.

### Install one standalone skill

Clone the repository, then symlink one skill into Codex's personal skills directory:

```sh
git clone https://github.com/Punpun1643/agents-skills.git
cd agents-skills
mkdir -p ~/.agents/skills
ln -s "$PWD/plugins/agents-skills/skills/readme-writer" ~/.agents/skills/readme-writer
```

Replace `readme-writer` with any skill name from the table above. Codex supports symlinked skill folders, so pulling the clone updates the installed skill.

To pin a fixed version instead, copy the folder:

```sh
cp -R "$PWD/plugins/agents-skills/skills/readme-writer" ~/.agents/skills/readme-writer
```

## Install for Claude Code

Install the complete collection as a Claude Code plugin from its marketplace:

```sh
claude plugin marketplace add Punpun1643/agents-skills
claude plugin install agents-skills@Punpun1643
```

Plugin skills are namespaced in Claude Code. For example, invoke the README skill with `/agents-skills:readme-writer`, or describe the task and let Claude select the skill automatically.

### Install one standalone skill

Clone the repository and create Claude Code's personal skills directory:

```sh
git clone https://github.com/Punpun1643/agents-skills.git
cd agents-skills
mkdir -p ~/.claude/skills
```

Install all skills as symlinks so they track the clone:

```sh
for d in cognitive-map cognitive-map-open dev-guide excalidraw git-commit product-designer readme-writer; do
  ln -s "$PWD/plugins/agents-skills/skills/$d" ~/.claude/skills/"$d"
done
```

Or install a fixed snapshot by replacing `ln -s` with `cp -R`:

```sh
for d in cognitive-map cognitive-map-open dev-guide excalidraw git-commit product-designer readme-writer; do
  cp -R "$PWD/plugins/agents-skills/skills/$d" ~/.claude/skills/"$d"
done
```

## License

Released under the [MIT License](LICENSE). The adapted Excalidraw skill also includes its [upstream attribution](plugins/agents-skills/skills/excalidraw/LICENSE).
