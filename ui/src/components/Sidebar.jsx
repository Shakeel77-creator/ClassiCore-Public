import React, { useState } from 'react';
import { FaPlus, FaTrash } from 'react-icons/fa';

const Sidebar = () => {
  const [chats, setChats] = useState([
    { id: 1, name: 'New Chat 1' }
  ]);
  const [editingChatId, setEditingChatId] = useState(null);

  const addChat = () => {
    const newId = Date.now(); // or use uuid
    setChats([...chats, { id: newId, name: 'New Chat' }]);
    setEditingChatId(newId); // auto focus the new one
  };

  const deleteChat = (id) => {
    setChats(chats.filter(chat => chat.id !== id));
    if (editingChatId === id) setEditingChatId(null);
  };

  const handleRename = (id, newName) => {
    setChats((prevChats) =>
      prevChats.map((chat) =>
        chat.id === id
          ? { ...chat, name: newName.trim() || chat.name }
          : chat
      )
    );
    setEditingChatId(null);
  };

  return (
    <div className="w-64 bg-white border-r h-full p-4 flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <span className="text-lg font-semibold text-purple-700">Chats</span>
        <button onClick={addChat} className="text-purple-700 hover:text-purple-900">
          <FaPlus />
        </button>
      </div>

      <div className="space-y-2 overflow-y-auto">
        {chats.map((chat) => (
          <div key={chat.id} className="flex items-center group">
            {editingChatId === chat.id ? (
              <input
                type="text"
                defaultValue={chat.name}
                autoFocus
                onBlur={(e) => handleRename(chat.id, e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleRename(chat.id, e.target.value);
                  }
                }}
                className="flex-grow px-2 py-1 border rounded text-sm"
              />
            ) : (
              <div
                onClick={() => setEditingChatId(chat.id)}
                className="flex-grow px-2 py-1 rounded text-sm cursor-pointer hover:bg-gray-100"
              >
                {chat.name}
              </div>
            )}

            <button
              onClick={() => deleteChat(chat.id)}
              className="text-gray-400 hover:text-red-500 ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Delete"
            >
              <FaTrash size={12} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
