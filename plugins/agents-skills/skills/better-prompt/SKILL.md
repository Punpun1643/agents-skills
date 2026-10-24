---
name: better-prompt
description: Deepen a prompt without making it bigger. Before rewriting, name what a top professional in the field would do that the prompt leaves out, the rawest material they would start from, the specific methods and tools they would use, and the outside evidence that would show the result is right. Then rewrite the prompt with those built in. Use when the user asks to improve, sharpen, deepen, upgrade, or rewrite a prompt, says "better-prompt this", "make this prompt better", or "how would an expert ask this", or pastes a prompt and asks what it is missing.
---

# Better prompt

Make a prompt deeper, not bigger. A deeper prompt asks for the same deliverable but gets it the way the best practitioner in the field would: from better inputs, with real methods, checked against something outside the conversation. A bigger prompt adds sections, deliverables, and adjectives. Do the first. Refuse the second.

## Input

The prompt to improve, verbatim. If the user only describes it, ask for the text. If they invoke the skill with no prompt, use their most recent request as the prompt.

Use the context around it too: files in the repo, earlier messages, the model or tool it is meant for. That context often tells you the field and the raw material better than the prompt does.

## Process

### 1. Pin down the task

Write two lines and show them in the output.

- **Field.** The profession that does this work for a living. Be specific: "B2B SaaS retention analyst", not "data". If the task spans fields, name the one whose judgment decides whether the result is good.
- **Deliverable.** What the prompt asks for, and its rough size. This is fixed. The rewrite must ask for the same kind of thing at about the same size. If the original sets no length or size, don't invent one. Leave it out or use a placeholder.

If you can't tell the field or the deliverable and a wrong guess would change the answers, ask one question. Otherwise state your guess and continue.

### 2. Answer the four questions

Every answer must be specific enough that a practitioner would nod and a layperson would learn something. Generic answers fail: "be thorough", "use best practices", "check sources", "consult an expert". Replace each with the named thing.

1. **What a top professional would do that the prompt doesn't ask for.** Look for the step amateurs skip. Defining terms before measuring them. Comparing against a baseline or control group. Reading the failure cases. Deciding in advance what would change their mind. Give 2 to 4 items. Each one must serve the existing deliverable. If it creates a new deliverable, drop it.

2. **The rawest material they would start from.** Name it instead of the digested version the prompt relies on. Event logs instead of a dashboard. The primary paper instead of a summary. Source code instead of the docs. Call recordings instead of the survey report. The statute instead of a blog post about it. Say where it lives or how to get it. If the user may not have access, name the next-rawest thing.

3. **The specific methods and tools.** Techniques, frameworks, software, standards, checklists, all by name. "Cohort retention curves in SQL, then a Cox model" rather than "statistical analysis". Match the deliverable's size. A one-page memo doesn't need a pipeline.

4. **What, other than the model or the user, would show the result is right.** It must be able to fail. Good examples include a held-out dataset, a test suite, running the code, a primary source that either says the thing or doesn't, a prediction checked against next month's numbers, a reviewer in a named role, or a case with a known answer. Bad examples are "it looks reasonable", "the user is happy", and "cross-check with another AI".

### 3. Rewrite the prompt

Fold the four answers into the prompt as instructions to whoever will run it.

- Keep the user's goal, voice, constraints, and audience. Keep their wording where it already works.
- Same deliverable, same scale. No new sections, reports, or extras. The one allowed addition is a short line reporting the outside check from question 4, such as "end with the test you ran and its result".
- Tell the runner what to start from (question 2), how to work (questions 1 and 3), and what counts as done (question 4).
- Where only the user knows something (a file path, a metric definition, a date), leave a bracketed placeholder like `[path to export]`. Don't invent it.
- Short prompts will grow, and that's fine. Every added sentence must change how the work is done or how it's checked. Cut words like "comprehensive", "detailed", and "world-class", which ask for size, not depth.
- Write a prompt the user can paste as is, addressed to whoever runs it. Skip persona preambles like "You are a world-class..." unless the original had one. The named methods do that job better.

### 4. Check before showing

Run these on the rewrite and fix whatever fails.

- **Scope.** List the deliverables in the original and in the rewrite. If the rewrite has more, cut.
- **Swap test.** For each instruction, ask whether it would fit a prompt in an unrelated field unchanged. If it would, it's generic. Make it specific or delete it.
- **Falsifiable.** At least one outside check could come back negative.
- **Runnable.** The runner could start now once the placeholders are filled. Placeholders are fine. Hidden assumptions aren't.

## Output

Use this shape. Keep the four answers to a line or two per bullet. The rewrite is the product.

````markdown
**Field:** ...
**Deliverable:** ...

**1. What a top professional would add**
- ...

**2. Rawest material**
- ...

**3. Methods and tools**
- ...

**4. Outside evidence it's right**
- ...

**Rewritten prompt**

```
...
```

**Placeholders to fill:** ... (omit if none)
````

If the user then asks you to run the rewritten prompt, run it as written, including the outside check, and report that check's result.

## Example

Original prompt:

> Look at our churn data and tell me why customers are leaving.

**Field:** B2B SaaS retention analyst
**Deliverable:** a short explanation of the main reasons customers churn

**1. What a top professional would add**
- Split churn into involuntary (failed payments) and voluntary first. They have different causes and different fixes.
- Compare churned accounts with retained accounts of the same plan and tenure. A trait common among churned accounts means nothing if retained accounts share it.
- Keep what customers said separate from what their behavior predicted. The two often disagree.

**2. Rawest material**
- Per-account product events and billing events from the warehouse, not the churn dashboard.
- Cancellation-form text and support tickets from the 90 days before each cancellation, not the tagged summary.

**3. Methods and tools**
- Cohort retention curves by signup month and plan, in SQL.
- Kaplan-Meier curves, then a Cox proportional hazards model on usage features.
- Open coding of at least 50 cancellation reasons before relying on existing tags.

**4. Outside evidence it's right**
- Drivers found on earlier data predict churn in a held-out later period better than the base rate.
- The customer success team recognizes the top driver from their calls.

**Rewritten prompt**

```
Explain why customers are leaving, in under a page.

Work from raw data, not the dashboard: per-account product events and billing events from [warehouse tables], plus cancellation-form text and support tickets from the 90 days before each cancellation.

Split churn into involuntary (failed payment) and voluntary, and give each share. For voluntary churn:
- Compare churned accounts with retained accounts on the same plan and tenure. A driver only counts if it separates the two groups.
- Build cohort retention curves by signup month and plan, then fit a Cox model on usage features to rank drivers.
- Read and open-code at least 50 cancellation reasons yourself before trusting existing tags. Note where stated reasons and behavior disagree.

Fit on data before [cutoff date] and test on the 3 months after it. Keep a driver only if it predicts held-out churn better than the base rate, and give the lift. Give the top 3 drivers with the evidence for each, and one question I can ask the customer success team to confirm the top one.
```

**Placeholders to fill:** warehouse tables, cutoff date
