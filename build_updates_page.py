#!/usr/bin/env python3
"""Generate updates.html from the manual-updates-*.md series files.
Re-run after editing any of those files."""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "updates.html"

# Each series: (source file, id prefix for DOM/copy targets, tab label, series title, series subtitle)
SERIES = [
    {
        "src": ROOT / "manual-updates-v2.md",
        "prefix": "v2",
        "tab": "V2 Architecture",
        "title": "Series: v2 architecture",
        "subtitle": "Core-architecture patterns folded into the v2 starter prompt: spine index/detail splitting, external task-board sync, entity spine files, a standing status index, two-tier context awareness, and an automation-mechanism guardrail. None depend on each other.",
    },
    {
        "src": ROOT / "manual-updates-v1.md",
        "prefix": "v1",
        "tab": "V1.0 → V1.1 Architecture",
        "title": "Series: v1.0 → v1.1 architecture",
        "subtitle": "Architecture and process patterns generalized from a mature, months-old ship's behavioral evolution — boot-behavior placement, file-based memory, connector patterns, a lessons log, standing board items, an intake-folder check, and a cost-efficiency guardrail. Anything too specific to one ship's exact tool stack was left out.",
    },
]


def parse_series(src_path):
    content = src_path.read_text()
    blocks = re.findall(
        r'## (Update \d of \d) — (.+?)\n\n\*\*What it does:\*\* (.+?)\n\n```\n(.*?)\n```',
        content, re.DOTALL
    )
    return blocks


def render_series(series, tab_index):
    blocks = parse_series(series["src"])
    prefix = series["prefix"]
    cards = []
    all_ids = []
    for i, (num, title, desc, body) in enumerate(blocks, start=1):
        body_escaped = html.escape(body.strip())
        desc_escaped = html.escape(desc.strip())
        title_escaped = html.escape(title.strip())
        target_id = f'update-prompt-{prefix}-{i}'
        all_ids.append(target_id)
        panel_id = f'update-panel-{prefix}-{i}'
        cards.append(f'''
        <div class="rounded-xl border border-[#1B3252] mb-5" style="box-shadow: 0 0 0 1px rgba(56,128,255,0.12), 0 4px 28px rgba(0,0,0,0.5);">
          <button class="update-toggle w-full flex items-center justify-between gap-4 px-5 py-4 text-left cursor-pointer" data-panel="{panel_id}" aria-expanded="false">
            <div class="min-w-0">
              <p class="font-mono text-xs uppercase text-[#FF2E88] tracking-[0.14em] mb-1.5">{num}</p>
              <h3 class="font-display text-lg font-semibold text-[#E6ECF5] uppercase truncate">{title_escaped}</h3>
              <p class="text-sm text-[#9FB3D2] mt-1">{desc_escaped}</p>
            </div>
            <span class="update-chevron font-mono text-[#7E97B8] text-lg shrink-0 transition-transform duration-200">&#9656;</span>
          </button>
          <div id="{panel_id}" class="update-panel hidden">
            <div class="bg-[#0C1B30] flex items-center justify-between px-5 py-3 border-t border-[#1B3252]">
              <span class="font-mono text-sm text-[#9FB3D2]">paste this prompt</span>
              <button class="update-copy-btn bg-transparent text-[#7E97B8] font-mono text-sm px-3 py-1.5 border border-[#1B3252] rounded hover:bg-[#0C1B30] hover:text-[#9FB3D2] hover:border-[#2F5A8C] transition-all cursor-pointer" data-target="{target_id}">Copy</button>
            </div>
            <div class="code-block-body bg-[#070F1E] rounded-b-xl overflow-auto" style="max-height: 360px; padding: 20px;">
              <pre class="font-mono text-[12px] text-[#CBD7EC] leading-relaxed whitespace-pre-wrap break-words"><code id="{target_id}">{body_escaped}</code></pre>
            </div>
          </div>
        </div>''')

    cards_html = "\n".join(cards)
    ids_attr = ",".join(all_ids)
    hidden_class = "" if tab_index == 0 else " hidden"
    section_html = f'''
    <section id="tab-panel-{prefix}" class="tab-panel pb-16{hidden_class}" data-tab="{prefix}">
      <div class="flex items-baseline justify-between mb-2 gap-4 flex-wrap">
        <h2 class="font-display text-2xl font-semibold text-[#E6ECF5] uppercase tracking-[-0.01em]">{series["title"]}</h2>
        <div class="flex items-center gap-3">
          <span class="font-mono text-xs text-[#7E97B8]">{len(cards)} updates</span>
          <button class="copy-all-btn bg-transparent text-[#9FD3DC] font-mono text-xs px-3 py-1.5 border border-[#1B3252] rounded hover:bg-[#0C1B30] hover:border-[#2F5A8C] transition-all cursor-pointer uppercase tracking-wide" data-ids="{ids_attr}" data-label="Copy all {len(cards)}">Copy all {len(cards)}</button>
        </div>
      </div>
      <p class="text-sm text-[#9FB3D2] mb-8 max-w-[620px]">{series["subtitle"]}</p>

      {cards_html}
    </section>'''
    return section_html, len(cards)


