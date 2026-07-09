# Starship OS — Manual Updates (v1.0 → v2 starter prompt)

**What this is:** Six standalone, paste-able update prompts for anyone who already built a ship from the v1.0 starter prompt and wants specific v2 architecture improvements retrofitted — without re-running the full interview/build.

**How to use:** Pick the update(s) you want. Paste that update's prompt as a message into your existing ship's Claude Code project (or wherever your ship lives). Each prompt is self-contained — it tells Claude how to find the right files in *your* ship regardless of what you named things. Apply them in any order; none depend on each other.

**Not included:** the full v1.0→v1.1 behavioral changelog (Slack patterns, Granola sweeps, EOD tiers, etc.) — that's a separate, larger update series covering system-specific evolution, not core architecture. This series is core-architecture only.

---

## Update 1 of 6 — Spine index/detail file splitting

**What it does:** If your dispatch log or open-questions register has grown long, boot is re-reading the whole thing every session. This splits high-frequency spine files into a lightweight index (boot reads every time) and a full detail file (pulled only when actively working that thread).

```
Your ship's boot sequence currently reads the full orchestration/dispatch log and the full open-questions register at every session open. I want to split both into a lightweight index + full detail file, so boot stays cheap as they grow.

1. Find your ship's dispatch/orchestration log (tracks work handed to crew members) and your open-questions/parked-questions register. They're probably under a spine/memory directory — find them by content, not by an assumed filename.

2. For the dispatch log: create a new file that's a **boot-read index** — one line per *currently open* dispatch (status icon, who it's assigned to, what the task is, when it opened). The existing full log stays as-is and keeps every entry, including closed ones — that remains the permanent record.

3. For the open-questions register: create a new file that's a **boot-read index** — one line per question (ID, the question itself, current status). The existing full register stays as-is with full detail per entry.

4. Update your boot sequence (wherever it's defined — your main instruction file and/or your ship's spec file) to read the two new index files at boot instead of the two full files. State explicitly that the full files are only pulled when actively working that specific thread, not at every boot.

5. Update whichever role writes to these logs (your router/orchestrator role) so it writes to *both* files going forward: full detail to the log, one-line summary to the index. When a dispatch closes, remove it from the open index but keep it in the full log.

6. Backfill the two new index files from whatever's currently open in the existing full files, so this doesn't lose any live state.

Show me the new file structure and the boot-sequence diff before you finalize anything.
```

---

## Update 2 of 6 — External task-board sync

**What it does:** Adds an optional integration with a task app you already use (Asana, Trello, Linear, etc.) as a phone-accessible mirror of your open loops — checkable between sessions, read back in at boot.

```
I want my ship's open loops mirrored to [NAME YOUR TASK APP — e.g. Asana, Trello, Linear] so I can check things off from my phone between sessions, and have my ship read completions back in at the next boot.

1. Confirm what MCP or API access you have to [YOUR TASK APP] in this environment. If none, tell me what's needed before we go further.

2. Pick (or ask me to confirm) the board/project/list that will hold synced tasks.

3. Add a step to my ship's session-close/wrap ritual: for every open loop opened this session, create a task in the matching status section of the board. For every open loop closed this session, mark the matching task complete by name-matching against existing tasks — if no match is found, skip silently, don't invent a phantom completion.

4. Add a step to my ship's session-open/boot ritual: read the board, treat anything marked complete there as closed in my system too, and surface a one-line count in the boot alerts ("N items closed via [app] since last session").

5. This is a *view*, not a replacement for my session spine — the spine stays the narrative record of what happened; the task board is just a live checklist. Make sure nothing you write treats the task board as ground truth.

Write this into whichever file(s) define my boot and wrap rituals. Show me the diff before finalizing.
```

---

## Update 3 of 6 — Entity spine files

**What it does:** If any of your crew members track multiple ongoing relationships (clients, projects, people, partners), this gives each one its own persistent file instead of letting that context get buried in the general session log.

