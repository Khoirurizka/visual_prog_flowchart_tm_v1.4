import React, { useEffect, useState } from 'react';

const { ipcRenderer } = window.require("electron");
function ScrewDriverFrameRender() {
  const [frameReceived, setframeReceived] = useState(null);

  useEffect(() => {
    // Listen for 'increment-timer' event from Electron main process
    ipcRenderer.on("VLM_capture", (event, vlm_frame) => {
      try {
        // console.log("Received data from main process:", vlm_frame);

        // Parse and update state with the respective arrays
        setframeReceived(vlm_frame);

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
          <p>VLM capture is unavailable, please wait for the robot.</p>
        </div>
      )}
    </div>
  );
}

export default ScrewDriverFrameRender;
