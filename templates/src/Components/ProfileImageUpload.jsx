import React from "react";

const ProfileImageUpload = ({ user, setUser }) => {
  const handleImageChange = (e) => {
    const file = URL.createObjectURL(e.target.files[0]);
    setUser({ ...user, profileImg: file });
  };

  return (
    <div className="col-span-2">
      <label>Profile Image</label>
      <img width="100" height="100" src={user.profileImg} alt="Profile" />
      <input type="file" onChange={handleImageChange} className="shadow-none bg-gray-100" />
    </div>
  );
};

export default ProfileImageUpload;
