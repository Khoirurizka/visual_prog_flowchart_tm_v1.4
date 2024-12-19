import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Use import syntax for axios
const { ipcRenderer } = window.require("electron");

const MessageParser = ({ children, actions }) => {
  const [isSubmitting, setIsSubmitting] = useState(false); // Track ongoing submissions

  const parse = async (message) => {
    if (isSubmitting) {
      console.warn("Submission is already in progress. Please wait.");
      return; // Prevent further submissions while one is ongoing
    }

    setIsSubmitting(true); // Set submission flag to true
    try {
      console.log("Message:", message);

      const response = await axios.post("http://127.0.0.1:5000/user_prompt_to_LLM_server", {
        message: message,
      });

      console.log("Response from server:", response.data); // Log the response
    } catch (error) {
      console.error("Error posting data:", error);
    } finally {
      setIsSubmitting(false); // Reset submission flag
    }
  };

  useEffect(() => {
    ipcRenderer.on("response_from_LLM", (event, jsonData) => {
      try {
        console.log("Received data from main process:", jsonData);
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
