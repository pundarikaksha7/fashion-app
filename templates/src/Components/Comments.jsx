import React from 'react'
import {useState} from 'react'
const Comments = ({post}) => {
    const [commentText, setCommentText] = useState('');
    const [comments, setComments] = useState(post.comments);
  
    const handleCommentSubmit = (e) => {
      e.preventDefault();
      // In a real app, post the comment to the backend.
      // For now, we simulate adding a new comment:
      const newComment = {
        id: Date.now(),
        user: { username: 'current_user', profileimg: '/assets/images/avatars/avatar-1.jpg' },
        text: commentText,
        created_at: new Date().toISOString()
      };
      setComments([...comments, newComment]);
      setCommentText('');
    };
  
    return (
      <div className="border-t pt-4 space-y-4">
        {comments.map((comment) => (
          <div className="flex items-start space-x-2" key={comment.id}>
            <img src={comment.user.profileimg} alt={comment.user.username} className="w-8 h-8 rounded-full" />
            <div>
              <p className="text-sm">
                <strong>{comment.user.username}</strong> {comment.text}
              </p>
              <span className="text-xs text-gray-500">
                {new Date(comment.created_at).toLocaleString()}
              </span>
            </div>
          </div>
        ))}
        <form onSubmit={handleCommentSubmit} className="mt-3 flex items-center">
          <input
            type="text"
            name="comment_text"
            className="flex-1 border rounded-lg py-2 px-3 text-sm"
            placeholder="Add a comment..."
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            required
          />
          <button type="submit" className="ml-2 bg-blue-500 text-white text-sm py-2 px-4 rounded-lg hover:bg-blue-600">
            Post
          </button>
        </form>
      </div>
    );
}

export default Comments
