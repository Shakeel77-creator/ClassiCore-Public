import React from 'react';

const MessageBubble = ({ role, content }) => {
  const isUser = role === 'user';

  const isStructuredBotMessage =
    !isUser &&
    (Array.isArray(content) ? content : [content]).every(item =>
      item.hasOwnProperty('matched_name') &&
      item.hasOwnProperty('predicted_code') &&
      item.hasOwnProperty('source') // confidence is optional
    );

    if (role === 'bot' && content === 'loading') {
      return (
        <div className="mb-4 flex justify-start">
          <div className="bg-white text-gray-800 px-4 py-3 rounded-lg shadow-md flex items-center space-x-2 animate-pulse">
            <span className="animate-spin text-2xl">⏳</span>
            <span className="font-medium">Classifying...</span>
          </div>
        </div>
      );
    }  

  return (
    <div className={`mb-4 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[75%] px-4 py-3 rounded-lg ${
          isUser ? 'bg-indigo-600 text-white' : 'bg-white text-gray-900 shadow-md'
        }`}
      >
        {isStructuredBotMessage ? (
          <div>
            <div className="text-xl font-semibold text-gray-800 mb-3">Top Matches</div>
            <div className="space-y-4">
              {(Array.isArray(content) ? content : [content]).map((item, idx) => (
                <div key={idx} className="bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm">
                  <div className="flex items-center mb-2 text-sm text-gray-800">
                    <span className="text-green-600 text-sm mr-2">✅</span>
                    <span>Match: {item.matched_name}</span>
                  </div>
                  <div className="flex items-center mb-2 text-sm">
                    <span className="bg-indigo-700 text-white text-xs font-semibold px-2 py-1 rounded mr-2">Code</span>
                    <span className="bg-gray-100 px-2 py-1 rounded text-sm">{item.predicted_code}</span>
                  </div>
                  <div className="mb-2">
                  <div className="mb-2">
                    {typeof item.confidence === 'number' && item.confidence > 0 && (
                      <>
                        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500"
                            style={{ width: `${Math.round(item.confidence * 100)}%` }}
                          ></div>
                        </div>
                        <div className="flex items-center mt-1 text-xs">
                          <span className="text-green-600 mr-2">
                            {(item.confidence * 100).toFixed(1)}% Confidence
                          </span>
                          <span className="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs font-medium">
                            {item.source}
                          </span>
                        </div>
                      </>
                    )}

                    {(item.confidence === undefined || item.confidence === 0) && (
                      <div className="flex items-center mt-1 text-xs">
                        <span className="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs font-medium">
                          {item.source}
                        </span>
                      </div>
                    )}
                  </div>


                  </div>
                </div>
              ))}
            </div>
          </div>

        ) : (
          <div className="whitespace-pre-wrap">{content}</div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
