import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Ensure CSS is imported if you added styling

function App() {
  const [mood, setMood] = useState('');
  const [playlist, setPlaylist] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/generate-playlist', { mood });
      setPlaylist(response.data.tracks || []);
    } catch (error) {
      setError('Failed to fetch playlist. Is the backend running?');
      console.error('Frontend error:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Mood Playlist Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          placeholder="Enter your mood (e.g., energetic workout)"
          style={{ padding: '10px', width: '300px' }}
        />
        <button type="submit" style={{ padding: '10px', marginLeft: '10px' }}>
          Generate Playlist
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {playlist.map((track, index) => (
          <li key={index}>
            {track.name} by {track.artist}{' '}
            {track.albumArt && (
              <img src={track.albumArt} alt="Album Art" width="50" style={{ marginRight: '10px' }} />
            )}
            {track.preview_url && <audio controls src={track.preview_url} style={{ marginLeft: '10px' }} />}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;