# Starship OS — Manual Updates (v1.0 → v1.1 architecture)

**What this is:** Eight standalone, paste-able update prompts for anyone who built a ship from the v1.0 starter prompt and wants specific architecture and process patterns retrofitted — pulled from the accumulated behavioral evolution of a mature, months-old ship, generalized so they apply to any mythos.

**How to use:** Same as the v2 series — pick the update(s) you want, paste that update's prompt into your existing ship's project. Each is self-contained and locates the right files in your own ship regardless of naming. Apply in any order.

**Not included:** anything too specific to one ship's actual tool stack to generalize (a particular chat platform's thread mechanics, a particular time-tracking tool, financial-disclosure rules for one company, etc.). This series is the architecture and process patterns that generalize across any ship.

---

## Update 1 of 8 — Boot behavior must live in the boot

**What it does:** Closes a subtle but common gap: a behavior written into a crew member's spec file doesn't run automatically — specs are inert until dispatched. Anything that must happen before your ship's first response has to live in the main instruction file itself.

```
I want to audit my ship for behaviors that were written into a crew member's spec file but were actually meant to happen automatically, every session, before any dispatch occurs. Those don't work — a crew spec is inert until something dispatches it; only the main instruction file (and the boot-identity spec it points to) runs unconditionally at session start.

1. Read my main instruction file and my boot-identity spec (the Ship/Computer/Oracle/whatever-I-named-it file) and list every behavior that's supposed to happen automatically at session open — silent reads, alerts, standing checks, anything that isn't a response to a specific user request.

2. Now check every other crew member's spec file for behaviors described in language like "at every session," "always," "on boot," or "automatically" that aren't actually referenced anywhere in the main instruction file's boot sequence.

3. For anything you find in step 2: either (a) move the trigger into the main instruction file's boot sequence, explicitly naming which crew member's logic runs and when, or (b) if it's not actually meant to be automatic, correct the language in that crew member's spec so it's clear it only runs when dispatched.

4. State this as a standing rule somewhere visible (main instruction file or boot spec): "Any behavior required before the first response must live in the main instruction file or the files it explicitly reads at boot. Crew specs are inert until dispatched."

Report what you found before changing anything — I want to see the list of gaps first.
```

---

## Update 2 of 8 — File-based spine over cloud memory API

**What it does:** Documents (or re-confirms) a specific architectural tradeoff: for anything read at high frequency — every session open — plain files on disk beat a cloud memory store or API, even though cloud stores sound more "proper."

```
I want you to evaluate whether my ship's memory/spine should stay file-based or move to a cloud memory API, and document the decision either way so it doesn't get re-litigated later.

1. Identify what my current memory setup actually is — plain markdown/text files on disk, a cloud memory API, a database, or some mix.

2. Reason through the tradeoff explicitly: files read at every session open benefit from being local (no network latency, no API cost per read, works offline, trivially diffable/greppable). A cloud memory store adds cost and latency to something that happens dozens of times a week, and most cloud memory products are optimized for semantic search over large corpora, not for "read the same five files every single time."

3. If I already have a sync/backup mechanism for my files (a synced drive folder, git, etc.), note that this already solves the durability problem a cloud store would solve — so the cloud store isn't buying me anything my current setup doesn't already have.

4. Write your recommendation into a short decision note in my spine (a lessons log if I have one — see Update 5 — otherwise a new short file). State the decision and the reasoning in 3-4 sentences so future-me (or future-you) doesn't reopen this question without new information.

Tell me your recommendation and reasoning before writing anything.
```

---

## Update 3 of 8 — Distill-once-route-many

**What it does:** If any crew member processes external sources (meeting transcripts, documents, long threads), this stops multiple officers from each independently re-processing the same source — one distillation, tagged by domain, routed to whoever needs which piece.