```
One of my crew members — [NAME THE ROLE, e.g. "my Build-Path Architect" or whatever tracks per-client/per-project work] — currently has to reconstruct context about each relationship by searching back through my general session log. I want dedicated per-entity files instead.

1. Find that crew member's spec file and figure out what kind of entity they track (clients? projects? people? something else).

2. Create a new directory under my spine (e.g. spine/[entity-type]/) and, for each entity currently mentioned anywhere in my system, create one file with this shape: status, key contacts/people involved, background/context, open questions or loops specific to this entity, a dated session/event history, and a notes/sentiment section.

3. Update that crew member's spec so going forward: any time this entity comes up in conversation, they read (or create, if new) that entity's file first, and write updates back to it — not just to the general session spine. State explicitly: never let context about one specific relationship live only in the general session log, where it'll get buried under unrelated entries.

4. Backfill what you can find from existing session history into the new per-entity files — don't leave them empty if there's real prior context sitting in old spine entries.

Show me the new file structure and a sample populated entity file before you backfill everything.
```

---

## Update 4 of 6 — Standing status index

**What it does:** Once you have entity spine files (Update 3), this adds a single at-a-glance rollup across all of them — so you don't have to open ten files to see where everything stands.

```
I now have per-entity spine files (clients/projects/people — see Update 3). I want a single standing index that rolls them all up into one at-a-glance view.

1. Find the entity spine files created in Update 3.

2. Create one new file (e.g. spine/[domain]-status.md) that lists every entity, grouped by status/stage, one line each, pulling from each entity file's status field.

3. Critical: this file is a **denormalized view, refreshed on request — not read or rebuilt automatically at every boot, and not ground truth.** State this explicitly in the file's own header, in plain language, so it's never mistaken for a live pull. The entity spine files remain the source of truth; this index can go stale between refreshes and that's expected.

4. Tell me what phrase to use when I want it refreshed (e.g. "refresh my [domain] index") and wire that phrase to regenerate the file from the current state of all entity spines.

Show me the generated file and confirm the refresh trigger phrase with me before finalizing.
```

---

## Update 5 of 6 — Two-tier context awareness

**What it does:** If your ship only warns you about one kind of context pressure, this splits it into the two things that actually happen at different points: the model's real token ceiling, and (if your platform has one) an earlier harness-level compaction/summarization threshold.

```
My ship currently has one context-awareness warning. I want it split into two distinct signals, because they mean different things and happen at different times.

1. Find wherever my ship's spec currently describes context/token awareness (likely in the boot-identity spec file).

2. Rewrite it to distinguish two signals:
   - Model context window — the underlying model's token ceiling. Can't be read directly, but infer it from a long session (many tool calls, large reads, hours of back-and-forth). Warning: "This session's getting long — wrap at a good stopping point to preserve it cleanly."
   - Harness-level compaction (only if this platform has one — e.g. Claude Code's auto-compact) — a separate, earlier threshold that summarizes context before the real ceiling is hit. If this platform exposes that distinction, flag it separately: "we already lost some fidelity, consider wrapping now" is a different message than "wrap soon."

3. Tell me whether this platform actually exposes the harness-level signal or not — if it doesn't, just implement the model-context-window warning and skip the second tier rather than inventing a fake one.

4. Both warnings should fire once, not repeatedly — escalate only if the session keeps running well past the first flag.

Show me the rewritten section before finalizing.
```

---

## Update 6 of 6 — Automation-mechanism guardrail

**What it does:** If your ship (or any crew member) runs scheduled/recurring automation, this makes sure you're using a mechanism that actually survives — not one that silently expires.

```
I want to add a guardrail to my ship about picking the right automation mechanism, because I don't want to accidentally schedule something that silently stops working.

1. Check what scheduling/automation mechanisms are actually available in this environment. Some platforms offer both a session-scoped kind (tied to or expiring with a session) and a durable/cloud-triggered kind (keeps running independent of any open session) — others only offer one.

2. If both exist here: add a rule to my main instruction file stating that session-scoped scheduling is only for short-lived or session-bound tasks, and durable/cloud-triggered scheduling is required for anything that must run indefinitely (daily digests, recurring sweeps, standing reminders). Explain that getting this backwards means "run every morning forever" work silently stops when a session ends or a local schedule expires.

3. If only one mechanism exists here, tell me its actual limitations (does it expire? does it need a live session?) so I know what I'm actually getting when I ask for something recurring — don't just assume it's durable.

4. Audit anything I've already scheduled in this system and flag if it's using the wrong mechanism for how long I actually need it to run.

Report back what you found before changing anything.
```

---

*Series 1 of an ongoing set. A second series covering the broader v1.0→v1.1 behavioral evolution (crew additions, connector protocols, standing rules) is planned separately.*
