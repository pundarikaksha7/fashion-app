import React from 'react'

const Sidebar = ({suggestions}) => {
    return (
        <div className="bg-white shadow-md rounded-md overflow-hidden">
          <div className="bg-gray-50 border-b border-gray-100 flex items-baseline justify-between py-4 px-6">
            <h2 className="font-semibold text-lg">Users You Can Follow</h2>
          </div>
          <div className="divide-gray-300 divide-opacity-50 divide-y px-4">
            {suggestions.map((suggestion, index) => (
              <div className="flex items-center justify-between py-3" key={index}>
                <div className="flex flex-1 items-center space-x-4">
                  <a href={`/profile/${suggestion.user}`}>
                    <img src={suggestion.profileimg} alt={suggestion.user} className="bg-gray-200 rounded-full w-10 h-10" />
                  </a>
                  <div className="flex flex-col">
                    <span className="block capitalize font-semibold">{suggestion.user}</span>
                    <span className="block capitalize text-sm">{suggestion.bio}</span>
                  </div>
                </div>
                <a
                  href={`/Profile/${suggestion.user}`}
                  className="border border-gray-200 font-semibold px-4 py-1 rounded-full hover:bg-pink-600 hover:text-white hover:border-pink-600"
                >
                  View User
                </a>
              </div>
            ))}
          </div>
        </div>
      );
}

export default Sidebar
