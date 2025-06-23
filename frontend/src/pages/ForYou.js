import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ForYou() {
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/foryou/`)
      .then(res => setSuggestions(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-semibold">For You</h1>
      {suggestions.length === 0 ? <p>No suggestions available.</p> : (
        suggestions.map(suggestion => (
          <div key={suggestion.id} className="border p-4 rounded shadow">
            <p className="font-semibold">{suggestion.text}</p>
          </div>
        ))
      )}
    </section>
  );
}