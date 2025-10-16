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
