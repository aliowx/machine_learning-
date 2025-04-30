import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <div className="app-container">
      <h1>Dashboard</h1>
      <p>Welcome to Panel Admin</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Dashboard;