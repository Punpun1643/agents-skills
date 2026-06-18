---
name: git-commit
description: Write clear, well-structured git commit messages that follow the Conventional Commits specification. Use this whenever you are about to commit staged or unstaged changes, write or rewrite a commit message, amend or squash commits, or are asked to "commit this", "write a commit message", or "clean up the history" — even when the user never says the words "conventional commits". Also use when configuring commit linting (commitlint/husky), generating a CHANGELOG, or reasoning about which semantic-version bump a set of changes implies.
---

# Git Commit (Conventional Commits)

Produce commit messages that are precise, scannable, and machine-parseable. A good commit message explains *what* changed and *why*, in a form that tools can use to generate changelogs and infer semantic-version bumps automatically.

## Message structure

Every message follows this shape:

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

Only the `<type>:` prefix and `<description>` are required. The blank lines separating description, body, and footers are mandatory when those sections exist — parsers rely on them.

## Workflow

Do not write a message from the prompt alone. Read the actual change first, then compose.

1. **Inspect what changed.** Run `git status` to see scope, then `git diff` (unstaged) and `git diff --staged` (staged) to see the substance. The diff tells you the real intent; the user's phrasing may not.
2. **Decompose into independent commits.** Before composing anything, partition the working tree into the smallest set of self-contained, logically-separate commits — one concern each. This is a required step, not an optional cleanup. See *Structuring changes into independent commits* below for how.
3. **Pick the type** from the dominant intent of the change (see table below).
4. **Pick a scope** (optional) — the area of the codebase touched, e.g. `parser`, `auth`, `api`.
5. **Write the description** — imperative mood, lowercase, no trailing period, kept short (aim for ≤ 50 characters).
6. **Add a body** only if the *why* isn't obvious from the description (rationale, trade-offs, context).
7. **Add footers** for breaking changes, issue references, reviewers, or co-authors.
8. **Verify before committing.** Re-read it: does the type match the change? Is it genuinely one logical change? If any public API/behavior broke, is that signalled with `!` or a `BREAKING CHANGE:` footer?

## Structuring changes into independent commits

This is the highest-leverage thing the skill does. A pile of mixed changes committed together is hard to review, hides what each change was for, and breaks the link between a commit and its version bump. So before writing any message, split the working tree into the smallest set of **independent, self-contained commits** — each one a single logical change that could stand (and ideally build) on its own.

**Group by intent, not by file.** The unit is a *concern*, not a path:
- One logical change often spans several files — a function, its test, and its doc entry belong in the *same* commit.
- One file often holds hunks from different concerns — an unrelated typo fix sitting next to new feature code belongs in a *different* commit.

**Mechanics for splitting a mixed tree:**
1. Survey everything first — `git status`, `git diff`, and `git diff --staged` — to see the full picture before staging anything.
2. Stage one concern at a time. Use `git add <path>` for whole files, and `git add -p` (interactive hunk staging) to peel apart changes that share a file: `y`/`n` per hunk, `s` to split a hunk into smaller ones, `e` to edit it by hand.
3. Confirm the staged set is exactly one concern with `git diff --staged`. Back out anything that slipped in with `git restore --staged <path>`.
4. Commit that concern with its conventional message, then repeat for the next.
5. Park work that isn't ready with `git stash` (or `git stash -p`) so it doesn't muddy the commits you're making now.

**Order commits so the tree always works.** Land foundational changes first — a refactor or shared helper before the feature that uses it, a dependency bump before the code that needs it. Each commit should ideally leave the project buildable with tests passing, so `git bisect` and partial reverts stay meaningful.

**Don't over-split.** The target is one *logical* change, not one line. A coherent feature whose parts only make sense together is a single commit — fragmenting it creates noise and broken intermediate states. The test: if two changes are genuinely independent, separate them; if removing one would break the other, keep them together.

When you present the plan to the user, briefly lay out the commits you intend to make (e.g. "I'll split this into three: `refactor(db): …`, `feat(api): …`, `docs: …`") before — or as — you create them, so the boundaries are reviewable.

## Writing the description


Use the **imperative mood** — write the description as a command that completes the sentence "If applied, this commit will ___".

- ✅ `fix: prevent racing of requests`
- ❌ `fix: fixed the racing of requests` (past tense)
- ❌ `fix: prevents racing of requests` (third person)

Keep it specific. `fix: handle empty CSV header row` is useful; `fix: bug fixes` and `chore: update` are noise.

## Types

