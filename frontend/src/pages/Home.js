import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/posts/`)
      .then(res => setPosts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-semibold">Home Feed</h1>
      {posts.length === 0 ? (
        <p className="text-gray-500">No posts available.</p>
      ) : (
        posts.map(post => (
          <div key={post.id} className="border p-4 rounded-lg shadow">
            <h2 className="text-xl font-bold">{post.title}</h2>
            <p>{post.caption}</p>
            {post.image && <img src={post.image} alt={post.title} className="mt-2 rounded" />}
          </div>
        ))
      )}
    </section>
  );
}