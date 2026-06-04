const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('starship', {
  openFile:          () => ipcRenderer.invoke('file:open'),
  loadConfig:        () => ipcRenderer.invoke('config:load'),
  saveConfig:        (cfg) => ipcRenderer.invoke('config:save', cfg),
  selectFolder:      () => ipcRenderer.invoke('dialog:selectFolder'),
  quitApp:           () => ipcRenderer.invoke('app:quit'),
  listBlobs:         () => ipcRenderer.invoke('file:listBlobs'),
  listFolderImages:  (dir) => ipcRenderer.invoke('file:listFolderImages', dir),
  terminal: {
    create: (opts) => ipcRenderer.invoke('terminal:create', opts),
    write:  (data) => ipcRenderer.send('terminal:write', data),
    resize: (cols, rows) => ipcRenderer.send('terminal:resize', { cols, rows }),
    kill:   () => ipcRenderer.invoke('terminal:kill'),
    onData: (cb) => {
      const handler = (_, data) => cb(data);
      ipcRenderer.on('terminal:data', handler);
      return () => ipcRenderer.removeListener('terminal:data', handler);
    },
    onExit: (cb) => {
      const handler = () => cb();
      ipcRenderer.on('terminal:exit', handler);
      return () => ipcRenderer.removeListener('terminal:exit', handler);
    },
  },
});
