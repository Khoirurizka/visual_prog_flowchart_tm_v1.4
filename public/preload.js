const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendData: (data) => ipcRenderer.invoke('update-data', data),
  sendToPython: (message) => ipcRenderer.send('send-to-python', message),

});
