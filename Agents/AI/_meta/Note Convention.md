---
title: Note Convention
created: 2026-06-22
tags:
  - meta
---

# Note Convention

How Claude Code writes AI-learning notes in this vault so they form a connected
Obsidian graph. This is the contract — every learning note follows it.

## 1. One concept per note (atomic)

Each note covers a single idea (e.g. `ReAct Prompting`, `Tool Calling`,
`Agent Loop`). Small, focused notes link together into a rich graph. Avoid
giant catch-all notes.

## 2. Frontmatter (required)

```yaml
---
title: <Concept Name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - ai-agents
  - <subtopic>        # e.g. prompting, memory, frameworks
status: learning      # learning | understood | reference
aliases: []           # alternate names so [[links]] resolve
---
```

## 3. Body structure

```markdown
# <Concept Name>

> One-sentence definition.

## What it is
## Why it matters
## How it works
## Q&A insights      ← questions that deepened understanding (see rule below)
## Related
- [[Other Concept]] — one line on how it connects
- Part of [[AI Agents MOC]]
```

## 4. Linking rules (this is what builds the graph)

- **Link every concept** mentioned that has — or should have — its own note,
  using `[[Concept Name]]`. Unresolved links are fine; they appear in the graph
  as planned notes and become real when written.
- **Every note links back to its MOC** (`[[AI Agents MOC]]`), so nothing is orphaned.
- Prefer linking over repeating: explain a concept once, link to it elsewhere.

## 5. Q&A insights rule (carried over from the project)

Notes must include BOTH the teaching content AND the Q&A insights — every
question Prajesh asked that changed or deepened understanding goes in the
`Q&A insights` section. After writing, ask: *"Did any question add nuance not
already captured?"* If yes, add it before finalising.

## 6. Files & folders

- New concept notes → `Topics/`
- Hubs / indexes → `MOCs/`
- Template → `_templates/Topic.md`
- Images/PDFs → `attachments/`

See also: [[AI Agents MOC]]
