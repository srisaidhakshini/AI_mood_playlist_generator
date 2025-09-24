from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables with validation
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check for missing credentials
if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GEMINI_API_KEY]):
    raise ValueError("Missing one or more API credentials in .env file")

# Initialize Spotipy client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
except Exception as e:
    raise ValueError(f"Failed to initialize Spotify client: {e}")

# Gemini API configuration
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    raise ValueError(f"Failed to configure Gemini API: {e}")

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/generate-playlist', methods=['POST'])
def generate_playlist():
    try:
        data = request.json
        if not data or 'mood' not in data:
            return jsonify({'error': 'Mood is required'}), 400
        
        mood = data.get('mood', '')
        if not mood:
            return jsonify({'error': 'Mood cannot be empty'}), 400
        
        # Use Gemini to refine mood
        prompt = f"Convert the mood '{mood}' into a single concise Spotify search query with genres or keywords (max 200 characters)."
        try:
            response = model.generate_content(prompt)
            search_query = getattr(response, 'text', '').strip()
            # Extract the first valid query (e.g., between backticks or first line)
            match = re.search(r'`([^`]+)`|\b\w+\b', search_query)
            search_query = match.group(1) if match and match.group(1) else mood
            search_query = search_query[:200].strip()  # Limit to 200 characters
        except Exception as e:
            print(f"Gemini error: {e}")
            search_query = mood  # Fallback to raw mood

        print(f"Search query: {search_query}")  # Debug log

        # Search Spotify with error handling
        try:
            results = sp.search(q=search_query, type='track', limit=5)
            if 'tracks' not in results or 'items' not in results['tracks']:
                raise ValueError("Invalid Spotify API response")
            tracks = []
            for item in results['tracks']['items']:
                track = {
                    'name': item.get('name', 'Unknown'),
                    'artist': item['artists'][0].get('name', 'Unknown') if item.get('artists') else 'Unknown',
                    'albumArt': item['album']['images'][0].get('url', '') if item.get('album', {}).get('images') else '',
                    'preview_url': item.get('preview_url', '')
                }
                tracks.append(track)
        except Exception as e:
            print(f"Spotify error: {e}")
            return jsonify({'error': 'Failed to fetch tracks from Spotify'}), 500

        return jsonify({'tracks': tracks})
    except Exception as e:
        print(f"Backend error: {e}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)