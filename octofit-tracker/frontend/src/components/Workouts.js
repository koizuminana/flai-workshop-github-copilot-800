import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const codespaceUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Fetching workouts from:', codespaceUrl);
        
        const response = await fetch(codespaceUrl);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fetched workouts data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Workouts</h2>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th>Workout Name</th>
              <th>Activity Type</th>
              <th>Difficulty</th>
              <th>Duration (min)</th>
              <th>Calories</th>
              <th>Equipment</th>
              <th>Instructions</th>
            </tr>
          </thead>
          <tbody>
            {workouts.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center">No workouts found.</td>
              </tr>
            ) : (
              workouts.map((workout) => (
                <tr key={workout.id}>
                  <td><strong>{workout.name}</strong></td>
                  <td>{workout.activity_type || 'N/A'}</td>
                  <td>
                    <span className={`badge ${
                      workout.difficulty?.toLowerCase() === 'beginner' ? 'bg-success' :
                      workout.difficulty?.toLowerCase() === 'intermediate' ? 'bg-warning text-dark' :
                      workout.difficulty?.toLowerCase() === 'advanced' ? 'bg-danger' :
                      workout.difficulty?.toLowerCase() === 'expert' ? 'bg-dark' :
                      'bg-secondary'
                    }`}>
                      {workout.difficulty || 'Not specified'}
                    </span>
                  </td>
                  <td>{workout.duration}</td>
                  <td>{workout.calories_estimate || 'N/A'}</td>
                  <td>
                    {workout.equipment && workout.equipment.length > 0 ? (
                      <span className="badge bg-primary">
                        {workout.equipment.length} item{workout.equipment.length !== 1 ? 's' : ''}
                      </span>
                    ) : (
                      <span className="text-muted">None</span>
                    )}
                  </td>
                  <td>
                    {workout.instructions && workout.instructions.length > 0 ? (
                      <span className="badge bg-info text-dark">
                        {workout.instructions.length} step{workout.instructions.length !== 1 ? 's' : ''}
                      </span>
                    ) : (
                      <span className="text-muted">No instructions</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Workouts;
