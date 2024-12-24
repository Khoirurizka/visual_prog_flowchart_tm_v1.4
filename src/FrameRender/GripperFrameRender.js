import React, { useState } from 'react';

const url_gripper_frame = "http://localhost:5001/gripper_frame_feed"

function GripperFrameRender() {
  const [videoAvailable, setVideoAvailable] = useState(true);
  const [imageKey, setImageKey] = useState(0); // To force image reload

  const checkVideoFeed = async () => {
    try {
      const response = await fetch(url_gripper_frame, {
        method: 'HEAD',
      });
      return response.ok; // Returns true if the feed is available
    } catch (error) {
      return false; // Returns false if an error occurs
    }
  };

  const handleRefresh = async () => {
    const isAvailable = await checkVideoFeed();
    setVideoAvailable(isAvailable);
    setImageKey((prevKey) => prevKey + 1); // Force image reload by updating key
  };

  const handleImageError = () => {
    setVideoAvailable(false);
  };

  return (
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
          <p>Gripper Capture is not unavailable, please update manually with refresh button.</p>
        </div>
      )}
      <div style={{ marginTop: '10px' }}>
        <button onClick={handleRefresh} style={{ padding: '5px 20px', fontSize: '12px' }}>
          Refresh
        </button>
      </div>
    </div>

  );
}

export default GripperFrameRender;
