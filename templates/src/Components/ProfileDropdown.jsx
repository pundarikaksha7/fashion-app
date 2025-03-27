import React, { useState } from "react";

const ProfileDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      {/* Dropdown Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="ml-2 bg-gray-700 text-black px-3 py-2 rounded-lg hover:bg-gray-600"
      >
        ▼
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white border rounded shadow-lg">
          <ul className="py-2">
            <li className="px-4 py-2 hover:bg-red-800">
              <a href="/Settings">Account Settings</a>
            </li>
            <li className="px-4 py-2 hover:bg-red-800">
              <a href="/Login">Log Out</a>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ProfileDropdown;
