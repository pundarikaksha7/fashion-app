import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query.trim() === '') {
      setResults([]);
      return;
    }
    const delayDebounce = setTimeout(() => {
      axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/search/?q=${query}`)
        .then(res => setResults(res.data))
        .catch(err => console.error(err));
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [query]);

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold">Search</h1>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search posts or users..."
        className="w-full px-4 py-2 border rounded"
      />
      <div>
        {results.length === 0 ? <p>No results found.</p> : (
          results.map(result => (
            <div key={result.id} className="border p-3 rounded mt-2">
              <p>{result.caption || result.username}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}