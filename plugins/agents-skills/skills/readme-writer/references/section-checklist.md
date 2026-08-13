# Canonical section checklist

The classic README section list (the GitLab README template). Every project is different — treat this as a menu, not a mandate: include the sections that apply and cut the rest. When a README feels too long, move detail into other docs (a `docs/` folder, `CONTRIBUTING.md`, `ARCHITECTURE.md`) rather than deleting information — too long beats too short.

Order these by the involvement gradient in SKILL.md (identity → proof → quickstart → depth → contribution → meta), with one exception: a **project-status** callout goes above everything when it's relevant.

| Section | Purpose | Notes |
| --- | --- | --- |
| **Name** | Self-explaining project name | The title. |
| **Description** | What it does, specifically, and for whom | Add context and links to unfamiliar references. May include **Features** and **Background** subsections and a "how this differs from alternatives" line. |
| **Badges** | Convey metadata (build passing, version, coverage) | Use [Shields](https://shields.io). Only real ones — a fake badge erodes trust. |
| **Visuals** | Show it working | Screenshots, video, or (commonly) GIFs. Terminal tools: `ttygif`, `asciinema`, `vhs`. The single highest-leverage element. |
| **Installation** | Get people running fast | Specific, step-by-step, verified commands. Assume the reader may be a novice. Add a **Requirements** subsection for version / OS / manual dependencies. |
| **Usage** | Show how to use it | Use examples liberally; show expected output. Inline the smallest example; link out to bigger ones. |
| **Support** | Where to get help | Issue tracker, chat room, email — any combination. Point to one obvious place. |
| **Roadmap** | Planned releases / direction | Only if concrete plans exist. |
| **Contributing** | Whether/how to contribute | State if you accept contributions and the requirements. Document dev setup (scripts, env vars), plus lint and test commands — especially any external setup (e.g. a Selenium server). Helps future-you too. |
| **Authors & acknowledgment** | Credit contributors | Show appreciation; nod to prior art. |
| **License** | How it's licensed | One line; full text in `LICENSE`. |
| **Project status** | Maintenance reality | If development has slowed/stopped, say so **at the top** so someone can fork or step in as maintainer. Can be an explicit call for maintainers. |
