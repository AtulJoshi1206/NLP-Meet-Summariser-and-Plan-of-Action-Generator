import subprocess

def extract_audio_from_video(video_path, audio_path):
    ffmpeg_command = [
        'ffmpeg',
        '-i', video_path,  # Specify the input video file
        '-q:a', '0',  # Set the audio quality
        '-map', 'a',  # Extract the audio stream only
        audio_path  # Specify the output audio file
    ]
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Audio extracted successfully from {video_path} to {audio_path}")
    except subprocess.CalledProcessError as error:
        print(f"An error occurred: {error}")
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in system PATH.")
if __name__ == "__main__":
    video_path = input("Please provide the full path to the video file (including extension): ")
    output_filename = input("Please provide the desired name for the audio file (without extension): ")
    audio_extension = input("Please specify the audio format (e.g., mp3, wav, aac): ")

    # Form the complete output audio path
    audio_path = f"{output_filename}.{audio_extension}"
    # Call the function to perform the conversion
    extract_audio_from_video(video_path, audio_path)
