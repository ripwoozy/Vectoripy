[![Banner](Assets/Logo.jpg)](https://github.com/ripwoozy/)
[![Language](https://img.shields.io/badge/Language-Python-4B8BBE)](https://wiki.python.org/moin/BeginnersGuide)
[![License](https://img.shields.io/badge/License-MIT-239120)](#-license)
[![Reddit](https://img.shields.io/badge/Reddit-Anki%20Vector-FF4500?logo=reddit)](https://www.reddit.com/r/AnkiVector/)
![GitHub stars](https://img.shields.io/github/stars/ripwoozy/Vectoripy?style=social)

**Vectoripy** is a Python project that seamlessly integrates the Anki Vector robot with the Spotify API, allowing Vector to display real-time track info, including album art, and control playback with gestures!

**Leave a ⭐ if you find this project interesting! It's a great way to show your support and help others find it.**


## Features ✨
- Displays album cover and track information.
- Skip to the next or previous track using Vector's lift **(Requires Vector to be on the charger)**.
- Pause and resume playback with Vector's touch sensor.
- Handles Spotify playback updates in real-time.


## Requirements 📦
- **Python 🐍:** 3.7+
- **Anki Vector SDK 📃:** Follow the [Installation Guide](https://github.com/kercre123/wirepod-vector-python-sdk)
- **Spotify API 🎵:** Utilize the [Spotipy Module](https://spotipy.readthedocs.io/en/2.24.0/) for interacting with the Spotify API

## Installation 🔧

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Vectoripy.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Vectoripy
    ```

3. Follow the [Anki Vector SDK installation guide](https://github.com/kercre123/wirepod-vector-python-sdk) for instructions on how to set up the Anki Vector SDK.

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Set up Spotify API credentials:

    Get your CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI from your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

    Add these credentials to a config.py file:
    
    ```python
        CLIENT_ID = 'your-client-id'
        CLIENT_SECRET = 'your-client-secret'
        REDIRECT_URI = 'your-redirect-uri'
    ```

## Usage 🚀

1. Turn on your Anki Vector robot and ensure it's connected to your SDK.

2. Run the main script:
    ```bash
    python main.py
    ```
3. Vector will display the album cover and track information of the currently playing song on your Spotify account <details> <summary> Showcase </summary> <img src="Assets/sosa.jpg" alt="Vector playing music" width="400" height="400"> </details>

4. Lift Vector's arm to skip to the next track or lower it to go back to the previous track.<details> <summary> Showcase </summary> <img src="Assets/vector-player.gif" alt="Vector skipping song " width="400"> </details>

5. Tap Vector's touch sensor to pause or resume playback.

6. Enjoy your music with Vector! 🎶
️
## Contributing 🤝
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License 📝
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
