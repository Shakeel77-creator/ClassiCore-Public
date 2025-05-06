import React from 'react';

const FeedbackModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-96 shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Submit Feedback</h2>
        <form className="space-y-3">
          <input
            type="text"
            placeholder="Name"
            className="w-full border border-gray-300 p-2 rounded"
          />
          <input
            type="email"
            placeholder="Email"
            className="w-full border border-gray-300 p-2 rounded"
          />
          <textarea
            placeholder="Enter your feedback"
            className="w-full border border-gray-300 p-2 rounded h-24"
          />
          <input type="file" className="w-full" />
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-purple-700 text-white px-4 py-2 rounded hover:bg-purple-800"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default FeedbackModal;