```
I want to check whether any of my crew members are redundantly re-processing the same external source — the same meeting transcript, document, or thread — separately, each doing their own pass over the raw material.

1. Find any crew member(s) whose job involves reading external sources (meeting notes, transcripts, documents, long message threads) and extracting information for different purposes.

2. If two or more crew members would plausibly need different pieces of the same source (e.g., one needs the technical details, another needs the relationship/sentiment signals, another needs action items), check whether each of them currently does its own independent read of the raw source.

3. If they do: redesign so there's exactly one distillation pass per source. That pass reads the raw material once and produces a single structured output with clearly domain-tagged sections (e.g., "## Technical," "## Relationship," "## Action Items"). Other crew members read the relevant section of the distillation, not the raw source again.

4. Decide who owns the distillation step — usually whichever crew member is positioned as the general intake/librarian role, if I have one; otherwise pick the most central reader.

5. Update the relevant crew specs to reflect: "read the distillation, not the raw source" for anyone who was previously doing their own pass.

Show me which crew members were duplicating work before you change any specs.
```

---

## Update 4 of 8 — Connector cookbook pattern

**What it does:** If your ship talks to several external tools (calendar, email, chat, CRM, docs), this consolidates each tool's integration behavior into one named, numbered reference file instead of scattering that logic across every crew spec that touches it.

```
I want to consolidate how my ship uses each external tool/connector into dedicated reference files, instead of having the same tool-specific logic re-explained or duplicated across multiple crew specs.

1. List every external tool/connector my ship actually uses (calendar, email, a chat platform, a CRM, a docs tool, whatever's real for me) and which crew members touch each one.

2. For each tool used by more than one crew member, or with more than one distinct usage pattern, create one reference file (e.g., spine/[tool]-patterns.md) that documents each distinct way it's used as a numbered "Pipeline": what triggers it, what it reads or writes, any gotchas or formatting requirements specific to that tool, and any tool-specific footguns already discovered in past sessions.

3. Update every crew spec that touches that tool to reference the pipeline number instead of re-explaining the mechanics inline (e.g., "uses Pipeline 3 from calendar-patterns.md for daily lookahead" instead of restating the calendar-query logic in the crew spec itself).

4. This is about eliminating duplication and drift, not adding process for its own sake — only do this for tools actually used by multiple crew members or in multiple distinct ways. A tool used once, one way, by one crew member doesn't need its own cookbook file.

Show me the proposed file structure before you start moving logic out of the crew specs.
```

---

## Update 5 of 8 — Running numbered lessons log

**What it does:** Adds a distinct, append-only log for durable architectural decisions and lessons — separate from your day-to-day session spine, which is narrative and gets long. This is the place hard-won "we tried X, it broke, do Y instead" knowledge lives permanently.

```
I want a dedicated lessons log — a place for durable architectural decisions and hard-won lessons that's separate from my regular session-by-session spine, because that file is narrative and grows long, and decisions get buried in it.

1. Create a new file (e.g., spine/lessons.md) with a simple format: sequential IDs (L-001, L-002, ...), each with a one-line statement of the lesson/decision, and 1-3 sentences of why it matters or what happens if you ignore it.

2. Scan my existing session spine for anything that reads like a durable decision rather than a day's events — things like "we decided X approach over Y because Z," or a correction to how the system should behave going forward, not just what happened on a given day. Pull candidates out and propose them as lesson entries; don't move anything without showing me first.

3. Going forward, tell me when to add an entry here versus just noting something in the regular session spine: if it's a decision or lesson that should shape *future* behavior across many sessions, it goes in the lessons log. If it's just what happened today, it stays in the session spine.

4. Note in your main instruction file or boot spec that the lessons log exists and is a good place to check when reasoning about "why do we do it this way" questions — but it does NOT need to be read at every boot; it's a reference, not a boot-read file.

Show me the candidate lessons pulled from my existing spine before finalizing the new file.
```

---

## Update 6 of 8 — Standing recurring board items

**What it does:** If you have a fixed recurring obligation (a weekly review, a regular report, anything on a schedule regardless of what else is going on), this makes sure it surfaces automatically instead of depending on someone remembering to add it.

