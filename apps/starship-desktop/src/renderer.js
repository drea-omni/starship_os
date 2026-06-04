// ── Blobby pixel art ─────────────────────────────────────────────────────────

function drawBlobby(frame) {
  const canvas = document.getElementById('blobby');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = 48, H = 48;
  ctx.clearRect(0, 0, W, H);

  const SCALE = 4;
  const PINK  = '#ff2d78';
  const PINK2 = '#c41e5a';
  const WHITE = '#ffffff';
  const DARK  = '#0a0f1e';

  const body = [
    [0,0,0,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0,0],
  ];

  body.forEach((row, y) => {
    row.forEach((px, x) => {
      if (!px) return;
      ctx.fillStyle = y < 4 ? PINK : PINK2;
      ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
    });
  });

  // Eyes — blink every 60 frames
  const eyeOpen = frame % 60 <= 54;
  const eyeSize = SCALE;
  ctx.fillStyle = DARK;
  ctx.fillRect(2 * SCALE, 3 * SCALE, SCALE * 2, SCALE * 2);
  ctx.fillRect(7 * SCALE, 3 * SCALE, SCALE * 2, SCALE * 2);
  if (eyeOpen) {
    ctx.fillStyle = WHITE;
    ctx.fillRect(2 * SCALE, 3 * SCALE, eyeSize, eyeSize);
    ctx.fillRect(7 * SCALE, 3 * SCALE, eyeSize, eyeSize);
  }

  // Smile
  [[4,8],[5,9],[6,9],[7,8]].forEach(([x, y]) => {
    ctx.fillStyle = DARK;
    ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
  });
}

let blobbyFrame = 0;
setInterval(() => drawBlobby(blobbyFrame++), 50);

// ── Theme engine ──────────────────────────────────────────────────────────────

const TERM_COLORS = {
  dark: {
    foreground:    '#c8deff',
    cursor:        '#ff2d78',
    cursorAccent:  '#050d1a',
    selectionBackground: 'rgba(255,45,120,0.35)',
    black: '#0a0f1e', red: '#ff2d78', green: '#00d4ff', yellow: '#f0c040',
    blue: '#2060c8', magenta: '#c41e5a', cyan: '#00d4ff', white: '#c8deff',
    brightBlack: '#4a6a99', brightRed: '#ff2d78', brightGreen: '#00d4ff',
    brightYellow: '#f0c040', brightBlue: '#2060c8', brightMagenta: '#ff2d78',
    brightCyan: '#00d4ff', brightWhite: '#e8f4ff',
  },
  light: {
    foreground:    '#1a2a4a',
    cursor:        '#ff2d78',
    cursorAccent:  '#eef2fa',
    selectionBackground: 'rgba(255,45,120,0.25)',
    black: '#d4dff0', red: '#cc1155', green: '#006fa0', yellow: '#a08000',
    blue: '#1a55a8', magenta: '#a01050', cyan: '#007a9a', white: '#1a2a4a',
    brightBlack: '#5a7aaa', brightRed: '#ff2d78', brightGreen: '#00aad4',
    brightYellow: '#c09000', brightBlue: '#2060c8', brightMagenta: '#ff2d78',
    brightCyan: '#00b8d4', brightWhite: '#0a1830',
  }
};

const DEFAULT_TERM_BG = { dark: '#050d1a', light: '#eef2fa' };

function buildTermTheme(theme, termBg) {
  const bg = termBg || DEFAULT_TERM_BG[theme] || DEFAULT_TERM_BG.dark;
  return { ...TERM_COLORS[theme] || TERM_COLORS.dark, background: bg };
}

function applyTheme(theme, termBg) {
  document.documentElement.setAttribute('data-theme', theme);
  if (term) term.options.theme = buildTermTheme(theme, termBg);
  // Sync CSS var for xterm viewport override
  const bg = termBg || DEFAULT_TERM_BG[theme] || DEFAULT_TERM_BG.dark;
  document.documentElement.style.setProperty('--term-bg', bg);
}

function applyTermBg(color) {
  document.documentElement.style.setProperty('--term-bg', color);
  if (term) term.options.theme = { ...term.options.theme, background: color };
}

// ── Status helpers ────────────────────────────────────────────────────────────

const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

function setStatus(state, label) {
  statusDot.className = `status-dot status-dot--${state}`;
  statusText.textContent = label;
}

