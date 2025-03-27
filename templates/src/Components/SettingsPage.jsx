import React, { useState } from "react";
import GeneralSettings from "./GeneralSettings";
import "./style.css"; // Import your styles

const SettingsPage = () => {
  const [user, setUser] = useState({
    username: "johndoe",
    profileImg: "https://randomuser.me/api/portraits/men/1.jpg",
    bio: "Loves coding!",
    location: "New York",
  });

  return (
    <div className="container m-auto">
      <h1 className="text-2xl leading-none text-gray-900 tracking-tight mt-3">
        <a href="/">Home</a> / Account Setting for <b>{user.username}</b>
      </h1>
      <br />
      <hr />
      <div className="grid lg:grid-cols-3 mt-12 gap-8">
        <GeneralSettings user={user} setUser={setUser} />
      </div>
    </div>
  );
};

export default SettingsPage;
