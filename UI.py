#!/usr/bin/env python3

"""
UI Builder Module.

Generates an image based on Spotify playback data, including album cover, track name,
artist, and playback time. Uses the Pillow library for image manipulation with a black 
background and teal-colored text.
"""

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
from config import (
    FONT_FILENAME, FONT_SIZE_TITLE, FONT_SIZE_ARTIST, FONT_SIZE_TIME, SCROLL_SPEED,
    ALBUM_COVER_POSITION, ALBUM_COVER_SIZE, TRACK_NAME_POSITION, 
    ARTIST_NAME_POSITION, PLAYBACK_TIME_POSITION, IMAGE_WIDTH, IMAGE_HEIGHT, 
    BACKGROUND_COLOR, TEXT_COLOR, PLACEHOLDER_COLOR, PLACEHOLDER_TEXT, DEFAULT_MESSAGE
)


class UIGenerator:
    """
    UIGenerator creates UI images based on Spotify playback data.
    """

    def __init__(self):
        """Initializes the UIGenerator with necessary fonts."""
        font_path = os.path.join(os.path.dirname(__file__), 'Fonts', FONT_FILENAME)
        try:
            self.font_title = ImageFont.truetype(font_path, FONT_SIZE_TITLE)
            self.font_artist = ImageFont.truetype(font_path, FONT_SIZE_ARTIST)
            self.font_time = ImageFont.truetype(font_path, FONT_SIZE_TIME)
            self.ARTIST_OFFSET = 0
            self.TRACK_OFFSET = 0
        except IOError:
            raise FileNotFoundError(f"Font file not found at {font_path}. Ensure the .ttf file is in the correct directory.")

    def fetch_album_cover(self, url):
        """
        Fetches the album cover image from the provided URL and resizes it.

        Args:
            url (str): URL of the album cover image.

        Returns:
            Image or None: Resized PIL Image object or None if fetching fails.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).resize(ALBUM_COVER_SIZE)
        except (requests.RequestException, Exception) as e:
            print(f"Failed to fetch album cover: {e}")
            return None

    @staticmethod
    def format_time(seconds):
        """
        Formats seconds into M:SS string.

        Args:
            seconds (int): Number of seconds.

        Returns:
            str: Formatted time string.
        """
        seconds = round(seconds)
        mins, secs = divmod(seconds, 60)
        return f"{mins}:{secs:02}"

    def marquee_text(self, draw, text, font, position, width, speed, offset):
        """
        Marquee scroll text continuously in a loop.

        Args:
            draw (ImageDraw): The ImageDraw object.
            text (str): The text to scroll.
            font (ImageFont): The font of the text.
            position (tuple): (x, y) position of the text.
            width (int): The available width for the text.
            speed (int): The speed of the scroll.
            offset (int): Current scroll offset.

        Returns:
            int: Updated scroll offset.
        """
        total_text_width = draw.textbbox((0, 0), text, font=font)[2]
        
        if total_text_width > (width - (ALBUM_COVER_SIZE[0] + ALBUM_COVER_POSITION[0] + ALBUM_COVER_POSITION[1])):
            offset = (offset + speed) % (total_text_width + width)
            current_x = position[0] - offset
            
            any_visible = False

            for char in text:
                char_width = draw.textbbox((0, 0), char, font=font)[2]
                if current_x + char_width > 85:  # Adjust this value as needed
                    draw.text((current_x, position[1]), char, font=font, fill=TEXT_COLOR)
                    any_visible = True
                current_x += char_width

            if not any_visible:
                offset = 0

            return offset
        else:
            draw.text(position, text, font=font, fill=TEXT_COLOR)
            return 0

    def reset_offsets(self):
        """
        Resets the scrolling offsets for track and artist names.
        """
        self.ARTIST_OFFSET = 0
        self.TRACK_OFFSET = 0

    def create_ui_image(self, playback_data):
        """
        Creates the UI image based on playback data.

        Args:
            playback_data (dict): Data containing track information.

        Returns:
            Image: Generated UI image.
        """ 
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        album_cover_url = playback_data.get('album_cover_url')
        album_cover = self.fetch_album_cover(album_cover_url) if album_cover_url else None

        if album_cover:
            img.paste(album_cover, ALBUM_COVER_POSITION)
        else:
            draw.rectangle(
                [ALBUM_COVER_POSITION, (ALBUM_COVER_POSITION[0] + ALBUM_COVER_SIZE[0], 
                                        ALBUM_COVER_POSITION[1] + ALBUM_COVER_SIZE[1])],
                fill=PLACEHOLDER_COLOR
            )
            bbox = draw.textbbox((0, 0), PLACEHOLDER_TEXT, font=self.font_time)
            text_x = ALBUM_COVER_POSITION[0] + (ALBUM_COVER_SIZE[0] - (bbox[2] - bbox[0])) // 2
            text_y = ALBUM_COVER_POSITION[1] + (ALBUM_COVER_SIZE[1] - (bbox[3] - bbox[1])) // 2
            draw.text((text_x, text_y), PLACEHOLDER_TEXT, font=self.font_time, fill=TEXT_COLOR)

        track_name = playback_data.get('track_name', 'Unknown Track')
        artist_name = playback_data.get('artist', 'Unknown Artist')
        
        self.TRACK_OFFSET = self.marquee_text(draw, track_name, self.font_title, TRACK_NAME_POSITION, IMAGE_WIDTH, SCROLL_SPEED, self.TRACK_OFFSET)
        self.ARTIST_OFFSET = self.marquee_text(draw, artist_name, self.font_artist, ARTIST_NAME_POSITION, IMAGE_WIDTH, SCROLL_SPEED, self.ARTIST_OFFSET)

        duration_sec = playback_data.get('duration_ms', 0) // 1000
        progress_sec = playback_data.get('progress_ms', 0) // 1000
        playback_time_text = f"{self.format_time(progress_sec)} / {self.format_time(duration_sec)}"
        draw.text(PLAYBACK_TIME_POSITION, playback_time_text, font=self.font_time, fill=TEXT_COLOR)

        return img

    def create_default_image(self):
        """
        Creates a default UI image when no music is playing.

        Returns:
            Image: PIL Image object representing the default UI.
        """
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        bbox = draw.textbbox((0, 0), DEFAULT_MESSAGE, font=self.font_title)
        position = ((IMAGE_WIDTH - (bbox[2] - bbox[0])) // 2, (IMAGE_HEIGHT - (bbox[3] - bbox[1])) // 2)
        draw.text(position, DEFAULT_MESSAGE, font=self.font_title, fill=TEXT_COLOR)

        return img
