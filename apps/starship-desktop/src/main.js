const { app, BrowserWindow, ipcMain, shell, dialog, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');

const DEFAULT_STARSHIP_DIR = path.join(__dirname, '../../..');
const CONFIG_PATH = path.join(os.homedir(), '.starship-omni', 'config.json');

let ptyProcess = null;

// ── Config ────────────────────────────────────────────────────────────────────

function ensureConfig() {
  const dir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  if (!fs.existsSync(CONFIG_PATH)) {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify({
      workingDir: DEFAULT_STARSHIP_DIR,
      starterPrompt: '',
    }, null, 2));
  }
  const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  if (!cfg.workingDir) cfg.workingDir = DEFAULT_STARSHIP_DIR;
  return cfg;
}

function saveConfig(config) {
  const dir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

ipcMain.handle('config:load', () => ensureConfig());
ipcMain.handle('config:save', (_, config) => { saveConfig(config); return { ok: true }; });

ipcMain.handle('dialog:selectFolder', async (event) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  const result = await dialog.showOpenDialog(win, {
    title: 'Select Starship OS Working Directory',
    properties: ['openDirectory'],
  });
  if (result.canceled || !result.filePaths.length) return null;
  return result.filePaths[0];
});

// ── Window ────────────────────────────────────────────────────────────────────

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#050d1a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    icon: path.join(__dirname, '../assets/icon.png'),
    title: 'Starship Omni OS',
  });

  win.loadFile(path.join(__dirname, 'index.html'));

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

// ── Feature 5: List bundled blobs + folder images ────────────────────────────

const BLOBS_DIR = path.join(__dirname, '../assets/blobs');

ipcMain.handle('file:listBlobs', () => {
  try {
    if (!fs.existsSync(BLOBS_DIR)) return [];
    return fs.readdirSync(BLOBS_DIR).filter(f => /\.(png|gif|jpg|jpeg|webp)$/i.test(f));
  } catch(_) { return []; }
});

ipcMain.handle('file:listFolderImages', (_, folderPath) => {
  try {
    return fs.readdirSync(folderPath).filter(f => /\.(png|gif|jpg|jpeg|webp)$/i.test(f));
  } catch(_) { return []; }
});

// ── File open ─────────────────────────────────────────────────────────────────

ipcMain.handle('file:open', async (event) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  const result = await dialog.showOpenDialog(win, {
    title: 'Open Markdown File',
    filters: [{ name: 'Markdown', extensions: ['md', 'markdown'] }],
    properties: ['openFile'],
  });
  if (result.canceled || !result.filePaths.length) return null;
  const filePath = result.filePaths[0];
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return { filePath, content };
  } catch (err) {
    return { error: err.message };
  }
});

// ── Terminal (node-pty) ───────────────────────────────────────────────────────

ipcMain.handle('terminal:create', (event, { cols = 80, rows = 24, workingDir } = {}) => {
  let pty;
  try { pty = require('node-pty'); } catch(e) {
    return { error: 'node-pty not available: ' + e.message };
  }

  if (ptyProcess) { try { ptyProcess.kill(); } catch(_) {} ptyProcess = null; }

  const cfg = ensureConfig();
  const cwd = workingDir || cfg.workingDir || DEFAULT_STARSHIP_DIR;

  const userShell = process.env.SHELL || '/bin/zsh';
  ptyProcess = pty.spawn(userShell, ['-l', '-c', 'claude'], {
    name: 'xterm-256color',
    cols, rows,
    cwd,
    env: {
      ...process.env,
      TERM: 'xterm-256color',
      PATH: `${process.env.PATH}:/usr/local/bin:/opt/homebrew/bin`,
    },
  });

  ptyProcess.onData((data) => {
    try { event.sender.send('terminal:data', data); } catch(_) {}
  });

  ptyProcess.onExit(() => {
    ptyProcess = null;
    try { event.sender.send('terminal:exit'); } catch(_) {}
  });

  return { ok: true, cwd };
});

ipcMain.on('terminal:write', (_, data) => {
  if (ptyProcess) ptyProcess.write(data);
});

ipcMain.on('terminal:resize', (_, { cols, rows }) => {
  if (ptyProcess) ptyProcess.resize(cols, rows);
});

ipcMain.handle('terminal:kill', () => {
  if (ptyProcess) { try { ptyProcess.kill(); } catch(_) {} ptyProcess = null; }
  return { ok: true };
});

ipcMain.handle('app:quit', () => {
  app.quit();
});

// ── App lifecycle ─────────────────────────────────────────────────────────────

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
