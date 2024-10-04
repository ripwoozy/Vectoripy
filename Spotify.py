#!/usr/bin/env python3

"""
Spotify API Module.

Handles authentication with Spotify and fetching the current playback data.
Uses the Spotipy library for interacting with the Spotify Web API.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

class SpotifyClient:
    """
    SpotifyClient handles authentication and fetching current playback data from Spotify.
    """

    def __init__(self):
        """
        Initializes the Spotify client with authentication.
        """
        # Initialize Spotipy client with SpotifyOAuth for authentication
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE
        ))

    def get_current_playback(self):
        """
        Retrieves the current playback information from Spotify.

        Returns:
            dict or None: A dictionary containing track name, artist, album cover URL,
                          duration in milliseconds, and progress in milliseconds.
                          Returns None if no music is playing.
        """
        try:
            # Fetch current playback information
            playback = self.sp.current_playback()

            # Check if music is currently playing
            if playback and playback.get('is_playing'):
                track = playback.get('item')

                # Extract track details
                track_name = track.get('name')
                artists = track.get('artists', [])
                artist_names = ', '.join([artist.get('name') for artist in artists])
                album = track.get('album')
                album_images = album.get('images', [])

                # Get the highest resolution album cover image
                album_cover_url = album_images[0].get('url') if album_images else None

                duration_ms = track.get('duration_ms', 0)
                progress_ms = playback.get('progress_ms', 0)

                # Return the playback data as a dictionary
                return {
                    'track_name': track_name,
                    'artist': artist_names,
                    'album_cover_url': album_cover_url,
                    'duration_ms': duration_ms,
                    'progress_ms': progress_ms
                }
            else:
                # No music is playing
                return None

        except spotipy.SpotifyException as e:
            # Handle Spotify-specific exceptions
            print(f"Spotify API error: {e}")
            return None
        except Exception as e:
            # Handle general exceptions
            print(f"An error occurred while fetching playback data: {e}")
            return None

    def next_track(self):
        """
        Skips to the next track in the user's Spotify playback.
        """
        try:
            self.sp.next_track()
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while skipping track: {e}")

    def previous_track(self):
        """
        Skips to the previous track in the user's Spotify playback.
        """
        try:
            self.sp.previous_track()
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while going to the previous track: {e}")

    def pause_playback(self):
        """
        Pauses the user's Spotify playback.
        """
        try:
            self.sp.pause_playback()
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while pausing playback: {e}")

    def resume_playback(self):
        """
        Resumes the user's Spotify playback.
        """
        try:
            self.sp.start_playback()
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while resuming playback: {e}")

    def volume_up(self):
        """
        Increases the volume of the user's Spotify playback by 10%.
        """
        try:
            current_volume = self.sp.current_playback()['device']['volume_percent']
            new_volume = min(current_volume + 10, 100)  # Ensure volume does not exceed 100%
            self.sp.volume(new_volume)
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while increasing volume: {e}")

    def volume_down(self):
        """
        Decreases the volume of the user's Spotify playback by 10%.
        """
        try:
            current_volume = self.sp.current_playback()['device']['volume_percent']
            new_volume = max(current_volume - 10, 0)  # Ensure volume does not go below 0%
            self.sp.volume(new_volume)
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"An error occurred while decreasing volume: {e}")
