# AI Mood Playlist Generator

## Overview
A web app that creates Spotify playlists by mood (e.g. "chill evening") from user input. It uses Gemini AI to interpret the mood, and the Spotify API to get track recommendations. The app displays the track name, artist name (links to their Spotify), album art, and listen preview—if available.

## Screenshot/Videos
![Main App Interface](screenshots/main-interface.png) 
*(Include a screenshot of the app with a playlist that it generated—see step 2 below)*

## Installation Instructions
### Backend
- Navigate to backend folder: `cd backend`
- Install required packages: `pip install -r requirements.txt`
- Run the backend server: `python app.py`
- Access backend via `http://localhost:5000`

### Frontend
- Navigate to frontend folder: `cd frontend`
- Install required packages: `npm install`
- Start the app: `npm start`
- Access frontend via `http://localhost:3000`

## Technology Stack
- Frontend - React.js
- Backend - Python with Flask
- APIs - Gemini AI, Spotify

## Completed Features
- User input of mood (e.g. "chill evening").
- Judgment of mood made by Gemini AI to compose a search query.
- Spotify API to return a maximum of 5 recommendation tracks that includes track name, artist name (link to artist on Spotify), album art, and preview URL.
- A simple responsive display for the playlist.
- Error handling to catch failed requests.
