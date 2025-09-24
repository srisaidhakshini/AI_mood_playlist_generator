// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mood, setMood] = useState('');
  const [playlist, setPlaylist] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!mood.trim()) return; // Prevent empty submissions
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/generate-playlist', { mood });
      setPlaylist(response.data.tracks || []);
    } catch (error) {
      console.error("Error fetching playlist:", error);
      alert("Failed to generate playlist. Check the console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>AI Mood Playlist</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          placeholder="Enter your mood (e.g., chill evening)"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </form>
      {playlist.length > 0 ? (
        <ul>
          {playlist.map((track, index) => (
            <li key={index}>
              <img src={track.albumArt || '/placeholder.jpg'} alt={track.name} />
              <span>{track.name} by {track.artist}</span>
              {track.preview_url && (
                <a href={track.preview_url} target="_blank" rel="noopener noreferrer">
                  Play Preview
                </a>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>No playlist yet. Enter a mood to start!</p>
      )}
    </div>
  );
}

export default App;