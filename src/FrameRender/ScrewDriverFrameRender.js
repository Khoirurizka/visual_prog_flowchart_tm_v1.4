import React, { useEffect, useState } from 'react';

const { ipcRenderer } = window.require("electron");
function ScrewDriverFrameRender() {
  const [frameReceived, setframeReceived] = useState(null);

  useEffect(() => {
    // Listen for 'increment-timer' event from Electron main process
    ipcRenderer.on("screw_diver_capture", (event, File_image) => {
      try {
        console.log("Received data from main process:", File_image.image);

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
          <p>Screw driver capture is not unavailable, please wait form robot.</p>
        </div>
      )}
    </div>
  );
}

export default ScrewDriverFrameRender;

//const url_gripper_frame ="http://127.0.0.1:7000/screw_driver_frame_feed"

/*
  const [videoAvailable, setVideoAvailable] = useState(true);
  const [imageKey, setImageKey] = useState(0); // To force image reload
 <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '370px', // Full viewport height for vertical centering
        textAlign: 'center',
      }}
    >
      {videoAvailable ? (
        <img
          key={imageKey} // Unique key to force reload
          src={url_gripper_frame}
          alt="Cam"
          style={{
            width: '100%',
            height: 'auto',
            maxWidth: '600px', // Ensures the image scales properly
          }}
          onAnimationEnd={() => console.log('Animation ended')}
          onError={handleImageError}
        />
      ) : (
        <div style={{ padding: '20px' }}>
          <p>Screw Driver Capture is not unavailable, please update manually with refresh button.</p>
        </div>
      )}
      <div style={{ marginTop: '10px' }}>
        <button onClick={handleRefresh} style={{ padding: '5px 20px', fontSize: '12px' }}>
          Refresh
        </button>
      </div>
    </div>

*/
