const { app, BrowserWindow, ipcMain } = require('electron');
const url = require('url');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const { Console } = require('console');

let mainWindow;

require('@electron/remote/main').initialize()
function createMainWindow() {
  mainWindow = new BrowserWindow({
    title: 'Visual Graph Generaive Planner',
    width: 800,
    height: 450,
    // fullscreen: true,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      contextIsolation: false,
      webSecurity: false

      // preload: path.join(__dirname, 'renderer.js'),
    },
  });

  // Open DevTools for debugging
  mainWindow.webContents.openDevTools();

  // Set startUrl to localhost:3000
  const startUrl = 'http://localhost:3000';
  mainWindow.maximize();
  // mainWindow.loadFile('index.html');
  require('@electron/remote/main').enable(mainWindow.webContents)

  mainWindow.loadURL(startUrl);
}

// Listening for collecting local resource
// Function to set up the Express.js server
function setupExpressServer() {
  const server = express();
  server.use(bodyParser.json());

  //temporary
  server.post('/screw_diver_capture', (req, res) => {
    // console.log('Received data:', req.body);
    mainWindow.webContents.send("screw_diver_capture", req.body);

    res.json({ status: 'success', message: 'screw_diver_capture received successfully' });
  });

  // Start the server on port 3000
  server.listen(6000, () => {
    console.log('Express server is running on http://localhost:6000');
  });
}

// from internal electron app
ipcMain.on('update_main_graph_chat_response_from_AI', (event, jsonData) => {
  // Send a message back to the renderer
  mainWindow.webContents.send("update_graph", jsonData);
  mainWindow.webContents.send("response_from_LLM", jsonData);
});
ipcMain.on('update_VLM_frame_from_AI', (event, frame) => {
  // Send a message back to the renderer
  mainWindow.webContents.send("VLM_capture", frame);
});

app.whenReady().then(() => {
  setupExpressServer();
  createMainWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow()
    }
  })
})

app.on('before-quit', () => {
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
});