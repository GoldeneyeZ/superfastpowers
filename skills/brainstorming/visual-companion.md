# Visual Companion Guide

Browser visual brainstorming companion for mockups, diagrams, options.

## When to Use

Decide per-question, not per-session. Test: **would the user understand this better by seeing it than reading it?**

**Use the browser** when content itself is visual:

- **UI mockups** — wireframes, layouts, navigation structures, component designs
- **Architecture diagrams** — system components, data flow, relationship maps
- **Side-by-side visual comparisons** — compare layouts, color schemes, design directions
- **Design polish** — question about look/feel, spacing, visual hierarchy
- **Spatial relationships** — state machines, flowcharts, entity relationships rendered as diagrams

**Use the terminal** when content is text/tabular:

- **Requirements and scope questions** — "what does X mean?", "which features are in scope?"
- **Conceptual A/B/C choices** — choose between word-described approaches
- **Tradeoff lists** — pros/cons, comparison tables
- **Technical decisions** — API design, data modeling, architectural approach selection
- **Clarifying questions** — answer is words, not visual preference

UI topic ≠ visual question. "What kind of wizard do you want?" conceptual — use terminal. "Which of these wizard layouts feels right?" visual — use browser.

## How It Works

Server watches directory for HTML files, serves newest to browser. Write HTML content to `screen_dir`; user sees it, clicks options. Selections recorded to `state_dir/events`; read next turn.

**Content fragments vs full documents:** If HTML starts with `<!DOCTYPE` or `<html`, server serves as-is (injects helper script only). Otherwise server wraps content in frame template: header, CSS theme, selection indicator, interactive infrastructure. **Write content fragments by default.** Write full documents only when full page control needed.

## Starting a Session

```bash
# Start server with persistence (mockups saved to project)
scripts/start-server.sh --project-dir /path/to/project

# Returns: {"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":"/path/to/project/.superfastpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superfastpowers/brainstorm/12345-1706000000/state"}
```

Save `screen_dir` and `state_dir` from response. Tell user to open URL.

**Finding connection info:** Server writes startup JSON to `$STATE_DIR/server-info`. If launched in background without stdout capture, read that file for URL/port. With `--project-dir`, check `<project>/.superfastpowers/brainstorm/` for session directory.

**Note:** Pass project root as `--project-dir` so mockups persist in `.superfastpowers/brainstorm/` across server restarts. Without it, files go to `/tmp` and get cleaned. Remind user to add `.superfastpowers/` to `.gitignore` if absent.

**Launching the server by platform:**

**Claude Code (macOS / Linux):**
```bash
# Default mode works — the script backgrounds the server itself
scripts/start-server.sh --project-dir /path/to/project
```

**Claude Code (Windows):**
```bash
# Windows auto-detects and uses foreground mode, which blocks the tool call.
# Use run_in_background: true on the Bash tool call so the server survives
# across conversation turns.
scripts/start-server.sh --project-dir /path/to/project
```
When calling via Bash tool, set `run_in_background: true`. Then read `$STATE_DIR/server-info` next turn for URL/port.

**Codex:**
```bash
# Codex reaps background processes. The script auto-detects CODEX_CI and
# switches to foreground mode. Run it normally — no extra flags needed.
scripts/start-server.sh --project-dir /path/to/project
```

**Gemini CLI:**
```bash
# Use --foreground and set is_background: true on your shell tool call
# so the process survives across turns
scripts/start-server.sh --project-dir /path/to/project --foreground
```

**Other environments:** Server must keep running in background across turns. If environment reaps detached processes, use `--foreground` and platform background execution.

If URL unreachable from browser (common remote/container setups), bind non-loopback host:

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

Use `--url-host` to control hostname printed in returned URL JSON.

## The Loop

1. **Check server is alive**, then **write HTML** to a new file in `screen_dir`:
   - Before each write, check `$STATE_DIR/server-info` exists. If missing (or `$STATE_DIR/server-stopped` exists), server shut down — restart with `start-server.sh` before continuing. Server auto-exits after 30 minutes inactivity.
   - Use semantic filenames: `platform.html`, `visual-style.html`, `layout.html`
   - **Never reuse filenames** — each screen gets fresh file
   - Use Write tool — **never use cat/heredoc** (dumps noise into terminal)
   - Server serves newest file automatically

2. **Tell user what to expect and end your turn:**
   - Remind them of URL every step, not just first
   - Give brief text summary of screen (e.g., "Showing 3 layout options for the homepage")
   - Ask them to respond in terminal: "Take a look and let me know what you think. Click to select an option if you'd like."

3. **On your next turn** — after user responds in terminal:
   - Read `$STATE_DIR/events` if it exists — user's browser interactions (clicks, selections) as JSON lines
   - Merge with terminal text for full picture
   - Terminal message is primary feedback; `state_dir/events` adds structured interaction data

4. **Iterate or advance** — if feedback changes current screen, write new file (e.g., `layout-v2.html`). Move to next question only when current step validated.

5. **Unload when returning to terminal** — when next step doesn't need browser (e.g., clarifying question, tradeoff discussion), push waiting screen to clear stale content:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   Prevents user staring at resolved choice after conversation moved on. When next visual question comes up, push new content file as usual.

6. Repeat until done.

## Writing Content Fragments

Write only content inside page. Server wraps in frame template automatically (header, theme CSS, selection indicator, interactive infrastructure).

**Minimal example:**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

That's it. No `<html>`, no CSS, no `<script>` tags needed. Server provides all.

## CSS Classes Available

Frame template provides CSS classes for content:

### Options (A/B/C choices)

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select:** Add `data-multiselect` to container so users select multiple options. Each click toggles item. Indicator bar shows count.

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### Cards (visual designs)

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view (side-by-side)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros/Cons

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements (wireframe building blocks)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections

- `h2` — page title
- `h3` — section heading
- `.subtitle` — secondary text below title
- `.section` — content block with bottom margin
- `.label` — small uppercase label text

## Browser Events Format

When user clicks browser options, interactions recorded to `$STATE_DIR/events` (one JSON object per line). File clears automatically when new screen pushed.

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

Full event stream shows exploration path — user may click multiple options before settling. Last `choice` event usually final selection; click pattern can reveal hesitation/preferences worth asking about.

If `$STATE_DIR/events` doesn't exist, user didn't interact with browser — use only terminal text.

## Design Tips

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions
- **Explain the question on each page** — "Which layout feels more professional?" not just "Pick one"
- **Iterate before advancing** — if feedback changes current screen, write new version
- **2-4 options max** per screen
- **Use real content when it matters** — for photography portfolio, use actual images (Unsplash). Placeholder content hides design issues.
- **Keep mockups simple** — focus layout/structure, not pixel-perfect design

## File Naming

- Use semantic names: `platform.html`, `visual-style.html`, `layout.html`
- Never reuse filenames — each screen must be new file
- For iterations: append version suffix like `layout-v2.html`, `layout-v3.html`
- Server serves newest file by modification time

## Cleaning Up

```bash
scripts/stop-server.sh $SESSION_DIR
```

If session used `--project-dir`, mockup files persist in `.superfastpowers/brainstorm/` for later reference. Only `/tmp` sessions deleted on stop.

## Reference

- Frame template (CSS reference): `scripts/frame-template.html`
- Helper script (client-side): `scripts/helper.js`
