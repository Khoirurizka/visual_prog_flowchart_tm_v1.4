import React, { useState } from 'react';

function FrameRender() {
  const [videoAvailable, setVideoAvailable] = useState(true);
  const [imageKey, setImageKey] = useState(0); // To force image reload

  const checkVideoFeed = async () => {
    try {
      const response = await fetch("http://localhost:5001/video_feed", {
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
    <div>
      {videoAvailable ? (
        <img
          key={imageKey} // Unique key to force reload
          src="http://localhost:5001/video_feed"
          alt="Cam"
          style={{ width: '100%', height: 'auto' }}
          onAnimationEnd={() => console.log('Animation ended')}
          onError={handleImageError}
        />
      ) : (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <p>Video feed unavailable</p>
        </div>
      )}
      <div style={{ textAlign: 'center', marginTop: '10px' }}>
        <button onClick={handleRefresh} style={{ padding: '5px 20px', fontSize: '12px' }}>
          Refresh
        </button>
      </div>
    </div>
  );
}

export default FrameRender;
