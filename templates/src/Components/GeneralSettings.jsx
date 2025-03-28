import React from "react";
import ProfileImageUpload from "./ProfileImageUpload";
import BioUpdate from "./BioUpdate";
import LocationUpdate from "./LocationUpdate";

const GeneralSettings = ({ user, setUser }) => {
  return (
    <div className="bg-white rounded-md lg:shadow-lg shadow col-span-2 p-6">
      <h3 className="text-xl mb-2">General</h3>
      <ProfileImageUpload user={user} setUser={setUser} />
      <BioUpdate user={user} setUser={setUser} />
      <LocationUpdate user={user} setUser={setUser} />

      <div className="bg-gray-10 p-6 pt-0 flex justify-end space-x-3">
        <button className="p-2 px-4 rounded bg-gray-50 text-red-500">
          <a href="/">Cancel</a>
        </button>
        <button className="button bg-blue-700">Save</button>
      </div>
    </div>
  );
};

export default GeneralSettings;
