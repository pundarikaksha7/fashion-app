import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SignUp.css"; // Import external CSS

const SignUp = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "",
  });

  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (formData.password !== formData.password2) {
      setMessage("Passwords do not match.");
      return;
    }

    // Handle form submission logic (e.g., API request)
    console.log("Form submitted:", formData);
    setMessage("Sign Up Successful!");
    navigate("/Login");
  };

  return (
    <div className="wrapper">
      {/* Header Section */}
      <header className="header">
        <div className="header-container">
          <a href="/" className="logo">
            <h1>NAME: TBD</h1>
          </a>
          <div className="header-links">
            <button className="login-btn" onClick={() => navigate("/Login")}>
              Login
            </button>
          </div>
        </div>
      </header>

      {/* Sign Up Section */}
      <div className="signup-container">
        <h1 className="signup-title">Sign Up</h1>
        {message && <p className="error-message">{message}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            className="input-field"
            value={formData.username}
            onChange={handleChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="input-field"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="input-field"
            value={formData.password}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password2"
            placeholder="Confirm Password"
            className="input-field"
            value={formData.password2}
            onChange={handleChange}
          />
          <button type="submit" className="signup-btn">
            Sign Up
          </button>
        </form>
        <p className="login-link">
          Already have an account? <a href="/Login">Login</a>
        </p>
      </div>

      {/* Footer Section */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-links">
            <a href="#">About</a>
            <a href="#">Help</a>
            <a href="#">Terms</a>
            <a href="#">Privacy</a>
          </div>
          <p className="copyright">© 2025 by NAME: TBD</p>
        </div>
      </footer>
    </div>
  );
};

export default SignUp;
