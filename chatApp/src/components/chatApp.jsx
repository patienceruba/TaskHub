import React, { useEffect, useRef, useState } from 'react';
import './styles/chat.css';  // Your CSS file

const ChatApp = ({ teamId, username }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const chatBoxRef = useRef(null);
  const socketRef = useRef(null);

  useEffect(() => {
    // Open WebSocket connection
    socketRef.current = new WebSocket(`ws://${window.location.host}/ws/chat/${teamId}/`);

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Append new message to messages list
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    socketRef.current.onclose = () => {
      console.error('Chat socket closed unexpectedly');
    };

    // Cleanup on component unmount
    return () => {
      socketRef.current.close();
    };
  }, [teamId]);

  useEffect(() => {
    // Auto scroll chat box to bottom on new messages
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Send message over WebSocket
    socketRef.current.send(JSON.stringify({ message }));

    // Clear input field
    setMessage('');
  };

  return (
    <section id="view-section">
      <div className="chat-wrapper">
        <div className="chat-section">
          <div className="chat-header">
            <h2>Team Chat</h2>
          </div>

          <div className="chat-box" ref={chatBoxRef}>
            {messages.length === 0 ? (
              <p>No messages yet. Start the conversation!</p>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`message ${msg.sender === username ? 'sent' : 'received'}`}
                >
                  <p><strong>{msg.sender}:</strong> {msg.message}</p>
                </div>
              ))
            )}
          </div>

          <form className="chat-input" onSubmit={sendMessage}>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
              autoComplete="off"
              required
            />
            <button type="submit">Send</button>
          </form>
        </div>
      </div>

      <footer style={{ textAlign: 'center', marginTop: '20px' }}>
        <p>&copy; 2025 I-Mind. All Rights Reserved.</p>
      </footer>
    </section>
  );
};

export default ChatApp;
