import React, { useEffect, useState } from 'react';

const { ipcRenderer } = window.require("electron");
function ScrewDriverFrameRender() {
  const [frameReceived, setframeReceived] = useState(null);

  useEffect(() => {
    // Listen for 'increment-timer' event from Electron main process
    ipcRenderer.on("screw_diver_capture", (event, File_image) => {
      try {
        // console.log("Received data from main process:", File_image.image);

        // Parse and update state with the respective arrays
        setframeReceived(File_image.image);

      } catch (error) {
        console.error("Error parsing JSON data:", error);
      }
    });
  }, []);


  return (
    <div>
      {frameReceived ? (
        <img
          src={`data:image/jpeg;base64,${frameReceived}`}
          alt="Received"
          style={{ width: '800px', height: 'auto' }}
        />
      ) : (
        <div style={{ paddingTop: '150px', paddingBottom: '150px', paddingLeft: '20px', paddingRight: '20px' }}>
          <p>Screw driver capture is unavailable, please wait for the robot.</p>
        </div>
      )}
    </div>
  );
}

export default ScrewDriverFrameRender;