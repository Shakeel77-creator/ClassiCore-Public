import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = () => {

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('<EC2-IP>/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: input }),
      });

      const result = await response.json();

      if (result?.data?.length) {
        const botMessage = {
          role: 'bot',
          content: result.data, // an array
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: 'bot', content: '❌ No results found.' },
        ]);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: '⚠️ Something went wrong.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      {/* Message display */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} role={msg.role} content={msg.content} />
        ))}
        {isLoading && <MessageBubble role="bot" content="loading" />}
        <div ref={chatEndRef} />
      </div>

      {/* Input box */}
      <div className="border-t py-3 flex justify-center bg-white">
        <div className="flex w-full max-w-3xl px-4">
          <input
            type="text"
            className="flex-grow border border-gray-300 rounded-lg px-4 py-2 mr-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button
            onClick={handleSend}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
