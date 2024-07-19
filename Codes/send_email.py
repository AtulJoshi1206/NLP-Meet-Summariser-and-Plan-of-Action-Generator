from email import encoders
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(sender_email, sender_password, recipient_email, subject, body, attachments=[]):
    """
    Sends an email with the specified subject, body, and attachments.

    :param sender_email: Sender's email address
    :param sender_password: Sender's email password
    :param recipient_email: Recipient's email address
    :param subject: Subject of the email
    :param body: Body of the email
    :param attachments: List of file paths to attach
    :return: None
    """
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach any files
    for attachment in attachments:
        with open(attachment, 'rb') as file:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(file.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
            msg.attach(mime_base)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    import getpass

    sender_email = input("Enter your email: ")
    sender_password = getpass.getpass("Enter your email password: ")
    recipient_email = input("Enter the recipient's email: ")
    subject = "Summary and Plan of Action"

    # Read the summary and plan of action from files
    summary_file = input("Enter the path to the summary file: ")
    plan_of_action_file = input("Enter the path to the plan of action file: ")

    try:
        with open(summary_file, 'r', encoding='utf-8') as file:
            summary_content = file.read()
    except FileNotFoundError:
        print(f"Summary file '{summary_file}' not found.")
        exit()

    try:
        with open(plan_of_action_file, 'r', encoding='utf-8') as file:
            plan_of_action_content = file.read()
    except FileNotFoundError:
        print(f"Plan of action file '{plan_of_action_file}' not found.")
        exit()

    # Combine the summary and plan of action into the email body
    body = f"Summary:\n\n{summary_content}\n\nPlan of Action:\n\n{plan_of_action_content}"

    # Send the email
    send_email(sender_email, sender_password, recipient_email, subject, body, [summary_file, plan_of_action_file])
