import React, { useState } from 'react';
import './App.css';

function App() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    gpa: '',
    interests: '',
    projects: '',
    extracurriculars: '',
    about: ''
  });
  const [suggestion, setSuggestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuggestion('');

    try {
      const response = await fetch('/api/counsel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSuggestion(data.suggestion);
    } catch (err) {
      console.error("Failed to get suggestion:", err);
      setError(err.message || 'Failed to fetch suggestion. Make sure the backend is running and the API key is set.');
    }
    setIsLoading(false);
  };

  const handleGetStarted = () => {
    setShowForm(true);
  };

  if (!showForm) {
    return (
      <div className="App hero-section">
        <div className="hero-content">
          <h1>College Ikigai</h1>
          <h2>Not all who wander are lost...find your dream college today</h2>
          <p className="hero-description">
            Discover colleges where you have the best chance of admission based on your academic profile, interests, and achievements.
          </p>
          <button onClick={handleGetStarted} className="hero-button">
            GET STARTED
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Career Counsellor</h1>
        <p>Find your perfect college match with AI-powered guidance.</p>
      </header>
      <main className="App-main">
        <form onSubmit={handleSubmit} className="profile-form">
          <h2>Tell Us About Yourself</h2>
          
          <div className="form-group">
            <label htmlFor="gpa">High School GPA:</label>
            <input type="text" id="gpa" name="gpa" value={formData.gpa} onChange={handleChange} placeholder="e.g., 3.8" />
          </div>

          <div className="form-group">
            <label htmlFor="interests">Interests/Hobbies:</label>
            <textarea id="interests" name="interests" value={formData.interests} onChange={handleChange} placeholder="e.g., Coding, Robotics, Debating, Painting"></textarea>
          </div>

          <div className="form-group">
            <label htmlFor="projects">Projects Undertaken:</label>
            <textarea id="projects" name="projects" value={formData.projects} onChange={handleChange} placeholder="e.g., Developed a weather app, Built a line-following robot"></textarea>
          </div>

          <div className="form-group">
            <label htmlFor="extracurriculars">Extracurricular Activities:</label>
            <textarea id="extracurriculars" name="extracurriculars" value={formData.extracurriculars} onChange={handleChange} placeholder="e.g., President of Science Club, Varsity Soccer Team Captain"></textarea>
          </div>

          <div className="form-group">
            <label htmlFor="about">A Little About Yourself:</label>
            <textarea id="about" name="about" value={formData.about} onChange={handleChange} placeholder="Briefly describe your aspirations, strengths, or anything else relevant."></textarea>
          </div>

          <button type="submit" disabled={isLoading} className="submit-button">
            {isLoading ? 'Getting Suggestions...' : 'Get College Suggestions'}
          </button>
        </form>

        {error && <div className="error-message">Error: {error}</div>}

        {suggestion && (
          <div className="suggestion-result">
            <h2>AI-Powered College Suggestions:</h2>
            <pre>{suggestion}</pre>
          </div>
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; 2024 Career Counsellor</p>
      </footer>
    </div>
  );
}

export default App;
