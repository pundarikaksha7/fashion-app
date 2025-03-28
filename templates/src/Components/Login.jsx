import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Import external CSS

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === "test" && password === "password") {
      setMessage("Login successful!");
      navigate("/home");
    } else {
      setMessage("Invalid username or password.");
    }
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
            <button className="register-btn" onClick={() => navigate("/signup")}>
              Register
            </button>
          </div>
        </div>
      </header>

      {/* Login Section */}
      <div className="login-container">
        <h1 className="login-title">Log in</h1>
        {message && <p className="error-message">{message}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            className="input-field"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="input-field"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="login-btn">
            Login
          </button>
        </form>
        <p className="register-link">
          Not registered? <a href="/SignUp">Create an account</a>
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

export default Login;
