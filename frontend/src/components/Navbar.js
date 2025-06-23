import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md py-4 px-6 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold text-gray-800">Fashion App</Link>
      <div className="space-x-4">
        <Link to="/foryou" className="text-gray-600 hover:text-gray-900">For You</Link>
        <Link to="/search" className="text-gray-600 hover:text-gray-900">Search</Link>
        <Link to="/saved" className="text-gray-600 hover:text-gray-900">Saved</Link>
        <Link to="/profile/testuser" className="text-gray-600 hover:text-gray-900">Profile</Link>
      </div>
    </nav>
  );
}