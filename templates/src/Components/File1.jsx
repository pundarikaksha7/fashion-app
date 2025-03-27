import React from 'react'
import { useState } from 'react';
import Header from "./Header";
import Post from "./Post";
import Sidebar from "./Sidebar"
const dummyPosts = [
    {
      id: 1,
      user: 'john_doe',
      profile_image: '/assets/images/avatars/avatar-1.jpg',
      caption: 'A beautiful sunrise!',
      image: '/assets/images/posts/post-1.jpg',
      no_of_likes: 3,
      comments: [
        {
          id: 1,
          user: { username: 'alice', profileimg: '/assets/images/avatars/avatar-2.jpg' },
          text: 'Wow, amazing shot!',
          created_at: '2025-03-20T08:30:00'
        },
        // ... more comments
      ]
    },
    // ... more posts
  ];
  
  const dummySuggestions = [
    {
      user: 'jane_doe',
      profileimg: '/assets/assets/images/avatars/avatar-1.jpg',
      bio: 'Fashion Enthusiast'
    },
    // ... more suggestions
  ];
const File1 = () => {
      const [posts, setPosts] = useState(dummyPosts);
      const [suggestions, setSuggestions] = useState(dummySuggestions);
    
      return (
        <div>
          <Header />
          <div className="container m-auto">
            <div className="lg:flex justify-center lg:space-x-10 lg:space-y-0 space-y-5">
              {/* Left Side - Posts */}
              <div className="space-y-5 flex-shrink-0 lg:w-7/12">
                {posts.map((post) => (
                  <Post key={post.id} post={post} />
                ))}
              </div>
    
              {/* Right Side - Suggestions */}
              <div className="lg:w-5/12">
                <Sidebar suggestions={suggestions} />
              </div>
            </div>
          </div>
        </div>
      );
}

export default File1
