import React from 'react';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {

  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice to meet you.');

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };
  
 
  const handleWriteLLMResponse = (responseText) => {
    setState((prev) => {
      // Get the last message in the messages array
      const lastMessage = prev.messages[prev.messages.length - 1];
  
      // Only add the new message if it's different from the last message
      if (!lastMessage || lastMessage.message !== responseText) {
        const botMessage = createChatBotMessage(responseText);
  
        return {
          ...prev,
          messages: [...prev.messages, botMessage],
        };
      }
  
      // If the text is the same, return the state unchanged
      return prev;
    });
  /*   const lastMessage = prev.messages[prev.messages.length - 1];
    if (!lastMessage || lastMessage.message !== responseText) {

    const botMessage = createChatBotMessage(responseText);

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));*/
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {handleHello,handleWriteLLMResponse},
        });
      })}
    </div>
  );
};

export default ActionProvider;