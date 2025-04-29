import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:8000/api/v1/login/', {
        email,
        password,
      });
      setMessage(response.data.message);
      localStorage.setItem('access_token', response.data.access_token);
    } catch (error) {
      setMessage(error.response?.data?.detail || "There is problem");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Login</h1>
      <form onSubmit={handleLogin} className="login-form">
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="enter your email"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'logging...' : 'login'}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;