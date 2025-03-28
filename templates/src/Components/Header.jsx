import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ProfileDropdown from "./ProfileDropdown";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import SearchResults from "./SearchResults";
//import  "./assets/assets/images/avatars/avatar-1.jpg"
const sampleUsers = [
  { id: 1, username: "john_doe", bio: "Loves coding!", location: "New York", profileImg: "https://randomuser.me/api/portraits/men/1.jpg" },
  { id: 2, username: "jane_smith", bio: "React Developer", location: "San Francisco", profileImg: "https://randomuser.me/api/portraits/women/2.jpg" },
  { id: 3, username: "alex_dev", bio: "Crypto Enthusiast", location: "London", profileImg: "https://randomuser.me/api/portraits/men/3.jpg" }
];

const Header = () => {
  const navigate = useNavigate();
  const [searchResults, setSearchResults] = useState([]);
  const [ser, setSer] = useState("");

  // Debugging: Log the search term
  useEffect(() => {
    console.log("Current search:", ser);
    if (ser.trim()) {
      navigate(`/search/${ser}`);
    }
  }, [ser, navigate]);

  const handleSearch = (query) => {
    console.log("Searching for:", query);  // Debugging log
    setSer(query);  // Update the state
    if (query.trim() === "") {
      setSearchResults([]);
      return;
    }

    const filteredResults = sampleUsers.filter(user =>
      user.username.toLowerCase().includes(query.toLowerCase())
    );
    setSearchResults(filteredResults);
  };

  return (
    <header>
      <div className="header_inner flex justify-between items-center p-4">
        <div className="left-side flex items-center">
          <div id="logo" className="uk-hidden@s">
            <a href="/Home">
              <h1 style={{ textTransform: "uppercase" }}>NAME : TBD</h1>
            </a>
          </div>

          <div className="flex items-center border border-gray-300 rounded-lg overflow-hidden w-72">
            <input
              type="text"
              value={ser}
              onChange={(e) => handleSearch(e.target.value)}
              placeholder="Search..."
              className="px-3 py-2 w-full outline-none"
            />
            <button className="text-black px-4 py-2 ">
              <FontAwesomeIcon icon={faSearch} />
            </button>
          </div>
        </div>

        <div className="right-side lg:pr-4 flex items-center">
          <a
            href="#"
            className="bg-pink-500 flex font-bold hidden hover:bg-pink-600 hover:text-white items-center lg:block max-h-10 mr-4 px-4 py-2 rounded text-white"
          >
            <ion-icon name="add-circle" className="-mb-1 mr-1 opacity-90 text-xl"></ion-icon>
            Upload Pics
          </a>

          <button onClick={() => navigate("/Profile")}>
            <img
              src="./assets/assets/images/avatars/avatar-1.jpg"
              className="header-avatar rounded-full w-10 h-10"
              alt="Profile"
            />
          </button>

          <ProfileDropdown />
        </div>
      </div>

      {searchResults.length > 0 && <SearchResults results={searchResults} />}
    </header>
  );
};

export default Header;
