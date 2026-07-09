#!/usr/bin/env python3
"""Generate updates.html from manual-updates-v2.md.
Re-run after editing that file."""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "manual-updates-v2.md"
OUT = ROOT / "updates.html"

content = SRC.read_text()
blocks = re.findall(
    r'## (Update \d of \d) — (.+?)\n\n\*\*What it does:\*\* (.+?)\n\n```\n(.*?)\n```',
    content, re.DOTALL
)

cards = []
for i, (num, title, desc, body) in enumerate(blocks, start=1):
    body_escaped = html.escape(body.strip())
    desc_escaped = html.escape(desc.strip())
    title_escaped = html.escape(title.strip())
    cards.append(f'''
        <div class="rounded-xl border border-[#1B3252] mb-8" style="box-shadow: 0 0 0 1px rgba(56,128,255,0.12), 0 4px 28px rgba(0,0,0,0.5);">
          <div class="px-5 py-4 border-b border-[#1B3252]">
            <p class="font-mono text-xs uppercase text-[#FF2E88] tracking-[0.14em] mb-2">{num}</p>
            <h3 class="font-display text-xl font-semibold text-[#E6ECF5] mb-2 uppercase">{title_escaped}</h3>
            <p class="text-sm text-[#9FB3D2]">{desc_escaped}</p>
          </div>
          <div class="bg-[#0C1B30] flex items-center justify-between px-5 py-3">
            <span class="font-mono text-sm text-[#9FB3D2]">paste this prompt</span>
            <button class="update-copy-btn bg-transparent text-[#7E97B8] font-mono text-sm px-3 py-1.5 border border-[#1B3252] rounded hover:bg-[#0C1B30] hover:text-[#9FB3D2] hover:border-[#2F5A8C] transition-all cursor-pointer" data-target="update-prompt-{i}">Copy</button>
          </div>
          <div class="code-block-body bg-[#070F1E] rounded-b-xl overflow-auto" style="max-height: 360px; padding: 20px;">
            <pre class="font-mono text-[12px] text-[#CBD7EC] leading-relaxed whitespace-pre-wrap break-words"><code id="update-prompt-{i}">{body_escaped}</code></pre>
          </div>
        </div>''')

cards_html = "\n".join(cards)

TEMPLATE = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Starship OS &mdash; Manual Updates for existing ships</title>
  <meta name="description" content="Paste-able upgrade prompts for anyone who already built a Starship OS and wants specific architecture improvements retrofitted, without rebuilding from scratch.">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Antonio:wght@500;600;700&family=Inter:wght@400;500;600&family=Share+Tech+Mono&display=swap" rel="stylesheet">

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            display: ['Antonio', 'system-ui', 'sans-serif'],
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['Share Tech Mono', 'ui-monospace', 'monospace'],
          }},
        }},
      }},
    }}
  </script>

  <style>
    html {{ -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    .hero-glow {{
      background:
        radial-gradient(1200px 400px at 70% -10%, rgba(255,46,136,0.14), transparent 60%),
        radial-gradient(900px 500px at 15% 0%, rgba(56,128,255,0.16), transparent 55%);
    }}
    .code-block-body::-webkit-scrollbar {{ width: 7px; height: 7px; }}
    .code-block-body::-webkit-scrollbar-track {{ background: transparent; }}
    .code-block-body::-webkit-scrollbar-thumb {{ background: #2A4A74; border-radius: 4px; }}
    .code-block-body::-webkit-scrollbar-thumb:hover {{ background: #3D6299; }}
    .lcars-pill {{ border-radius: 9999px; }}
  </style>
</head>
<body class="bg-[#091324] text-[#E6ECF5] font-sans">

  <div class="relative w-full hero-glow" style="max-height: 220px; overflow: hidden;">
    <div class="absolute inset-0" style="background: linear-gradient(to bottom, transparent 30%, #091324 100%);"></div>
  </div>

  <div class="max-w-[840px] mx-auto px-6 md:px-8 lg:px-0" style="margin-top: -140px; position: relative; z-index: 10;">

    <!-- Header -->
    <section class="pt-12 pb-14">
      <a href="index.html" class="font-mono text-xs uppercase text-[#7E97B8] hover:text-[#9FB3D2] tracking-[0.14em] transition-colors">&larr; Back to Starship OS</a>
      <div class="flex items-center gap-3 mt-6 mb-6">
        <span class="lcars-pill bg-[#FF2E88] h-3 w-10 inline-block"></span>
        <p class="font-mono text-xs uppercase text-[#7E97B8] tracking-[0.18em]">For existing ships &middot; not a fresh build</p>
      </div>
      <h1 class="font-display text-4xl md:text-5xl font-bold text-[#E6ECF5] tracking-[-0.01em] leading-[1.05] mb-5 uppercase">Manual updates</h1>
      <p class="text-lg text-[#9FB3D2] max-w-[620px]">Already built a ship from the starter prompt? These are standalone, paste-able upgrade prompts &mdash; apply just the ones you want, in any order, without rerunning the full interview. Each one figures out your ship's actual file names and mythos on its own.</p>
    </section>

    <!-- v2 series -->
    <section class="pb-16">
      <div class="flex items-baseline justify-between mb-2">
        <h2 class="font-display text-2xl font-semibold text-[#E6ECF5] uppercase tracking-[-0.01em]">Series: v2 architecture</h2>
        <span class="font-mono text-xs text-[#7E97B8]">6 updates</span>
      </div>
      <p class="text-sm text-[#9FB3D2] mb-8 max-w-[620px]">Core-architecture patterns folded into the v2 starter prompt: spine index/detail splitting, external task-board sync, entity spine files, a standing status index, two-tier context awareness, and an automation-mechanism guardrail. None depend on each other.</p>

      {cards_html}
    </section>

    <!-- Coming soon -->
    <section class="pb-20">
      <div class="rounded-xl border border-dashed border-[#1B3252] px-6 py-8">
        <p class="font-mono text-xs uppercase text-[#7E97B8] tracking-[0.14em] mb-3">Coming soon</p>
        <h3 class="font-display text-xl font-semibold text-[#E6ECF5] mb-3 uppercase">Series: v1.0 &rarr; v1.1 behavioral evolution</h3>
        <p class="text-sm text-[#9FB3D2] max-w-[600px]">A second, larger series covering the full behavioral evolution beyond core architecture &mdash; new crew roles, connector protocols, standing rules, and board-display conventions. These are also being folded back into the starter prompt itself where they generalize. Check back for updates.</p>
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
    document.querySelectorAll('.update-copy-btn').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        const target = document.getElementById(btn.dataset.target);
        navigator.clipboard.writeText(target.textContent).then(function () {{
          const original = btn.textContent;
          btn.textContent = 'Copied';
          btn.classList.add('text-green-400');
          btn.classList.remove('text-[#7E97B8]');
          setTimeout(function () {{
            btn.textContent = original;
            btn.classList.remove('text-green-400');
            btn.classList.add('text-[#7E97B8]');
          }}, 2000);
        }});
      }});
    }});
  </script>
</body>
</html>
'''

OUT.write_text(TEMPLATE)
print(f"wrote {OUT} ({len(TEMPLATE)} bytes, {len(cards)} update cards)")
