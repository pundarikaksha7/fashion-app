import React from "react";
import "./style.css";

const SearchResults = ({ results = [] }) => {
  return (
    <div className="results-container">
      {results.length > 0 ? (
        results.map((user) => (
          <div key={user.id} className="result-item">
            <img
              src={user.profileImg}
              alt={user.username}
              className="profile-img"
            />
            <div>
              <h3>@{user.username}</h3>
              <p>{user.bio}</p>
              <p>
                <b>Location:</b> {user.location}
              </p>
            </div>
          </div>
        ))
      ) : (
        <p className="no-results">No users found.</p>
      )}
    </div>
  );
};

export default SearchResults; 
