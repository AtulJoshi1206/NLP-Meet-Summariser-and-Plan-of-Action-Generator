import os
import openai
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from whisper import load_model
import msal
import requests

# Application (client) ID, client secret, and tenant ID
client_id = ''
client_secret = ''
tenant_id = ''
site_id = ''
drive_id = ''


def authenticate():
    authority = f'/{tenant_id}'
    scope = ['']

    app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    token_response = app.acquire_token_for_client(scopes=scope)

    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        raise Exception('Authentication failed')


def get_file_id(access_token, filename='s1.mp4'):
    list_items_endpoint = f''

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(list_items_endpoint, headers=headers)
    items = response.json().get('value', [])

    for item in items:
        if item['name'] == filename:
            return item['id']

    raise Exception(f'File {filename} not found')


def download_file(access_token, file_id, output_filename='s1.mp4'):
    download_endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{file_id}/content'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(download_endpoint, headers=headers, stream=True)

    with open(output_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f'File {output_filename} downloaded successfully')


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


def convert_video_to_text_and_summarize(openai_api_key, sender_email, receiver_email, email_password):
    """Downloads video from OneDrive, converts to text, summarizes, and sends an email."""

    try:
        # Step 1: Authenticate
        access_token = authenticate()

        # Step 2: Get file ID of 's1.mp4'
        file_id = get_file_id(access_token)

        # Step 3: Download the file
        local_file_path = 's1.mp4'
        download_file(access_token, file_id, local_file_path)

        # Step 4: Extract audio and transcribe
        temporary_audio_file = "temp_audio.mp3"
        subprocess.run(["ffmpeg", "-i", local_file_path, "-vn", temporary_audio_file])
        model = load_model("base")
        result = model.transcribe(temporary_audio_file)
        text = result["text"]

        # Clean up temporary files
        os.remove(temporary_audio_file)

        # Step 5: Summarize and generate plan
        summary_and_plan = summarize_and_generate_plan(text, openai_api_key)

        # Step 6: Send email notification
        send_email(summary_and_plan, sender_email, receiver_email, email_password)

    except Exception as e:
        print(f'An error occurred: {e}')


# Example usage (replace with your actual credentials)
openai_api_key = ""
sender_email = ""
receiver_email = ""
email_password = ""

convert_video_to_text_and_summarize(openai_api_key, sender_email, receiver_email, email_password)