import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const codespaceUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Fetching leaderboard from:', codespaceUrl);
        
        const response = await fetch(codespaceUrl);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fetched leaderboard data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading leaderboard...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Leaderboard</h2>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Username</th>
              <th>Total Calories</th>
              <th>Team</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center">No leaderboard data found.</td>
              </tr>
            ) : (
              leaderboard.map((entry, index) => (
                <tr key={entry.id}>
                  <td>
                    <span className={`badge ${
                      index === 0 ? 'bg-warning text-dark' :
                      index === 1 ? 'bg-secondary' :
                      index === 2 ? 'bg-danger' :
                      'bg-primary'
                    }`}>
                      #{index + 1}
                    </span>
                  </td>
                  <td><strong>{entry.username}</strong></td>
                  <td>
                    <strong>{entry.total_calories}</strong> calories
                  </td>
                  <td>{entry.team_name || 'N/A'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
