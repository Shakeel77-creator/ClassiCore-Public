import React from 'react';
import ChatWindow from '../components/ChatWindow';
import Header from '../components/Header';

const Home = () => {
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header />
      <ChatWindow />
    </div>
  );
};

export default Home;
