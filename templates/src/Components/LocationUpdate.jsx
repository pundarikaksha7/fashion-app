import React from "react";

const LocationUpdate = ({ user, setUser }) => {
  return (
    <div className="col-span-2">
      <label>Location</label>
      <input
        type="text"
        className="shadow-none bg-gray-100"
        value={user.location}
        onChange={(e) => setUser({ ...user, location: e.target.value })}
      />
    </div>
  );
};

export default LocationUpdate;