// ── Terminal ──────────────────────────────────────────────────────────────────

let term = null;
let fitAddon = null;

async function initTerminal() {
  const container = document.getElementById('terminal-container');
  if (!container) return;

  // xterm loaded via script tag
  const TermClass = window.Terminal;
  // @xterm/addon-fit UMD exports as window.FitAddon (object with FitAddon class)
  const FitAddonClass = window.FitAddon?.FitAddon ?? window.FitAddon;

  if (!TermClass) {
    container.innerHTML = '<div style="color:#ff2d78;padding:1rem;font-family:monospace">ERROR: xterm.js failed to load.</div>';
    return;
  }

  const termFontFamily = appConfig.termFont
    ? `'${appConfig.termFont}', 'Courier New', monospace`
    : "'Share Tech Mono', 'Courier New', monospace";
  const termFontSize = parseInt(appConfig.termFontSize) || 14;

  term = new TermClass({
    theme: buildTermTheme(appConfig.theme || 'dark', appConfig.termBg || ''),
    fontFamily: termFontFamily,
    fontSize: termFontSize,
    lineHeight: 1.4,
    cursorBlink: true,
    cursorStyle: 'block',
    scrollback: 10000,
    allowTransparency: false,
  });

  if (FitAddonClass) {
    fitAddon = new FitAddonClass();
    term.loadAddon(fitAddon);
  }

  term.open(container);
  if (fitAddon) fitAddon.fit();

  // Input → PTY
  term.onData((data) => window.starship.terminal.write(data));

  // PTY output → terminal
  window.starship.terminal.onData((data) => term.write(data));

  // Session exit
  window.starship.terminal.onExit(() => {
    setStatus('idle', 'ENDED');
    term.write('\r\n\x1b[33m── session ended ── click ⟳ RESTART to reconnect ──\x1b[0m\r\n');
  });

  // Resize observer
  const ro = new ResizeObserver(() => {
    if (!fitAddon) return;
    fitAddon.fit();
    window.starship.terminal.resize(term.cols, term.rows);
  });
  ro.observe(container);

  // Launch claude
  setStatus('thinking', 'LAUNCHING');
  const result = await window.starship.terminal.create({ cols: term.cols, rows: term.rows });

  if (result?.error) {
    term.write(`\x1b[31mERROR: ${result.error}\x1b[0m\r\n`);
    setStatus('error', 'ERROR');
    return;
  }

  setStatus('streaming', 'CONNECTED');
  if (result?.cwd) {
    const parts = result.cwd.replace(/\\/g, '/').split('/');
    document.getElementById('cwdDisplay').textContent = parts[parts.length - 1] || result.cwd;
    document.getElementById('cwdDisplay').title = result.cwd;
  }

  scheduleAutoGreet();

  // ── Feature 1: Link detection ──
  if (term.registerLinkProvider) {
    term.registerLinkProvider({
      provideLinks(y, callback) {
        const line = term.buffer.active.getLine(y);
        if (!line) { callback([]); return; }
        const text = line.translateToString(true);
        const urlRe = /https?:\/\/[^\s"'>)]+/g;
        const links = [];
        let m;
        while ((m = urlRe.exec(text)) !== null) {
          links.push({
            range: { start: { x: m.index + 1, y }, end: { x: m.index + m[0].length, y } },
            text: m[0],
            activate(e, text) { loadUrlInPreview(text); },
          });
        }
        callback(links);
      }
    });
  }
}

// ── Auto-greet ────────────────────────────────────────────────────────────────

function scheduleAutoGreet() {
  if (!appConfig.autoGreet) return;
  let sent = false;
  let quietTimer = null;
  let maxTimer = null;

  function send() {
    if (sent) return;
    sent = true;
    clearTimeout(quietTimer);
    clearTimeout(maxTimer);
    window.starship.terminal.write('Computer, good morning\r');
  }

  // Wait for first PTY data → reset 2s quiet timer → send when quiet
  // Hard cap at 8s in case Claude stays noisy
  const unsub = window.starship.terminal.onData(() => {
    if (sent) { unsub(); return; }
    if (!maxTimer) maxTimer = setTimeout(send, 8000);
    clearTimeout(quietTimer);
    quietTimer = setTimeout(() => { unsub(); send(); }, 2000);
  });

  // Absolute fallback — if no data ever, still try after 12s
  setTimeout(() => { if (!sent) { unsub(); send(); } }, 12000);
}

// ── Clear session ─────────────────────────────────────────────────────────────

document.getElementById('clearBtn').addEventListener('click', () => {
  if (!term) return;
  window.starship.terminal.write('/clear\r');
});

// ── Wrap session ──────────────────────────────────────────────────────────────

document.getElementById('wrapBtn').addEventListener('click', () => {
  if (!term) return;
  window.starship.terminal.write('Computer, end program\r');
});

// ── Exit app ──────────────────────────────────────────────────────────────────

document.getElementById('exitBtn').addEventListener('click', () => {
  window.starship.quitApp();
});

// ── Restart ───────────────────────────────────────────────────────────────────

document.getElementById('restartBtn').addEventListener('click', async () => {
  if (!term) return;
  setStatus('thinking', 'RESTARTING');
  term.write('\r\n\x1b[33m── restarting session ──\x1b[0m\r\n');
  const result = await window.starship.terminal.create({ cols: term.cols, rows: term.rows });
  if (result?.error) {
    term.write(`\x1b[31mERROR: ${result.error}\x1b[0m\r\n`);
    setStatus('error', 'ERROR');
  } else {
    setStatus('streaming', 'CONNECTED');
    scheduleAutoGreet();
  }
});

// ── Preview panel ─────────────────────────────────────────────────────────────

let previewOpen = false;

function openPreviewPanel() {
  previewOpen = true;
  document.getElementById('previewPanel').classList.remove('hidden');
  document.getElementById('contentSplit').classList.add('split-with-preview');
  setTimeout(() => { if (fitAddon) fitAddon.fit(); }, 50);
}

function closePreviewPanel() {
  previewOpen = false;
  document.getElementById('previewPanel').classList.add('hidden');
  document.getElementById('contentSplit').classList.remove('split-with-preview');
  setTimeout(() => { if (fitAddon) fitAddon.fit(); }, 50);
}

document.getElementById('previewToggleBtn').addEventListener('click', () => {
  previewOpen ? closePreviewPanel() : openPreviewPanel();
});

document.getElementById('previewCloseBtn').addEventListener('click', closePreviewPanel);

async function openFileAndRender() {
  const result = await window.starship.openFile();
  if (!result) return;
  if (result.error) { console.error('File read error:', result.error); return; }

  if (!previewOpen) openPreviewPanel();

  const parts = result.filePath.replace(/\\/g, '/').split('/');
  document.getElementById('previewFileName').textContent = parts[parts.length - 1].toUpperCase();

  // Simple markdown render (no external dep needed — basic conversion)
  const html = result.content
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^#{3} (.+)$/gm, '<h3>$1</h3>')
    .replace(/^#{2} (.+)$/gm, '<h2>$1</h2>')
    .replace(/^#{1} (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<[hli])(.+)$/gm, '$1');

  document.getElementById('previewBody').innerHTML = `<div class="preview-markdown"><p>${html}</p></div>`;
}

document.getElementById('previewOpenBtn').addEventListener('click', openFileAndRender);
document.getElementById('openFileBtn').addEventListener('click', openFileAndRender);

// ── Feature 1: Load URL in preview panel ─────────────────────────────────────

function loadUrlInPreview(url) {
  if (!previewOpen) openPreviewPanel();
  const frame = document.getElementById('previewFrame');
  const body  = document.getElementById('previewBody');
  const empty = document.getElementById('previewEmpty');
  // Try to get a display title
  let title = url;
  try { title = new URL(url).hostname; } catch(e) {}
  // Drive /view → /preview for iframe embedding
  const embedUrl = url.replace(/\/view(\?.*)?$/, '/preview$1');
  document.getElementById('previewFileName').textContent = title.toUpperCase();
  // Hide markdown div, show iframe
  document.querySelectorAll('.preview-markdown').forEach(el => el.remove());
  if (empty) empty.classList.add('hidden');
  frame.classList.remove('hidden');
  frame.src = embedUrl;
}

// ── Settings modal ────────────────────────────────────────────────────────────

let appConfig = { workingDir: '', starterPrompt: '', theme: 'dark', termBg: '', autoGreet: true };

document.getElementById('settingsBtn').addEventListener('click', async () => {
  appConfig = await window.starship.loadConfig();
  document.getElementById('workingDirInput').value = appConfig.workingDir || '';
  document.getElementById('starterPromptInput').value = appConfig.starterPrompt || '';

  // Appearance fields
  const theme = appConfig.theme || 'dark';
  document.getElementById('themeDarkBtn').classList.toggle('active', theme === 'dark');
  document.getElementById('themeLightBtn').classList.toggle('active', theme === 'light');
  const termBg = appConfig.termBg || DEFAULT_TERM_BG[theme] || DEFAULT_TERM_BG.dark;
  document.getElementById('termBgPicker').value = termBg;
  document.getElementById('termBgHex').value = termBg;
  document.getElementById('autoGreetCheck').checked = appConfig.autoGreet !== false;

  // Terminal font fields
  document.getElementById('termFontInput').value = appConfig.termFont || '';
  document.getElementById('termFontSizeSelect').value = appConfig.termFontSize || '14';
  // Feature 3: Preview style fields
  document.getElementById('previewFontSize').value = appConfig.previewFontSize || '14px';
  const prevBg = appConfig.previewBg || '';
  document.getElementById('previewBgHex').value = prevBg;
  if (prevBg && /^#[0-9a-fA-F]{6}$/.test(prevBg)) document.getElementById('previewBgPicker').value = prevBg;
  document.getElementById('previewLineHeight').value = appConfig.previewLineHeight || '';
  document.getElementById('previewFontFamily').value = appConfig.previewFontFamily || '';
  // Feature 5: Blobby grid
  await loadBlobbyGrid();
  document.getElementById('settingsModal').classList.remove('hidden');
});

document.getElementById('settingsClose').addEventListener('click', () => {
  document.getElementById('settingsModal').classList.add('hidden');
});

document.getElementById('cancelSettingsBtn').addEventListener('click', () => {
  document.getElementById('settingsModal').classList.add('hidden');
});

document.getElementById('browseFolderBtn').addEventListener('click', async () => {
  const dir = await window.starship.selectFolder();
  if (dir) document.getElementById('workingDirInput').value = dir;
});

document.getElementById('saveSettingsBtn').addEventListener('click', async () => {
  appConfig.workingDir    = document.getElementById('workingDirInput').value.trim();
  appConfig.starterPrompt = document.getElementById('starterPromptInput').value;
  appConfig.theme         = document.getElementById('themeDarkBtn').classList.contains('active') ? 'dark' : 'light';
  appConfig.termBg        = document.getElementById('termBgHex').value.trim() || DEFAULT_TERM_BG[appConfig.theme];
  appConfig.autoGreet     = document.getElementById('autoGreetCheck').checked;
  // Terminal font
  appConfig.termFont     = document.getElementById('termFontInput').value.trim();
  appConfig.termFontSize = document.getElementById('termFontSizeSelect').value;
  if (term) {
    term.options.fontFamily = appConfig.termFont
      ? `'${appConfig.termFont}', 'Courier New', monospace`
      : "'Share Tech Mono', 'Courier New', monospace";
    term.options.fontSize = parseInt(appConfig.termFontSize) || 14;
    if (fitAddon) fitAddon.fit();
  }
  // Feature 3
  appConfig.previewFontSize   = document.getElementById('previewFontSize').value;
  appConfig.previewBg         = document.getElementById('previewBgHex').value.trim();
  appConfig.previewLineHeight = document.getElementById('previewLineHeight').value.trim();
  appConfig.previewFontFamily = document.getElementById('previewFontFamily').value.trim();
  applyPreviewStyle(appConfig);
  await window.starship.saveConfig(appConfig);
  document.getElementById('settingsModal').classList.add('hidden');

  // Apply theme + termBg immediately
  applyTheme(appConfig.theme, appConfig.termBg);

  if (appConfig.workingDir) {
    const parts = appConfig.workingDir.replace(/\\/g, '/').split('/');
    document.getElementById('cwdDisplay').textContent = parts[parts.length - 1] || appConfig.workingDir;
    document.getElementById('cwdDisplay').title = appConfig.workingDir;
  }
});

document.getElementById('launchStarterBtn').addEventListener('click', async () => {
  const starterField = document.getElementById('starterPromptInput');
  // If the field is empty, fall back to the prompt bundled with the app
  // (starter-prompt.js → window.BUNDLED_STARTER_PROMPT). Fill it in so it's
  // visible/editable, then launch — one click pastes and fires.
  if (!starterField.value.trim() && window.BUNDLED_STARTER_PROMPT) {
    starterField.value = window.BUNDLED_STARTER_PROMPT;
  }
  const prompt = starterField.value.trim();
  appConfig.workingDir    = document.getElementById('workingDirInput').value.trim();
  appConfig.starterPrompt = starterField.value;
  await window.starship.saveConfig(appConfig);
  document.getElementById('settingsModal').classList.add('hidden');

  // Restart session in new dir, then type the starter prompt
  if (!term) return;
  setStatus('thinking', 'RESTARTING');
  term.write('\r\n\x1b[33m── launching starter prompt ──\x1b[0m\r\n');
  const result = await window.starship.terminal.create({
    cols: term.cols, rows: term.rows,
    workingDir: appConfig.workingDir || undefined,
  });
  if (result?.error) {
    term.write(`\x1b[31mERROR: ${result.error}\x1b[0m\r\n`);
    setStatus('error', 'ERROR');
    return;
  }
  setStatus('streaming', 'CONNECTED');
  // Wait briefly for claude to initialize, then send the starter prompt
  if (prompt) {
    setTimeout(() => {
      window.starship.terminal.write(prompt + '\r');
    }, 3000);
  }
});

// ── Feature 4: Theme toggle button ──────────────────────────────────────────────

document.getElementById('themeToggleBtn').addEventListener('click', async () => {
  appConfig.theme = appConfig.theme === 'dark' ? 'light' : 'dark';
  appConfig.termBg = DEFAULT_TERM_BG[appConfig.theme];
  applyTheme(appConfig.theme, appConfig.termBg);
  document.getElementById('themeToggleBtn').textContent = appConfig.theme === 'dark' ? '☀' : '◑';
  // Sync settings modal if open
  document.getElementById('themeDarkBtn').classList.toggle('active', appConfig.theme === 'dark');
  document.getElementById('themeLightBtn').classList.toggle('active', appConfig.theme === 'light');
  document.getElementById('termBgPicker').value = appConfig.termBg;
  document.getElementById('termBgHex').value = appConfig.termBg;
  await window.starship.saveConfig(appConfig);
});

// ── Theme + color picker wiring ───────────────────────────────────────────────

document.getElementById('themeDarkBtn').addEventListener('click', () => {
  document.getElementById('themeDarkBtn').classList.add('active');
  document.getElementById('themeLightBtn').classList.remove('active');
  const newBg = DEFAULT_TERM_BG.dark;
  document.getElementById('termBgPicker').value = newBg;
  document.getElementById('termBgHex').value = newBg;
});

document.getElementById('themeLightBtn').addEventListener('click', () => {
  document.getElementById('themeLightBtn').classList.add('active');
  document.getElementById('themeDarkBtn').classList.remove('active');
  const newBg = DEFAULT_TERM_BG.light;
  document.getElementById('termBgPicker').value = newBg;
  document.getElementById('termBgHex').value = newBg;
});

// Keep color picker and hex input in sync
document.getElementById('termBgPicker').addEventListener('input', (e) => {
  document.getElementById('termBgHex').value = e.target.value;
});

document.getElementById('termBgHex').addEventListener('input', (e) => {
  const val = e.target.value.trim();
  if (/^#[0-9a-fA-F]{6}$/.test(val)) {
    document.getElementById('termBgPicker').value = val;
  }
});

// ── Feature 2: Sidebar command click-to-paste ───────────────────────────────────

document.querySelectorAll('.sidebar-cmd').forEach(el => {
  el.addEventListener('click', () => {
    if (!term) return;
    window.starship.terminal.write(el.dataset.cmd + '\r');
  });
});

// ── Boot ──────────────────────────────────────────────────────────────────────

// ── Feature 3: Apply preview style ──────────────────────────────────────────────

function applyPreviewStyle(cfg) {
  const panel = document.getElementById('previewPanel');
  if (!panel) return;
  if (cfg.previewFontSize) panel.style.setProperty('--preview-font-size', cfg.previewFontSize);
  if (cfg.previewBg)       panel.style.setProperty('--preview-bg',        cfg.previewBg);
  if (cfg.previewLineHeight) panel.style.setProperty('--preview-line-height', cfg.previewLineHeight);
  if (cfg.previewFontFamily) panel.style.setProperty('--preview-font-family', cfg.previewFontFamily);
}

// ── Feature 5: Blobby picker ─────────────────────────────────────────────────

const BLOBS_PATH = '../assets/blobs/';

async function loadBlobbyGrid(extraPaths) {
  const grid = document.getElementById('blobbyGrid');
  if (!grid) return;
  grid.innerHTML = '';
  // Default canvas option
  const defaultItem = document.createElement('div');
  defaultItem.className = 'blobby-grid-item' + (appConfig.blobbySelection === 'default' || !appConfig.blobbySelection ? ' selected' : '');
  defaultItem.title = 'Default (animated)';
  const mini = document.createElement('canvas'); mini.width = 32; mini.height = 32;
  const ctx = mini.getContext('2d'); ctx.fillStyle = '#ff2d78'; ctx.beginPath(); ctx.arc(16,16,12,0,Math.PI*2); ctx.fill();
  defaultItem.appendChild(mini);
  defaultItem.addEventListener('click', () => { selectBlobby('default'); });
  grid.appendChild(defaultItem);
  // Bundled blobs
  const bundled = await window.starship.listBlobs?.() || [];
  const allPaths = [...bundled.map(f => BLOBS_PATH + f), ...(extraPaths||[])];
  allPaths.forEach(src => {
    const item = document.createElement('div');
    item.className = 'blobby-grid-item' + (appConfig.blobbySelection === src ? ' selected' : '');
    const img = document.createElement('img');
    img.src = src; img.width = 40; img.height = 40; img.style.objectFit = 'contain';
    item.appendChild(img);
    item.title = src.split('/').pop();
    item.addEventListener('click', () => { selectBlobby(src); });
    grid.appendChild(item);
  });
}

function selectBlobby(src) {
  appConfig.blobbySelection = src;
  setBlobby(src);
  document.querySelectorAll('.blobby-grid-item').forEach(el => el.classList.remove('selected'));
  const items = document.querySelectorAll('.blobby-grid-item');
  items.forEach(el => {
    const img = el.querySelector('img');
    if ((src === 'default' && !img) || (img && img.src.endsWith(src.split('/').pop()))) {
      el.classList.add('selected');
    }
  });
}

function setBlobby(src) {
  const canvas = document.getElementById('blobby');
  const img    = document.getElementById('blobbyImg');
  if (!canvas || !img) return;
  if (src === 'default' || !src) {
    canvas.classList.remove('hidden');
    img.classList.add('hidden');
    img.src = '';
  } else {
    canvas.classList.add('hidden');
    img.classList.remove('hidden');
    img.src = src;
  }
}

async function boot() {
  appConfig = await window.starship.loadConfig();
  appConfig.theme     = appConfig.theme     || 'dark';
  appConfig.termBg    = appConfig.termBg    || '';
  appConfig.autoGreet = appConfig.autoGreet !== false;
  applyTheme(appConfig.theme, appConfig.termBg);
  applyPreviewStyle(appConfig);
  setBlobby(appConfig.blobbySelection || 'default');
  document.getElementById('themeToggleBtn').textContent = appConfig.theme === 'dark' ? '☀' : '◑';
  await initTerminal();
}

boot();

// Feature 3: Preview advanced toggle
document.getElementById('previewAdvancedToggle')?.addEventListener('click', () => {
  const adv = document.getElementById('previewAdvanced');
  const tog = document.getElementById('previewAdvancedToggle');
  adv.classList.toggle('hidden');
  tog.textContent = adv.classList.contains('hidden') ? '▶ ADVANCED' : '▼ ADVANCED';
});

// Feature 3: preview bg color picker sync
document.getElementById('previewBgPicker')?.addEventListener('input', (e) => {
  document.getElementById('previewBgHex').value = e.target.value;
});
document.getElementById('previewBgHex')?.addEventListener('input', (e) => {
  const val = e.target.value.trim();
  if (/^#[0-9a-fA-F]{6}$/.test(val)) document.getElementById('previewBgPicker').value = val;
});

// Feature 5: Blobby folder picker
document.getElementById('blobbyFolderBtn')?.addEventListener('click', async () => {
  const dir = await window.starship.selectFolder();
  if (!dir) return;
  const files = await window.starship.listFolderImages?.(dir) || [];
  const paths = files.map(f => 'file://' + dir + '/' + f);
  await loadBlobbyGrid(paths);
});