tab_buttons = []
sections = []
total_cards = 0
for idx, series in enumerate(SERIES):
    active = idx == 0
    tab_buttons.append(
        f'<button class="tab-btn font-mono text-xs uppercase tracking-[0.12em] px-4 py-2.5 rounded-lg transition-all cursor-pointer{" bg-[#FF2E88] text-[#091324] font-semibold" if active else " text-[#9FB3D2] border border-[#1B3252] hover:border-[#2F5A8C] hover:text-[#E6ECF5]"}" data-tab="{series["prefix"]}">{series["tab"]}</button>'
    )
    section_html, count = render_series(series, idx)
    sections.append(section_html)
    total_cards += count

tabs_html = "\n      ".join(tab_buttons)
sections_html = "\n".join(sections)

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
    .update-toggle[aria-expanded="true"] .update-chevron {{ transform: rotate(90deg); }}
  </style>
</head>
<body class="bg-[#091324] text-[#E6ECF5] font-sans">

  <div class="relative w-full hero-glow" style="height: 220px; overflow: hidden;">
    <div class="absolute inset-0" style="background: linear-gradient(to bottom, transparent 30%, #091324 100%);"></div>
  </div>

  <div class="max-w-[840px] mx-auto px-6 md:px-8 lg:px-0" style="margin-top: -140px; position: relative; z-index: 10;">

    <!-- Header -->
    <section class="pt-12 pb-10">
      <a href="index.html" class="inline-flex items-center gap-2 font-mono text-xs font-semibold uppercase text-[#091324] bg-[#FF2E88] tracking-[0.14em] px-4 py-2.5 rounded-lg hover:bg-[#FF5BA3] transition-all">&larr; Home</a>
      <div class="flex items-center gap-3 mt-6 mb-6">
        <span class="lcars-pill bg-[#FF2E88] h-3 w-10 inline-block"></span>
        <p class="font-mono text-xs uppercase text-[#7E97B8] tracking-[0.18em]">For existing ships &middot; not a fresh build</p>
      </div>
      <h1 class="font-display text-4xl md:text-5xl font-bold text-[#E6ECF5] tracking-[-0.01em] leading-[1.05] mb-5 uppercase">Manual updates</h1>
      <p class="text-lg text-[#9FB3D2] max-w-[620px]">Already built a ship from the starter prompt? These are standalone, paste-able upgrade prompts &mdash; apply just the ones you want, in any order, without rerunning the full interview. Each one figures out your ship's actual file names and mythos on its own.</p>
    </section>

    <!-- Tabs -->
    <div class="flex items-center gap-3 mb-10 flex-wrap">
      {tabs_html}
    </div>

    {sections_html}

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
    // Tabs
    document.querySelectorAll('.tab-btn').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        const tab = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(function (b) {{
          const isActive = b.dataset.tab === tab;
          b.classList.toggle('bg-[#FF2E88]', isActive);
          b.classList.toggle('text-[#091324]', isActive);
          b.classList.toggle('font-semibold', isActive);
          b.classList.toggle('text-[#9FB3D2]', !isActive);
          b.classList.toggle('border', !isActive);
          b.classList.toggle('border-[#1B3252]', !isActive);
        }});
        document.querySelectorAll('.tab-panel').forEach(function (panel) {{
          panel.classList.toggle('hidden', panel.dataset.tab !== tab);
        }});
      }});
    }});

    // Collapsible prompt cards
    document.querySelectorAll('.update-toggle').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        const panel = document.getElementById(btn.dataset.panel);
        const expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!expanded));
        panel.classList.toggle('hidden', expanded);
      }});
    }});

    // Copy single prompt
    document.querySelectorAll('.update-copy-btn').forEach(function (btn) {{
      btn.addEventListener('click', function (e) {{
        e.stopPropagation();
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

    // Copy all prompts in a series
    document.querySelectorAll('.copy-all-btn').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        const ids = btn.dataset.ids.split(',');
        const combined = ids.map(function (id, idx) {{
          const el = document.getElementById(id);
          return '--- Update ' + (idx + 1) + ' of ' + ids.length + ' ---\\n\\n' + el.textContent;
        }}).join('\\n\\n\\n');
        navigator.clipboard.writeText(combined).then(function () {{
          const original = btn.dataset.label;
          btn.textContent = 'Copied all';
          btn.classList.add('text-green-400');
          btn.classList.remove('text-[#9FD3DC]');
          setTimeout(function () {{
            btn.textContent = original;
            btn.classList.remove('text-green-400');
            btn.classList.add('text-[#9FD3DC]');
          }}, 2000);
        }});
      }});
    }});
  </script>
</body>
</html>
'''

OUT.write_text(TEMPLATE)
print(f"wrote {OUT} ({len(TEMPLATE)} bytes, {total_cards} update cards across {len(SERIES)} series)")
