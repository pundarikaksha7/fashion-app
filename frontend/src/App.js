import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Profile from './pages/Profile';
import SavedPosts from './pages/SavedPosts';
import ForYou from './pages/ForYou';
import Search from './pages/Search';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <Navbar />
      <main className="max-w-5xl mx-auto p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile/:username" element={<Profile />} />
          <Route path="/saved" element={<SavedPosts />} />
          <Route path="/foryou" element={<ForYou />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </main>
    </Router>
  );
}
