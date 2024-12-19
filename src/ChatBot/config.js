import { createChatBotMessage } from 'react-chatbot-kit';
import botAvatar from '../assets/Cover Icon 500x500px.png';
import userAvatar from '../assets/User Engineer 500x500px.png';

const config = {
    initialMessages: [createChatBotMessage("Hi there! I’m Hucenrotia Assistant, I can help you design or refine your automation project. let's turn  ideas into reality!")],
    botName: "Hucenrotia",
    customComponents: {
        // Replaces the default header
        header: () => <div ></div>,
        botAvatar: () => <img
            src={botAvatar}
            alt="Bot Avatar"
            style={{ width: '100px', height: '80px', borderRadius: '50%',    padding: '0px 20px 0px 0px',marginRight: '5px' }}
        />,
        userAvatar: () => <img
        src={userAvatar}
        alt="User Avatar"
        style={{ width: '100px', height: '80px', borderRadius: '50%',    padding: '0px 20px 0px 0px',marginLeft: '5px' }}
    />,

    },
};

export default config;