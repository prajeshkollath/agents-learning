# Learning Guide: How to Use Your Documentation

This project generates three different formats of documentation for each topic. Each serves a different purpose in your learning journey.

---

## The Three Formats

### 1. **Notes** (`notes/*.md`)
**Purpose:** Comprehensive study material with full explanations

**What's inside:**
- Detailed definitions and concepts
- Your own explanations and understanding
- Tables for comparisons
- Examples discussed during tutoring sessions
- Analogies and mental models
- Common misconceptions

**Best for:**
- Initial learning of a new topic
- Deep study sessions
- Understanding "why" and "how"
- Preparing for complex topics

**How to use:**
- Read in VS Code or any Markdown viewer
- Use VS Code's Markdown preview (`Ctrl+Shift+V`)
- Take your time, read sequentially
- Refer back when concepts get fuzzy

---

### 2. **Mindmaps** (`mindmaps/*.md` → `.html`)
**Purpose:** Interactive hierarchical view for exploration and review

**What's inside:**
- Structured breakdown of all concepts
- Multiple levels of detail (H2, H3, H4, bullets)
- Complete coverage of subtopics
- All key points organized hierarchically

**Best for:**
- Visual learners
- Review and revision
- Seeing relationships between concepts
- Interactive exploration (expand/collapse branches)
- Study sessions where you want to navigate freely

**How to view:**
1. Convert to HTML: `markmap <filename>.md -o <filename>.html`
2. Open the `.html` file in your browser
3. Click nodes to expand/collapse
4. Zoom and pan to explore

**When to use:**
- After reading notes, to reinforce structure
- Before moving to the next topic (quick review)
- When you need to see "the big picture"
- During revision sessions

---

### 3. **Mermaid Diagrams** (`diagrams/*.mmd`)
**Purpose:** Quick visual reference and glanceable overview

**What's inside:**
- Key concepts only (condensed)
- 2-3 levels deep maximum
- Visual icons for quick recognition
- Clean, simple structure

**Best for:**
- Quick reference during coding/work
- At-a-glance reminders
- Embedding in other documents
- When you already know the topic but need a refresher
- Posters/wallpapers for passive learning

**How to view:**
- Use Mermaid Chart extension in VS Code
- Right-click → "Preview Mermaid" (or similar)
- Or use Command Palette → "Mermaid: Preview"
- Can also paste into https://mermaid.live for online viewing

**When to use:**
- Quick lookups ("What were the 3 prompt techniques again?")
- As a cheat sheet while building projects
- After mastering a topic (quick refresher)

---

## Comparison Table

| Aspect | Notes | Mindmaps | Mermaid Diagrams |
|--------|-------|----------|------------------|
| **Detail Level** | High (complete) | Medium-High (structured) | Low (key points) |
| **Depth** | Linear, thorough | Hierarchical, expandable | Flat, concise |
| **Best Phase** | Learning | Reviewing | Quick reference |
| **Format** | Prose + tables | Collapsible tree | Visual diagram |
| **Reading Time** | 10-20 min | 5-10 min | 1-2 min |
| **Interaction** | Read sequentially | Click to explore | View statically |
| **Use Case** | Understand deeply | Reinforce structure | Recall quickly |

---

## Suggested Learning Workflow

### Phase 1: **Learn** (First Encounter)
1. **Tutor Session**: Learn the topic with the Tutor agent
2. **Documenter Creates**: Notes, mindmap, diagram generated
3. **Read Notes**: Go through `notes/XX-topic.md` thoroughly
4. **View Mindmap**: Open the HTML mindmap to see structure
5. **Check Understanding**: Can you explain it back?

### Phase 2: **Review** (Same Day or Next Day)
1. **Open Mindmap**: Click through to test recall
2. **Refer to Notes**: For sections you forgot
3. **Glance at Diagram**: Quick visual reinforcement

### Phase 3: **Reinforce** (Week Later)
1. **Start with Diagram**: Can you remember from just the visual?
2. **Use Mindmap**: If you need more detail
3. **Back to Notes**: Only if you've forgotten key concepts

### Phase 4: **Reference** (During Work/Projects)
1. **Mermaid Diagram**: Quick lookup while coding
2. **Mindmap**: If you need more context
3. **Notes**: Deep dive if implementing something complex

---

## Tips for Maximum Learning

### For Visual Learners
- Convert mindmaps to HTML immediately
- Keep diagrams open in a browser tab
- Print Mermaid diagrams as posters

### For Text Learners
- Start with notes, read thoroughly
- Use mindmaps to verify you didn't miss anything
- Diagrams as quick reminders only

### For Active Learners
- After reading notes, try to recreate the mindmap structure from memory
- Compare with actual mindmap to find gaps
- Use the Evaluator agent to test yourself

### Spaced Repetition
- Day 1: Notes (deep learning)
- Day 2: Mindmap (review structure)
- Day 7: Diagram (quick recall test)
- Day 14: Mindmap (reinforce)
- Day 30: Diagram (long-term retention check)

---

## Special Use Cases

### Before Building Code
1. Review the Mermaid diagram for the relevant topic
2. Keep it visible while coding
3. Refer to notes if you hit a complex implementation

### Before Evaluations
1. Start with diagram (quick warm-up)
2. Expand with mindmap (structured review)
3. Dive into notes for areas you're weak

### When Stuck on a Concept
1. Re-read the notes section carefully
2. Explore the mindmap interactively
3. Ask the Tutor agent for clarification
4. Update your notes with new understanding

---

## Maintenance

### After Each Topic
- [ ] Verify all three formats were created
- [ ] Convert mindmap to HTML
- [ ] Open each format to verify content
- [ ] Commit to git with proper message

### Weekly Review
- Browse through all Mermaid diagrams (quick refresh of everything)
- Pick 1-2 topics to explore via mindmap
- Note any gaps and discuss with Tutor agent

### Before Moving to Next Phase
- Review all diagrams from current phase
- Use Evaluator agent to test understanding
- Fill gaps before proceeding

---

## Tools Setup

### Required
- VS Code with Markdown preview (built-in)
- Mermaid Chart extension (for `.mmd` preview)
- markmap-cli (for mindmap HTML conversion)
  ```bash
  npm install -g markmap-cli
  ```

### Optional but Recommended
- Browser of choice (for HTML mindmaps)
- Markdown Preview Mermaid Support extension (alternative)
- Live Server extension (for live preview of HTML mindmaps)

---

## Remember

> **Notes** = Learn deeply
> **Mindmaps** = Review structure
> **Diagrams** = Recall quickly

Each format has its time and place. Use all three for maximum retention and understanding!

---

*See [ROADMAP.md](ROADMAP.md) for your learning progress.*
