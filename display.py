import pygame
import time
import cv2
from flask import Flask, request, json
from threading import Thread
import asyncio

# Initialize pygame
pygame.init()

# Define the screen dimensions (usually, you want fullscreen size)
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# List of video files
video_files = ["blink.mp4", "blush.mp4", "grin.mp4", "inquisitive.mp4", "suprised.mp4"]

# Define a function to play videos
def play_video(video_file):
    # Open the video file using OpenCV
    video_capture = cv2.VideoCapture(video_file)

    # Get video properties (fps, frame count, and size)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Loop through the frames of the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break  # Exit if no frames left

        # Convert frame from BGR (OpenCV format) to RGB (Pygame format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Rotate the frame if needed (to fix sideways issue)
        # This can happen if the video is in portrait mode, so we check its size
        # if video_width < video_height:
        frame = cv2.transpose(frame)  # Rotate frame by 90 degrees
        frame = cv2.flip(frame, flipCode=0)  # Flip frame horizontally (if needed)

        # Convert frame to a pygame surface
        frame_surface = pygame.surfarray.make_surface(frame)

        # Resize the frame to fit the screen while preserving aspect ratio
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

        # Display the frame on the screen
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        # Wait for the appropriate time per frame based on FPS
        time.sleep(1 / fps)

        # Exit if the user closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # Release the video capture once done
    video_capture.release()

# Function to loop through the videos
def play_videos_in_sequence():
    for video in video_files:
        play_video(video)
        time.sleep(0.5)  # Optional: delay between videos

# Function to loop all videos indefinitely
def play_videos_looped():
    while True:
        play_videos_in_sequence()

# Example to play the videos once
# play_videos_in_sequence()

# Example to play the videos in a loop
# play_videos_looped()

video_play_queue = []

def play_videos():
    count = 0
    prev_video = "inquisitive.mp4"
    while True: 
        if len(video_play_queue) == 0:
            if prev_video == "inquisitive.mp4":
                play_video("blink.mp4")
                if count >= 5: 
                    prev_video = "blink.mp4"
                    count = 0
                else:
                    count += 1
            else:
                play_video("inquisitive.mp4")
                prev_video = "inquisitive.mp4"
        else:
            play_video(video_play_queue.pop(0))




app = Flask(__name__)


# add_ipad_response POST request
@app.route('/event', methods = ['POST'])
def event_callback_api():
    if request.method == 'POST':
        data = json.loads(request.data)
    
        event_type = data['event_type']
        print(event_type)

        if event_type == "thermal-print":
            video_play_queue.append("grin.mp4")
        elif event_type == "color-print":
            video_play_queue.append("suprised.mp4")
        elif event_type == "submit":
            video_play_queue.append("blush.mp4")
    return "succes"

def thread_flack():
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run(host='0.0.0.0', port=50299, debug=False) 



if __name__ == '__main__':
    Thread(target=thread_flack, daemon=True).start()


    play_videos()
# Close pygame window
pygame.quit()
