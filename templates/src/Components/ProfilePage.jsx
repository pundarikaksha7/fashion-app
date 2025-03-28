import React from 'react'
import { useState } from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMapMarkerAlt } from "@fortawesome/free-solid-svg-icons";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { faHeart } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-solid-svg-icons";
import { faHome } from "@fortawesome/free-solid-svg-icons";
import './ProfilePage.css'
const dummyUserProfile = {
  
    user: { username: 'johndoe' },
    profileimg: '/assets/images/avatars/avatar-1.jpg',
    location: 'New York, USA',
    bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
  };
  
  const dummyStats = {
    posts: 12,
    followers: 150,
    following: 80,
  };
  
  const dummyUserPosts = [
    {
      id: 1,
      image: '/assets/images/posts/post-1.jpg',
      no_of_likes: 45,
      comments: [
        { id: 1, user: { username: 'alice' }, text: 'Awesome post!', created_at: '2025-03-21T08:30:00' },
        { id: 2, user: { username: 'bob' }, text: 'Love this!', created_at: '2025-03-21T09:00:00' },
      ],
    },
    {
      id: 2,
      image: '/assets/images/posts/post-2.jpg',
      no_of_likes: 32,
      comments: [
        { id: 3, user: { username: 'sam' }, text: 'Great pic!', created_at: '2025-03-20T10:15:00' },
      ],
    },
  ];
  
  const dummySuggestions = [
    { user: 'janedoe', profileimg: '/assets/images/avatars/avatar-2.jpg', bio: 'Fashion Enthusiast' },
    { user: 'mike', profileimg: '/assets/images/avatars/avatar-3.jpg', bio: 'Photographer' },
  ];
  
 
