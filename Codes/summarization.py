import os
import openai
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from whisper import load_model

def summarize_and_generate_plan(text, openai_api_key):
    """Summarizes text and generates a plan of action using OpenAI."""
    openai.api_key = openai_api_key
    prompt = (
        "Summarize the following meeting transcript and generate a plan of action with a maximum of 5 points:\n\n"
        f"{text}\n\n"
        "Summary:\n\n"
        "Plan of Action (5 points):\n"
    )
    client = openai.Client(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    summary_and_plan = response.choices[0].message.content.strip()

    return summary_and_plan

def send_email(summary_and_plan, sender_email, receiver_email, email_password):
    """Sends an email with the provided message."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Summary and Plan of Action"
    msg.attach(MIMEText(summary_and_plan, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')
    finally:
        server.quit()

def convert_video_to_text_and_summarize(local_file_path, openai_api_key, sender_email, receiver_email, email_password):
    """Converts video to text, summarizes, and sends an email."""
    downloaded_video_path = local_file_path

    # Extract audio and transcribe
    temporary_audio_file = "temp_audio.mp3"
    subprocess.run(["ffmpeg", "-i", downloaded_video_path, "-vn", temporary_audio_file])
    model = load_model("base")
    result = model.transcribe(temporary_audio_file)
    text = result["text"]

    # Clean up temporary files
    os.remove(temporary_audio_file)

    # Summarize and generate plan
    summary_and_plan = summarize_and_generate_plan(text, openai_api_key)

    # Send email notification
    send_email(summary_and_plan, sender_email, receiver_email, email_password)

# Example usage (replace with your actual local file path and credentials)
local_file_path = "D:\\Study material\\Python\\Infosys_Internship\\A one minute TEDx Talk for the digital age _ Woody Roseland _ TEDxMileHigh.mp4"
openai_api_key = ""
sender_email = ""
receiver_email = ""
email_password = ""

convert_video_to_text_and_summarize(local_file_path, openai_api_key, sender_email, receiver_email, email_password)
