import subprocess
import openai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API key
openai.api_key = #use api key


def video_to_audio(video_path, audio_output_path):
    # Construct the FFmpeg command to extract audio from the video
    command = [
        'ffmpeg',  # The command to run FFmpeg
        '-i', video_path,  # Input file path (video)
        '-q:a', '0',  # Set the audio quality (0 is the highest)
        '-map', 'a',  # Select the audio stream
        audio_output_path,  # Output file path (audio)
        '-y'  # Automatically overwrite output files
    ]
    logging.info(f"Running command: {' '.join(command)}")
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"FFmpeg command failed with error: {result.stderr}")
    else:
        logging.info("Audio extraction completed successfully.")


def transcribe_audio(audio_path):
    # Read the audio file
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    # Transcribe the audio file using OpenAI's Whisper API
    logging.info("Transcribing audio...")
    response = openai.Audio.transcribe("whisper-1", audio_data)

    transcription = response['text']
    logging.info("Transcription completed.")
    # Return the transcribed text
    return transcription


def save_transcription_to_file(transcription, file_path):
    # Save the transcription to a text file
    with open(file_path, 'w') as file:
        file.write(transcription)
    logging.info(f"Transcription saved to {file_path}")


# Example usage
video_path = r'D:\Study material\Python\Infosys_Internship\Infosys Foundation – Restoring life to an ailing lake.mp4'
audio_output_path = r'D:\Study material\Python\Infosys_Internship\test2.mp3'
transcription_output_path = r'D:\Study material\Python\Infosys_Internship\transcribe1.txt'

# Convert video to audio
video_to_audio(video_path, audio_output_path)

# Transcribe audio to text
transcription = transcribe_audio(audio_output_path)

# Save transcription to a file
save_transcription_to_file(transcription, transcription_output_path)

logging.info("Transcription process completed.")
