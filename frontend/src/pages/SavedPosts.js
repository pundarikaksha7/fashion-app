import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function SavedPosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/saved/`)
      .then(res => setPosts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-semibold">Saved Posts</h1>
      {posts.length === 0 ? <p>No saved posts yet.</p> : (
        posts.map(post => (
          <div key={post.id} className="border p-4 rounded shadow">
            <h2 className="font-semibold">{post.title}</h2>
            <p>{post.caption}</p>
            {post.image && <img src={post.image} alt="Saved Post" className="mt-2 rounded" />}
          </div>
        ))
      )}
    </section>
  );
}