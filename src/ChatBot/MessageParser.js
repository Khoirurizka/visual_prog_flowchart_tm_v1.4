import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Use import syntax for axios
const { ipcRenderer } = window.require("electron");

const MessageParser = ({ children, actions }) => {
  const [isSubmitting, setIsSubmitting] = useState(false); // Track ongoing submissions
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


  const parse = async (message) => {
    if (isSubmitting) {
      console.warn("Submission is already in progress. Please wait.");
      return; // Prevent further submissions while one is ongoing
    }

    setIsSubmitting(true); // Set submission flag to true
    try {
      console.log("Message:", message);

      let response = await axios.post("http://127.0.0.2:8000/user_prompt_to_LLM_server", {
        message: message,
        frame_screw_driver: frameReceived
      });

      console.log(response.data.result_from_AI)
      if (response && response.data) {
        // Send the data to the renderer process
        ipcRenderer.send("update_main_graph_chat_response_from_AI", response.data.result_from_AI);
        ipcRenderer.send("update_VLM_frame_from_AI", response.data.result_from_AI.vlm_frame);
        console.log('update graph and show VLM figure  successfully');
      } else {
        console.error("Invalid response from LLM server");
      }
    } catch (error) {
      console.error("Error posting data:", error);
    } finally {
      setIsSubmitting(false); // Reset submission flag
    }
  };

  useEffect(() => {
    ipcRenderer.on("response_from_LLM", (event, jsonData) => {
      try {
        console.log("Received data from main process msg:", jsonData);

        console.log(jsonData.message)
        actions.handleWriteLLMResponse(jsonData.message);


      } catch (error) {
        console.error("Error parsing JSON data:", error);
      }
    });
  }, []);
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse,
          actions: actions, // Pass the actions prop if needed
        });
      })}
    </div>
  );
};

export default MessageParser;