```
I have at least one recurring obligation that should show up on my board automatically, on schedule, regardless of my current workload or posture — not something that has to be manually re-added each time. Help me encode it as a standing item.

1. Ask me what the recurring obligation is (or I'll tell you): what it is, how often (daily/weekly/monthly), and any specific day/time it's tied to.

2. Add a rule to my ship's boot-identity spec (in the board-item shapes / prioritization section) stating: on [the relevant day/time], this item surfaces on the board automatically, regardless of posture mode — it does not get filtered out even in a "low energy, 2-3 items only" mode, because it's non-negotiable.

3. If I have more than one such recurring item, make this a general pattern rather than a one-off special case: a small table or list of "standing items" with their trigger condition (day/date/recurrence) and urgency, checked at every board surface alongside the regular dynamic items.

4. Make sure this doesn't turn into nagging — if I've already handled it this cycle, it shouldn't keep surfacing until the next cycle comes around. Ask me how completion should be tracked (a checkbox in a file, a phrase I say, whatever's lightweight) if it isn't obvious.

Confirm the recurring item(s) and trigger conditions with me before writing the rule.
```

---

## Update 7 of 8 — External intake-folder check

**What it does:** If you have a shared drop location (a synced folder, a shared drive) where things land for your ship to process, this adds a boot-time check plus a "processed" convention so nothing gets picked up twice.

```
I have an external location — [DESCRIBE IT: a synced folder, a shared drive folder, an inbox, wherever things land for me to process] — where new items show up that I want my ship to notice and help me process. Set up a check-and-file pattern for it.

1. Confirm what access you actually have to this location in this environment (filesystem access, a connector/MCP tool, etc.). If you don't have access, tell me what's needed.

2. Add a step to my ship's boot sequence: check this location for anything new since the last check. Surface what's new in the boot alerts (a one-line count is enough, not a full dump) so I know something's waiting without having to go look myself.

3. Set up a "Processed" subfolder (or equivalent marking mechanism) within that location. After anything from the intake location has been read and acted on (discussed, filed, added to the board), move it there — so it's never picked up as "new" again on a future boot check.

4. Decide with me: does landing something in this folder mean "process it automatically" or "flag it and wait for me to say go"? Default to flagging and waiting unless I tell you otherwise — don't take action on intake items without confirmation.

Tell me what you found in the location right now, if anything, before setting up the automatic check.
```

---

## Update 8 of 8 — No heavy dispatches for answerable questions

**What it does:** A cost-efficiency guardrail: stops your ship from spinning up an expensive research pass or specialized skill for something that's already answerable from context or general knowledge.

```
I want a standing rule that stops my ship from reaching for expensive tools — a big research pass, a specialized multi-step skill, a strong-model sub-agent — when a question is actually answerable directly, from context already loaded or from general knowledge.

1. Add this rule to my main instruction file: before dispatching any token-heavy skill or research pass, first check whether the question is answerable directly — from what's already in context this session, from the spine, or from general knowledge that doesn't require a live lookup. If it is, just answer it inline.

2. Be specific about what counts as "needs the heavy path": anything requiring live/current data (today's calendar, a live database, a real-time status), anything requiring a source I haven't already loaded this session, or anything where I've explicitly asked for a thorough/verified pass.

3. Be specific about what does NOT need the heavy path: general knowledge questions, clarifying questions about my own system's architecture (which should be answerable from the specs already on disk), and anything where the answer is already sitting in context from earlier in the conversation.

4. This pairs with (but is distinct from) any existing "confirm before token spend" rule I already have — that rule gates spend once you've decided something needs a heavy dispatch; this rule is about not deciding that in the first place when it isn't warranted.

Show me the rule as you'd write it before adding it to my instruction file.
```

---

*Series 2 of the manual updates. Covers architecture and process patterns generalized from a mature, months-old ship's behavioral evolution — everything too specific to one ship's exact tool stack was left out.*
