import React from "react";

const BioUpdate = ({ user, setUser }) => {
  return (
    <div className="col-span-2">
      <label>Bio</label>
      <textarea
        rows="3"
        className="shadow-none bg-gray-100"
        value={user.bio}
        onChange={(e) => setUser({ ...user, bio: e.target.value })}
      />
    </div>
  );
};

export default BioUpdate;
