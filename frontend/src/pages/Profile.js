import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function Profile() {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/profile/${username}/`)
      .then(res => setProfile(res.data))
      .catch(err => console.error(err));

    axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/profile/${username}/posts/`)
      .then(res => setPosts(res.data))
      .catch(err => console.error(err));
  }, [username]);

  return (
    <section className="space-y-6">
      {profile ? (
        <div className="border p-4 rounded shadow">
          <h1 className="text-2xl font-bold">{profile.name}</h1>
          <p className="text-gray-600">@{profile.username}</p>
        </div>
      ) : <p>Loading profile...</p>}

      <div>
        <h2 className="text-xl font-semibold">Posts</h2>
        {posts.length === 0 ? <p>No posts yet.</p> : (
          posts.map(post => (
            <div key={post.id} className="border p-4 rounded mt-2">
              <h3 className="font-semibold">{post.title}</h3>
              <p>{post.caption}</p>
              {post.image && <img src={post.image} alt="Post" className="mt-2 rounded" />}
            </div>
          ))
        )}
      </div>
    </section>
  );
}