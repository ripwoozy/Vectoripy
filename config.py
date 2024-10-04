"""
Configuration module for Vector-Spotify Integration.

Contains all the necessary configuration variables such as API credentials,
file paths, and other constants used across the project.
"""

# -------------------- Spotify API --------------------


CLIENT_ID = 'CLIENT_ID' # Spotify API client ID
CLIENT_SECRET = 'CLIENT_SECRET' # Spotify API client secret
REDIRECT_URI = 'REDIRECT_URI' # Redirect URI for Spotify API

# Spotify API Scope for accessing user playback state and skipping to the next track 
SCOPE = 'user-read-playback-state user-modify-playback-state'

# -------------------- Vector Configuration --------------------

SCREEN_UPDATE_INTERVAL = 0.3  # Update interval in seconds

# Thresholds for detecting lift movement (up or down)
LIFT_THRESHOLD = 10  # Threshold for lift movement detection

# Image dimensions
IMAGE_WIDTH = 184
IMAGE_HEIGHT = 96

# Colors (RGB tuples)
BACKGROUND_COLOR = (0, 0, 0)        # Black background
TEXT_COLOR = (0, 128, 128)          # Teal text
PLACEHOLDER_COLOR = (70, 130, 180)  # SteelBlue for placeholder rectangle

# Font settings
FONT_FILENAME = 'Roboto-Regular.ttf'  # Font file name in the same directory
FONT_SIZE_TITLE = 18
FONT_SIZE_ARTIST = 13
FONT_SIZE_TIME = 14

# Text Animation
SCROLL_SPEED = 2  # Scroll speed in pixels per frame


# Album cover size and positions (x, y)
ALBUM_COVER_SIZE = (64, 64)
ALBUM_COVER_POSITION = (10, 10)
TRACK_NAME_POSITION = (80, 10)
ARTIST_NAME_POSITION = (80, 33)
PLAYBACK_TIME_POSITION = (80, 60)

# Placeholder text
PLACEHOLDER_TEXT = "No Image"
DEFAULT_MESSAGE = "No music playing"