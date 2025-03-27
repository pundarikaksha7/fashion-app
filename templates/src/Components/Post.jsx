import React from 'react'
import LikeButton from './LikeButton';
import Comments from './Comments';

const Post = ({post}) => {
    return (
        <div className="bg-white shadow rounded-md mx-2 lg:mx-0">
          {/* Post header */}
          <div className="flex justify-between items-center px-4 py-3">
            <div className="flex flex-1 items-center space-x-4">
              <img src={post.profile_image} className="bg-gray-200 rounded-full w-10 h-10" alt={post.user} />
              <span className="block font-semibold">
                <a href={`/profile/${post.user}`}>@{post.user}</a>
              </span>
            </div>
            <div className="relative">
              <a href="#">
                <i className="icon-feather-more-horizontal text-2xl hover:bg-gray-200 rounded-full p-2 transition"></i>
              </a>
              {/* More options dropdown */}
              <div
                className="bg-white w-56 shadow-md mx-auto p-2 mt-12 rounded-md text-gray-500 border border-gray-100 hidden"
                /* You can implement dropdown behavior with state */
              >
                <ul className="space-y-1">
                  <li>
                    <a href="#" className="flex items-center px-3 py-2 text-red-500 hover:bg-red-100 hover:text-red-500 rounded-md">
                      <i className="uil-trash-alt mr-1">Delete Post</i> 
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
    
          {/* Post image */}
          <div className="cursor-pointer" onClick={() => window.open(post.image, '_blank')}>
            <img src={post.image} alt="Post" className="w-full" />
          </div>
    
          {/* Post details */}
          <div className="py-3 px-4 space-y-3">
            <div className="flex space-x-4 lg:font-bold items-center">
              <LikeButton postId={post.id} initialLikes={post.no_of_likes} />
              <a href={post.image} download className="flex-1 flex justify-end">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8.5 1.5A1.5 1.5 0 0 1 10 0h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h6c-.314.418-.5.937-.5 1.5v6h-2a.5.5 0 0 0-.354.854l2.5 2.5a.5.5 0 0 0 .708 0l2.5-2.5A.5.5 0 0 0 10.5 7.5h-2v-6z" />
                </svg>
              </a>
            </div>
    
            {/* Post caption */}
            <p>
              <a href={`/profile/${post.user}`}>
                <strong>{post.user}</strong>
              </a>{' '}
              {post.caption}
            </p>
    
            {/* Comments Section */}
            <Comments post={post} />
          </div>
        </div>
      );
}

export default Post
