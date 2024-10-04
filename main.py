#!/usr/bin/env python3

import time
import anki_vector
from anki_vector.util import degrees
from config import SCREEN_UPDATE_INTERVAL, LIFT_THRESHOLD
from Spotify import SpotifyClient  # Import the Spotify client module
from UI import UIGenerator  # Import the UI generator module


def main():
    """Main function to control Vector's interaction with Spotify."""
    
    # Parse command line arguments for Vector's serial
    args = anki_vector.util.parse_command_args()
    
    # Initialize Spotify client and UI generator
    spotify_client = SpotifyClient()  
    ui_generator = UIGenerator()  

    # Connect to Vector
    with anki_vector.Robot(args.serial) as robot:
        # Position Vector's head and lift for optimal viewing
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)

        # Initial state variables
        current_track_name = None  
        is_paused = False  
        
        # Set initial lift height to 40% (around 40 mm)
        robot.behavior.set_lift_height(0.4)
        time.sleep(1)  # Allow time for the lift to adjust
        baseline_lift_height = robot.lift_height_mm  
        print(f"Baseline lift height: {baseline_lift_height} mm")

        while True:
            # Check for touch to pause/resume the song
            if robot.touch.last_sensor_reading.is_being_touched:
                if is_paused:
                    spotify_client.resume_playback()
                    print("Resumed playback!")
                    is_paused = False
                else:
                    spotify_client.pause_playback()
                    print("Paused playback!")
                    is_paused = True

            # Disengage lift motor for manual movement
            robot.motors.set_lift_motor(0.0)

            # Get the current lift height in mm
            vec_lift = robot.lift_height_mm
            # Skip to the next song if the lift is raised significantly above baseline
            if vec_lift > (baseline_lift_height + LIFT_THRESHOLD):
                spotify_client.next_track()
                print("Skipped to the next track!")
                robot.behavior.set_lift_height(0.4)  # Reset lift to baseline
                time.sleep(0.5)  # Delay to avoid retriggering

            # Go back to the previous song if the lift is lowered significantly below baseline
            elif vec_lift < (baseline_lift_height - LIFT_THRESHOLD):
                spotify_client.previous_track()
                print("Went back to the previous track!")
                robot.behavior.set_lift_height(0.4)  # Reset lift to baseline
                time.sleep(0.5)  # Delay to avoid retriggering
            
            # Get the current track details from Spotify
            track_data = spotify_client.get_current_playback()
            
            if track_data:
                is_paused = False  # Reset the pause state
                track_name = track_data['track_name']
                                
                # Update the display if the track has changed
                if track_name != current_track_name:
                    current_track_name = track_name

                    # Perform a head animation to signal the song change
                    robot.behavior.set_head_angle(degrees(10.0))
                    robot.behavior.set_head_angle(degrees(45.0))

                    # Reset the scrolling offsets for track and artist names
                    ui_generator.reset_offsets()
                    print(f"Now playing: {track_name}")
                    
                # Generate and display the updated UI on Vector's screen
                ui_image = ui_generator.create_ui_image(track_data)
                screen_data = anki_vector.screen.convert_image_to_screen_data(ui_image)
                robot.screen.set_screen_with_image_data(screen_data, SCREEN_UPDATE_INTERVAL)

            else:
                # Display a default image if no track is playing
                is_paused = True  # Set the pause state to True
                default_image = ui_generator.create_default_image()
                screen_data = anki_vector.screen.convert_image_to_screen_data(default_image)
                robot.screen.set_screen_with_image_data(screen_data, SCREEN_UPDATE_INTERVAL)

            # Wait for the next update interval
            time.sleep(SCREEN_UPDATE_INTERVAL)


if __name__ == "__main__":
    try:
        main()  # Run the main function
    except Exception as e:
        print(f"An error occurred: {e}")
