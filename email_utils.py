import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
def draft_leave_email(employee_email: str, start_date:str, end_date:str, reason:str)->str:
    """
    Drafts a professional leave request email based on provided details.

    Args:
        employee_email: The email of the employee requesting leave.
        start_date: The start date of the leave in YYYY-MM-DD format.
        end_date: The end date of the leave in YYYY-MM-DD format.
        reason: The reason for the leave.

    Returns:
        A formatted string containing the subject and body of the email.
    """

    subject=f"Leave Request from {employee_email}"
    body = f"""
    Dear Manager,

    I am writing to formally request a leave of absence from {start_date} to {end_date}.

    The reason for my leave is: {reason}.

    I will ensure all my pending tasks are completed before my departure. Please let me know if you require any further information.

    Thank you for your consideration.

    Best regards,
    {employee_email}
    """
    
    email_draft = f"Subject: {subject}\n\n{body}"
    
    print("✅ Email drafted successfully.")
    return email_draft






def send_email(recipient_email: str, subject: str, body: str) -> None:
    """
    Sends an email using SendGrid.

    Args:
        recipient_email: The email address of the recipient.
        subject: The subject of the email.
        body: The body content of the email.

    Returns:
        A string indicating the status of the email sending operation.
    """
    sendgrid_api_key= os.getenv("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        return "Error: SendGrid API key is not configured."
    
    
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=body
    )
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        if response.status_code == 202: # 222 is the status code for "accepted"
            print(f"✅ Email sent successfully to {recipient_email}")
            return f"Successfully sent the email to {recipient_email}."
        else:
            return f"Error: Failed to send email. Status code: {response.status_code}"
    except Exception as e:
        print(f"❌ An error occurred while sending email: {e}")
        return "An unexpected error occurred while trying to send the email."
