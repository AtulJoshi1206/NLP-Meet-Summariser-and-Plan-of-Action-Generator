import os
import openai
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from whisper import load_model
import streamlit as st
import base64

# Set the page configuration at the very beginning
st.set_page_config(page_title="Meeting Summarizer and Plan of Action", page_icon=":memo:", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for background color and background image
def set_background(image_file):
    bin_str = open(image_file, 'rb').read()
    data_uri = "data:image/png;base64," + base64.b64encode(bin_str).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{data_uri}");
            background-size: cover;
        }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to send email
def send_email(subject, message, from_addr, to_addrs, password):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)

    for to_addr in to_addrs:
        msg['To'] = to_addr
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)

    server.quit()

# Function to summarize and generate plan
def summarize_and_generate_plan(text, openai_api_key):
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

# Function to convert video to text and summarize
def convert_video_to_text_and_summarize(openai_api_key, video_file_path, sender_email, receiver_email, email_password):
    try:
        # Step 1: Extract audio and transcribe
        temporary_audio_file = "temp_audio.mp3"
        subprocess.run(["ffmpeg", "-i", video_file_path, "-vn", temporary_audio_file])
        model = load_model("base")
        result = model.transcribe(temporary_audio_file)
        text = result["text"]

        # Clean up temporary files
        os.remove(temporary_audio_file)

        # Step 2: Summarize and generate plan
        summary_and_plan = summarize_and_generate_plan(text, openai_api_key)

        # Step 3: Send email notification
        send_email("Summary and Plan of Action", summary_and_plan, sender_email, [receiver_email], email_password)
        return "Email sent successfully!"

    except Exception as e:
        return f'An error occurred: {e}'

# Main function to create Streamlit app
def main():
    # Title and header
    st.title("Meeting Summarizer and Plan of Action")
    st.markdown("---")

    # Set the background image
    set_background("D:/Study material/Python/Infosys_Internship/Task week 3 4/Complete/image.png")

    # File upload widget with specific type and label
    uploaded_file = st.file_uploader("Choose a video file (MP4, AVI, or OV)", type=['mp4', 'avi', 'ov'])

    if uploaded_file is not None:
        # Display video player
        st.video(uploaded_file)

        # Email sending section
        st.markdown("---")
        st.subheader("Send Meeting Summary via Email")
        st.write("Please enter recipient's email address:")
        receiver_email = st.text_input("Recipient Email Address")

        if st.button("Send Email"):
            if receiver_email:
                try:
                    # Credentials for sending email (replace with your actual credentials)
                    openai_api_key = ""
                    sender_email = ""
                    email_password = ""

                    # Save the uploaded file temporarily
                    with open("temp_video.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Convert video to text, summarize, and send email
                    result_message = convert_video_to_text_and_summarize(openai_api_key, "temp_video.mp4", sender_email, receiver_email, email_password)

                    st.success(result_message)
                    os.remove("temp_video.mp4")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please enter a valid email address")

if __name__ == "__main__":
    main()
