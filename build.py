#!/usr/bin/env python3
"""Generate the Starship OS launch page from the canonical Opus starter prompt.

Single source of truth: /starter-prompt-opus.md (the PROMPT body between the
=== BEGIN PROMPT === / === END PROMPT === markers). Re-run after editing that file.
"""
import pathlib
import html

ROOT = pathlib.Path(__file__).resolve().parent  # repo root (script lives here now)
SRC = ROOT / "starter-prompt-opus.md"
OUT = ROOT / "index.html"

lines = SRC.read_text().splitlines()
b = next(i for i, l in enumerate(lines) if l.strip() == "=== BEGIN PROMPT ===")
e = next(i for i, l in enumerate(lines) if l.strip() == "=== END PROMPT ===")
prompt = "\n".join(lines[b + 1:e]).strip("\n")
prompt_escaped = html.escape(prompt)              # &, <, > safe inside <code>
approx_tokens = int(round(len(prompt) / 4, -2))   # ~chars/4, nearest 100

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Starship OS &mdash; Your crew starts with one prompt</title>
  <meta name="description" content="An open prompt that boots a personal AI operating system. It interviews you, designs a crew that fits your life, names it after a universe you pick, and builds the whole system &mdash; boot menu, officers, and a memory spine that survives every rebuild.">

  <!-- OG / Twitter -->
  <meta property="og:title" content="Starship OS &mdash; Your crew starts with one prompt">
  <meta property="og:description" content="One prompt boots a personal AI crew that builds itself around your actual day and rides on a memory spine that survives every rebuild.">
  <meta property="og:type" content="website">
  <!-- TODO: set your published URL + a share image -->
  <meta property="og:url" content="https://your-username.github.io/starship-os/">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Starship OS &mdash; Your crew starts with one prompt">
  <meta name="twitter:description" content="One prompt boots a personal AI crew that builds itself around your actual day.">

  <!-- Fonts: Antonio (LCARS-flavored display), Inter (body), Share Tech Mono (code) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Antonio:wght@500;600;700&family=Inter:wght@400;500;600&family=Share+Tech+Mono&display=swap" rel="stylesheet">

  <!-- Tailwind Play CDN (matches the reference; keeps this a single file) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            display: ['Antonio', 'system-ui', 'sans-serif'],
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['Share Tech Mono', 'ui-monospace', 'monospace'],
          },
        },
      },
    }
  </script>

  <style>
    html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
    .hero-glow {
      background:
        radial-gradient(1200px 400px at 70% -10%, rgba(255,46,136,0.18), transparent 60%),
        radial-gradient(900px 500px at 15% 0%, rgba(56,128,255,0.20), transparent 55%);
    }
    .starfield {
      background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(230,236,245,0.7), transparent),
        radial-gradient(1px 1px at 60% 70%, rgba(230,236,245,0.5), transparent),
        radial-gradient(1px 1px at 80% 20%, rgba(255,46,136,0.6), transparent),
        radial-gradient(1px 1px at 40% 80%, rgba(230,236,245,0.4), transparent),
        radial-gradient(1px 1px at 90% 60%, rgba(159,179,210,0.5), transparent);
    }
    .code-block-body::-webkit-scrollbar { width: 7px; height: 7px; }
    .code-block-body::-webkit-scrollbar-track { background: transparent; }
    .code-block-body::-webkit-scrollbar-thumb { background: #2A4A74; border-radius: 4px; }
    .code-block-body::-webkit-scrollbar-thumb:hover { background: #3D6299; }
    .lcars-pill { border-radius: 9999px; }
  </style>
</head>
<body class="bg-[#091324] text-[#E6ECF5] font-sans">

  <!-- Hero backdrop -->
  <div class="relative w-full hero-glow" style="max-height: 420px; overflow: hidden;">
    <div class="starfield w-full" style="height: 420px; opacity: 0.5;"></div>
    <div class="absolute inset-0" style="background: linear-gradient(to bottom, transparent 45%, #091324 100%);"></div>
  </div>

  <div class="max-w-[720px] mx-auto px-6 md:px-8 lg:px-0" style="margin-top: -220px; position: relative; z-index: 10;">

    <!-- Hero -->
    <section class="pt-12 md:pt-16 pb-20 md:pb-28">
      <div class="flex items-center gap-3 mb-7">
        <span class="lcars-pill bg-[#FF2E88] h-3 w-10 inline-block"></span>
        <p class="font-mono text-xs uppercase text-[#7E97B8] tracking-[0.18em]">Opus edition &middot; Open source</p>
      </div>
      <h1 class="font-display text-5xl md:text-[64px] font-bold text-[#E6ECF5] tracking-[-0.01em] leading-[1.02] mb-6 uppercase">Your personal OS starts with one prompt and a crew.</h1>
      <p class="text-lg text-[#9FB3D2] max-w-[560px] mb-10">A self-contained prompt that interviews you, designs an AI crew that fits your actual life, names it after a universe you pick, and builds the whole operating system &mdash; boot menu, officers, and a memory spine that survives every rebuild.</p>
      <div class="flex flex-col sm:flex-row gap-4">
        <button id="hero-copy-btn" class="bg-[#FF2E88] text-[#091324] text-[15px] font-semibold px-6 py-3 rounded-lg hover:bg-[#FF5BA3] active:bg-[#E61E73] active:scale-[0.98] transition-all cursor-pointer">Copy the prompt</button>
        <!-- TODO: point this at your repo, or delete if not publishing the source -->
        <a href="#" class="text-[#9FB3D2] hover:text-[#E6ECF5] hover:underline text-[15px] font-medium px-6 py-3 transition-colors">View on GitHub</a>
      </div>
    </section>

    <!-- Prompt -->
    <section class="pb-20 md:pb-28">
      <div class="rounded-xl border border-[#1B3252]" style="box-shadow: 0 0 0 1px rgba(56,128,255,0.12), 0 4px 28px rgba(0,0,0,0.5);">
        <div class="bg-[#0C1B30] rounded-t-xl flex items-center justify-between px-5 py-3">
          <span class="font-mono text-sm text-[#9FB3D2]">starter-prompt.md &mdash; Opus edition</span>
          <button id="code-copy-btn" class="bg-transparent text-[#7E97B8] font-mono text-sm px-3 py-1.5 border border-[#1B3252] rounded hover:bg-[#0C1B30] hover:text-[#9FB3D2] hover:border-[#2F5A8C] transition-all cursor-pointer">Copy</button>
        </div>
        <div class="code-block-body bg-[#070F1E] rounded-b-xl overflow-auto" style="max-height: 480px; padding: 24px 20px;">
          <pre class="font-mono text-[12.5px] text-[#CBD7EC] leading-relaxed whitespace-pre-wrap break-words"><code id="prompt-content">__PROMPT__</code></pre>
        </div>
      </div>
      <p class="text-sm text-[#7E97B8] text-center mt-6">~__TOKENS__ tokens. Paste it into Claude Code (or any AI with filesystem access) and start building.</p>
    </section>

    <!-- What you get -->
    <section class="pb-20 md:pb-28">
      <h2 class="font-display text-4xl font-semibold text-[#E6ECF5] mb-12 uppercase tracking-[-0.01em]">What you get</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-y-12 gap-x-10">
        <div>
          <h3 class="font-display text-2xl font-semibold text-[#E6ECF5] mb-3 uppercase">The Ship</h3>
          <p class="text-base text-[#9FB3D2] max-w-[320px]">The ambient intelligence you talk to first, every session. It boots to a menu, holds your whole board, and serves it back at your current energy. Never a character &mdash; just the system, always on.</p>
        </div>
        <div>
          <h3 class="font-display text-2xl font-semibold text-[#E6ECF5] mb-3 uppercase">The Orchestrator</h3>
          <p class="text-base text-[#9FB3D2] max-w-[320px]">A captain that routes every request to the right crew member and returns the result. You talk to the ship; it switches into the orchestrator to dispatch work. It never does the work itself.</p>
        </div>
        <div>
          <h3 class="font-display text-2xl font-semibold text-[#E6ECF5] mb-3 uppercase">A crew from your day</h3>
          <p class="text-base text-[#9FB3D2] max-w-[320px]">No fixed roster. A short interview reads your actual day and derives only the officers you need &mdash; a build-path architect, a researcher, a librarian, a forge. The day reveals the ship.</p>
        </div>
        <div>
          <h3 class="font-display text-2xl font-semibold text-[#E6ECF5] mb-3 uppercase">A memory spine</h3>
          <p class="text-base text-[#9FB3D2] max-w-[320px]">Plain markdown that persists across sessions: a session log, a dispatch ledger, a parked-questions register, and an operator profile. Ground truth. Your context never resets to zero.</p>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="pb-20 md:pb-28">
      <h2 class="font-display text-4xl font-semibold text-[#E6ECF5] mb-12 uppercase tracking-[-0.01em]">How it works</h2>
      <div class="flex flex-col gap-10">
        <div class="flex flex-row gap-6">
          <span class="font-mono text-xs text-[#FF2E88] pt-1 shrink-0">01</span>
          <div>
            <h3 class="font-display text-lg font-semibold text-[#E6ECF5] mb-2 uppercase tracking-wide">Create a folder</h3>
            <code class="font-mono text-sm text-[#9FD3DC] bg-[#0C1B30] px-2.5 py-1 rounded">mkdir mystarship &amp;&amp; cd mystarship</code>
          </div>
        </div>
        <div class="flex flex-row gap-6">
          <span class="font-mono text-xs text-[#FF2E88] pt-1 shrink-0">02</span>
          <div>
            <h3 class="font-display text-lg font-semibold text-[#E6ECF5] mb-2 uppercase tracking-wide">Open your AI tool</h3>
            <p class="text-base text-[#9FB3D2]">Claude Code, or any AI with filesystem access. Run it on Opus &mdash; this prompt holds a whole architecture in its head.</p>
          </div>
        </div>
        <div class="flex flex-row gap-6">
          <span class="font-mono text-xs text-[#FF2E88] pt-1 shrink-0">03</span>
          <div>
            <h3 class="font-display text-lg font-semibold text-[#E6ECF5] mb-2 uppercase tracking-wide">Paste the prompt</h3>
            <p class="text-base text-[#9FB3D2]">It runs the interview, designs your crew, builds every file, and boots your ship. The next message just works.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-[#1B3252] py-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <p class="text-sm text-[#7E97B8]">Built by <span class="text-[#9FB3D2]">Drea</span></p>
      <div class="flex items-center gap-2 text-sm text-[#7E97B8]">
        <span class="text-[#9FB3D2]">Starship OS</span>
        <span>/</span>
        <span>MIT License</span>
      </div>
    </footer>

  </div>

  <script>
    const promptText = document.getElementById('prompt-content').textContent;

    function flashCopy(btn, doneText, addClasses, removeClasses) {
      navigator.clipboard.writeText(promptText).then(function () {
        const original = btn.textContent;
        btn.textContent = doneText;
        removeClasses.forEach(function (c) { btn.classList.remove(c); });
        addClasses.forEach(function (c) { btn.classList.add(c); });
        setTimeout(function () {
          btn.textContent = original;
          addClasses.forEach(function (c) { btn.classList.remove(c); });
          removeClasses.forEach(function (c) { btn.classList.add(c); });
        }, 2000);
      });
    }

    document.getElementById('hero-copy-btn').addEventListener('click', function () {
      flashCopy(this, 'Copied!',
        ['bg-green-600', 'text-white'],
        ['bg-[#FF2E88]', 'hover:bg-[#FF5BA3]', 'active:bg-[#E61E73]', 'text-[#091324]']);
    });
    document.getElementById('code-copy-btn').addEventListener('click', function () {
      flashCopy(this, 'Copied',
        ['text-green-400'],
        ['text-[#7E97B8]']);
    });
  </script>
</body>
</html>
'''

out = TEMPLATE.replace("__PROMPT__", prompt_escaped).replace("__TOKENS__", f"{approx_tokens:,}")
OUT.write_text(out)
print(f"wrote {OUT}")
print(f"  page: {len(out):,} bytes | prompt: {len(prompt):,} chars | ~{approx_tokens:,} tokens")