| Type | Use for | SemVer |
|------|---------|--------|
| `feat` | A new feature for the user or API | **MINOR** |
| `fix` | A bug fix | **PATCH** |
| `docs` | Documentation only | — |
| `style` | Formatting/whitespace/semicolons; no change to code meaning | — |
| `refactor` | A code change that neither fixes a bug nor adds a feature | — |
| `perf` | A change that improves performance | — |
| `test` | Adding or correcting tests | — |
| `build` | Build system or external dependencies (npm, webpack, Docker…) | — |
| `ci` | CI configuration and scripts (GitHub Actions, CircleCI…) | — |
| `chore` | Maintenance that doesn't touch src or tests | — |
| `revert` | Reverting a previous commit | — |

`feat` and `fix` are the only types the spec *mandates*; the rest are the widely-used Angular/commitlint convention. Teams may add their own types — consistency matters more than the exact list. Types other than `feat`/`fix` carry **no** implicit version bump unless they include a breaking change.

If a change genuinely fits two types, that's a signal it should be **two commits**. Split it.

## Scope

A scope is an optional noun in parentheses naming the affected section of the codebase:

```
feat(parser): add ability to parse arrays
```

Use it when it adds clarity about *where* the change lives. Keep scope names short and consistent across the project (`api`, `auth`, `db`, `ui`…). Omit it when the change is broad or a scope wouldn't help.

## Breaking changes

A breaking change is anything that forces consumers to change their code. Signal it in **one or both** ways — either triggers a **MAJOR** bump regardless of type:

1. **`!` before the colon:**
   ```
   feat!: drop support for Node 6
   ```
2. **A `BREAKING CHANGE:` footer:**
   ```
   feat: allow config object to extend other configs

   BREAKING CHANGE: `extends` key is now used for extending other config files
   ```

You can combine them. When `!` is present, the footer may be omitted and the description itself explains the break. `BREAKING CHANGE` **must be uppercase** in a footer; `BREAKING-CHANGE` (with a hyphen) is an accepted synonym. A breaking change can ride on *any* type — `refactor!`, `chore!`, etc.

## Body

The body is free-form, starts one blank line after the description, and may span multiple paragraphs. Use it to explain motivation and contrast with previous behavior — the *why*, not a restatement of the *what* (the diff already shows the what).

## Footers

Footers come one blank line after the body and follow the git-trailer convention: a token, then `: ` or ` #`, then a value.

- Tokens replace spaces with hyphens: `Reviewed-by`, `Acked-by`, `Co-authored-by`. (The sole exception is `BREAKING CHANGE`, which keeps its space.)
- Common footers: `Refs: #123`, `Closes: #45`, `Reviewed-by: Z`, `Co-authored-by: Jane Doe <jane@example.com>`.
- A footer value may contain spaces and newlines; parsing ends when the next valid token/separator pair appears.

## Examples

**A bug fix, no body:**
```
fix: array parsing issue when multiple spaces in string
```

**A feature with scope:**
```
feat(lang): add Polish language
```

**Docs change:**
```
docs: correct spelling of CHANGELOG
```

**Breaking change with `!` and an explanatory footer:**
```
feat(api)!: send an email to the customer when a product is shipped

BREAKING CHANGE: the shipping webhook payload now omits the legacy `status` field
```

**Multi-paragraph body with multiple footers:**
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

**A revert:**
```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Semantic-version mapping

When reasoning about releases from commit history:

- `fix:` → **PATCH** (0.0.x)
- `feat:` → **MINOR** (0.x.0)
- any commit with `!` or `BREAKING CHANGE:` → **MAJOR** (x.0.0)

## Common mistakes to avoid

- **Past-tense or third-person descriptions** — use the imperative ("add", not "added"/"adds").
- **Trailing period** on the description line.
- **Vague descriptions** — "fix stuff", "update", "changes". Say what and where.
- **Wrong type** — e.g. labelling a user-facing bug fix as `chore`, which hides it from the changelog and version bump.
- **Mixing unrelated changes** in one commit — split them.
- **Missing breaking-change signal** — if a public API or behavior changed incompatibly, it needs `!` or a `BREAKING CHANGE:` footer, or the MAJOR bump gets missed.
- **Lowercase `breaking change` footer** — the token must be uppercase to be recognized.

## Notes

- Casing of the type is conventionally lowercase; be consistent within a project. The spec treats the units as case-insensitive *except* `BREAKING CHANGE`.
- During early/initial development, write messages as if the project is already released — someone is always a consumer, even if it's only your teammates.
- For squash-based workflows, casual contributors needn't follow the convention; the maintainer writes the clean conventional message at merge time.