const ProfilePage = () => {
    const [modalPost, setModalPost] = useState(null); // currently open post modal

  // Handler to open a modal with a given post's details
  const openModal = (post) => {
    setModalPost(post);
    document.body.style.overflow = 'hidden'; // disable scrolling
  };

  const closeModal = () => {
    setModalPost(null);
    document.body.style.overflow = 'auto';
  };

  // A simple like toggle handler
  const toggleLike = (postId) => {
    // In a real app, you would update the like status via API.
    // For this demo, we simply update the dummy post.
    const updatedPosts = dummyUserPosts.map((post) =>
      post.id === postId
        ? { ...post, no_of_likes: post.no_of_likes + 1 } // Simulate incrementing like
        : post
    );
    // Normally you would update state. Here you might call an API.
    console.log('Toggle like for post:', postId, updatedPosts);
  };
  const [isFollowing, setIsFollowing] = useState(false); // Track follow state

  const handleFollowToggle = () => {
    setIsFollowing(!isFollowing); // Toggle follow/unfollow state
  };
  return (
    <div className="theme-layout">
    {/* Home Button */}
    <a href="/" className="home-btn">
    <FontAwesomeIcon icon={faHome} className="text-[#da334f] text-3xl" />
    </a>

    {/* Profile Header Section */}
    <section className="container" style={{ paddingTop: '60px' }}>
      <div className="profile-header">
        <div className="row">
          {/* Profile Image */}
          <div className="col-lg-3 col-md-4 text-center">
            <div className="profile-img-container">
              <img src={dummyUserProfile.profileimg} className="profile-img" alt="Profile" />
            </div>
          </div>
          {/* Profile Info */}
          <div className="col-lg-9 col-md-8">
            <h1 style={{ fontSize: '28px', marginBottom: '5px' }}>
              <b>@{dummyUserProfile.user.username}</b>
            </h1>
            {/* Profile Stats */}
            <div className="profile-stats">
              <div className="stat-box">
                <div className="stat-number">{dummyStats.posts}</div>
                <div className="stat-label">{dummyStats.posts === 1 ? 'Post' : 'Posts'}</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{dummyStats.followers}</div>
                <div className="stat-label">{dummyStats.followers === 1 ? 'Follower' : 'Followers'}</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{dummyStats.following}</div>
                <div className="stat-label">Following</div>
              </div>
            </div>
            {/* Location Info */}
            {dummyUserProfile.location && (
              <div style={{ marginTop: '10px' }}>
                <FontAwesomeIcon icon={faMapMarkerAlt} className="text-gray-500" />
                <span style={{ color: '#555', marginLeft: '5px' }}>{dummyUserProfile.location}</span>
              </div>
            )}
            {/* Action Buttons */}
            <div style={{ marginTop: '20px' }}>
              {/* For demonstration, we assume this is another user's profile */}
              <button
            className={`follow-btn ${isFollowing ? "unfollow" : ""}`}
            onClick={handleFollowToggle}
          >
            <FontAwesomeIcon icon={faPlus} className="text-blue-500 text-xl" />
            {isFollowing ? "Unfollow" : "Follow"}
          </button>
               
            </div>
          </div>
        </div>
      </div>
    </section>

    {/* Bio Section */}
    <section className="container">
      <div className="bio-section">
        <h2 className="section-title">About</h2>
        <div style={{ lineHeight: '1.6', color: '#444' }}>
          {dummyUserProfile.bio ? (
            dummyUserProfile.bio
          ) : (
            <p style={{ color: '#999', fontStyle: 'italic' }}>No bio available</p>
          )}
        </div>
      </div>
    </section>

    {/* Posts Section */}
    <section className="container" style={{ marginBottom: '50px' }}>
      <div style={{ backgroundColor: '#fff', borderRadius: '10px', padding: '20px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h2 className="section-title">Posts</h2>
        {dummyUserPosts.length > 0 ? (
          <div className="posts-grid">
            {dummyUserPosts.map((post) => (
              <div key={post.id} className="post-item" onClick={() => openModal(post)}>
                <img src={post.image} className="post-image" alt="Post" />
                <div className="post-overlay">
                  <div className="post-stats">
                  <FontAwesomeIcon icon={faHeart} className="text-red-500 text-2xl " />
                    <span>{post.no_of_likes}</span>
                    <FontAwesomeIcon icon={faComment} className="text-blue-400 text-2xl" />
                    <span>{post.comments.length}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <i className="fa fa-picture-o fa-4x" style={{ color: '#ddd' }}></i>
            <p style={{ color: '#999', marginTop: '10px' }}>No posts yet</p>
          </div>
        )}
      </div>
    </section>

    {/* Modal for Post Details */}
    {modalPost && (
      <div className="modal" onClick={(e) => { if (e.target.classList.contains('modal')) closeModal(); }}>
        <span className="close-btn" onClick={() => closeModal()}>&times;</span>
        <div className="modal-content">
          <div className="modal-image-container">
            <img src={modalPost.image} className="modal-image" alt="Post" />
          </div>
          <div className="modal-details">
            <div className="modal-header">
              <img src={dummyUserProfile.profileimg} className="modal-user-img" alt="User" />
              <h3>@{dummyUserProfile.user.username}</h3>
            </div>
            <div className="modal-caption">{/* Post caption can be added here if available */}</div>
            <div className="modal-stats">
              <div className="modal-likes">
                <i className="fa fa-heart"></i> <span>{modalPost.no_of_likes}</span> likes
              </div>
              <div className="modal-comments-count">
                <i className="fa fa-comment"></i> <span>{modalPost.comments.length}</span> comments
              </div>
            </div>
            <div className="interaction-section">
              <button className="like-btn" onClick={() => toggleLike(modalPost.id)}>
                <i className="fa fa-heart"></i> Like
              </button>
            </div>
            <div className="comments-list">
              {modalPost.comments.map((comment) => (
                <div key={comment.id} className="comment">
                  <p>
                    <strong>{comment.user.username}</strong>: {comment.text}
                  </p>
                  <small>{new Date(comment.created_at).toLocaleString()}</small>
                </div>
              ))}
            </div>
            {/* Add Comment Form (for demo, the form just logs the comment) */}
            <form
              className="comment-form"
              onSubmit={(e) => {
                e.preventDefault();
                // In a real app, submit the comment to the backend
                console.log('Comment submitted for post', modalPost.id);
                e.target.reset();
              }}
            >
              <textarea name="comment_text" placeholder="Add a comment..." required></textarea>
              <button type="submit" className="comment-btn">
                Post Comment
              </button>
            </form>
            <div className="created-time">Posted on {new Date().toLocaleDateString()}</div>
          </div>
        </div>
      </div>
    )}
  </div>
);
  
}

export default ProfilePage
