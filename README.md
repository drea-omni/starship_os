# Starship OS

**The prompt that turns Claude into mission control.**

Starship OS is a bootstrapping prompt that builds a personal AI operating system — a named crew of specialist sub-agents, an ambient ship intelligence that runs your daily board, and a memory spine that persists context across sessions. You run the prompt once, it interviews you, designs a crew around your actual life, and generates every file the system needs. When it's done, your ship boots up and you start using it immediately.

---

## What you get

- **A Ship** — the ambient intelligence you talk to every session. Runs your boot menu, daily board, and session-close ritual. Holds the whole picture; serves a slice at a time, shaped to where you are.
- **An Orchestrator** — the router. Reads context, dispatches the right crew member, presents outcomes. Never does the work itself.
- **A Crew** — specialist sub-agents derived from your interview. Your day decides who's on your ship. A solo founder gets different crew than a household manager or a novelist.
- **A Spine** — plain markdown files that persist memory across sessions. What was done, what was decided, what's still open. Ground truth.

---

## How to use it

### Option 1 — Use the prompt directly

1. Open a new **Claude project** (claude.ai → Projects → New project)
2. Open `starter-prompt-opus.md` and copy everything between `=== BEGIN PROMPT ===` and `=== END PROMPT ===`
3. Paste it as your **project instructions** (the "Custom instructions" field in project settings)
4. Start a conversation in the project — Claude will greet you and begin the interview
5. Run on **Claude Opus** for best results — the prompt asks the model to hold an entire system architecture and reproduce it precisely

### Option 2 — Use the desktop app

The desktop app bundles the prompt and launches it with one click.

**[Download for Mac (Apple Silicon) →](#)** *(link coming soon)*

1. Download the `.dmg`, open it, drag **Starship Omni OS** to Applications
2. Open the app, enter your Anthropic API key
3. Click **LAUNCH STARTER** — the prompt is bundled, no paste required

> **Note:** The app requires an [Anthropic API key](https://console.anthropic.com/). Usage is billed to your account.

---

## The architecture (the fixed part)

Every ship built from this prompt has the same bones:

```
Main-thread Claude = The Ship (boots every session, runs the board)
                   ↕ switches into
             The Orchestrator (routes crew work)
                   ↓ dispatches
              Crew sub-agents (do the actual work)
                   ↓ write to
              The Spine (plain markdown memory)
```

The **only two things that vary** between ships: the naming mythos you pick (Star Trek, Roman mythology, SpongeBob, whatever you want) and the crew composition (derived from the interview — your day decides who's on board). Everything else — the boot menu, the board, the posture modes, the session-close ritual, the spine format — reproduces identically.

---

## The crew taxonomy

The interview pulls from a role palette — not a checklist. A work-heavy life and a home-focused life call for completely different crews:

| Work example | Home / creative example |
|---|---|
| Build-Path Architect (client engagements) | Steward (meal planning, household logistics) |
| Deal Intelligence (pipeline) | Chronicle Keeper (schedules, records, appointments) |
| Librarian / Knowledge Keeper (product updates, feeds) | Muse (creative spark, research rabbit holes) |
| People Officer (team, onboarding) | Quartermaster (logistics, supplies, errands) |
| The Forge (builds artifacts in your tools) | The Forge (same — builds things) |

Crew size is 3–11 beyond the Ship and Orchestrator. Don't pad — a role with no real work is dead weight.

---

## The wrap ritual

At the end of every session, say your ship's close phrase (e.g., `Computer, end program`). The Ship synthesizes everything that happened, writes a permanent entry to the session spine, and confirms what was logged. Without the wrap, context from the session won't carry forward.

---

## Files in this repo

```
starter-prompt-opus.md        # The prompt — copy this
apps/
  launch-page/
    index.html                # The launch page (GitHub Pages)
    build.py                  # Regenerates the page from the prompt
  starship-desktop/
    src/                      # Electron app source
    assets/                   # App icon
    package.json
```

---

## Built by

[@drea-omni](https://github.com/drea-omni) — Managing Architect, [Omni Analytics](https://omni.co)

---

*Starship OS is a pattern, not a product. Build your own ship.*
