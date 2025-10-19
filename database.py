# In database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import date

# Load environment variables from .env file
load_dotenv()

# --- DATABASE CONNECTION SETUP ---
DB_HOST = "127.0.0.1" # Connecting via Cloud SQL Proxy
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "leave_app_db" # Ensure this matches the DB name in Cloud SQL

if not DB_PASSWORD:
    raise ValueError("❌ DB_PASSWORD environment variable not found.")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def get_leave_balance(employee_email: str) -> float | None:
    """
    Retrieves the current leave balance for a given employee from Cloud SQL.
    """
    with engine.connect() as connection:
        query = text("SELECT leave_balance FROM employees WHERE email = :email")
        result = connection.execute(query, {"email": employee_email}).scalar_one_or_none()

        if result is not None:
            print(f"✅ DB: Found leave balance for {employee_email}: {result}")
            return float(result)
        else:
            print(f"⚠️ DB: No employee found with email: {employee_email}")
            return None

def create_pending_leave_request(employee_email: str, start_date: str, end_date: str, reason: str) -> int | None:
    """
    Logs a new, pending leave request in Cloud SQL (PostgreSQL).
    Returns the unique ID (int) of the new leave request, or None if failed.
    """
    print(f"✅ DB: Creating pending leave request for {employee_email} from {start_date} to {end_date}...")
    with engine.connect() as connection:
        try:
            find_id_query = text("SELECT id FROM employees WHERE email = :email")
            employee_id = connection.execute(find_id_query, {"email": employee_email}).scalar_one_or_none()

            if not employee_id:
                print(f"⚠️ DB: Cannot create request. No employee found: {employee_email}")
                return None

            insert_query = text(
                """
                INSERT INTO leave_requests (employee_id, start_date, end_date, reason, status)
                VALUES (:emp_id, :start_date, :end_date, :reason, 'pending')
                RETURNING id
                """
            )
            result = connection.execute(
                insert_query,
                {"emp_id": employee_id, "start_date": date.fromisoformat(start_date), "end_date": date.fromisoformat(end_date), "reason": reason}
            )
            new_request_id = result.scalar_one()
            connection.commit()

            print(f"✅ DB: Successfully created pending request with ID: {new_request_id}")
            return new_request_id
        except Exception as e:
            print(f"❌ DB: Error creating leave request: {e}")
            connection.rollback()
            return None

def update_leave_status(request_id: int, new_status: str) -> dict | None:
    """
    Updates a leave request to 'approved' or 'rejected' in Cloud SQL.
    If approved, it deducts the leave from the employee's balance.
    Returns a dict with employee_email and status, or None if failed.
    """
    print(f"✅ DB: Processing request ID {request_id} with status '{new_status}'...")
    with engine.connect() as connection:
        with connection.begin(): # Start transaction
            try:
                request_query = text("SELECT employee_id, start_date, end_date, status FROM leave_requests WHERE id = :req_id FOR UPDATE")
                request_data = connection.execute(request_query, {"req_id": request_id}).first()

                if not request_data:
                    print(f"⚠️ DB: No request found with ID: {request_id}")
                    return None

                if request_data.status != 'pending':
                    print(f"⚠️ DB: Request {request_id} already processed. Status: {request_data.status}")
                    email_query = text("SELECT email FROM employees WHERE id = :emp_id")
                    employee_email = connection.execute(email_query, {"emp_id": request_data.employee_id}).scalar()
                    return {"employee_email": employee_email, "status": request_data.status}

                update_query = text("UPDATE leave_requests SET status = :status WHERE id = :req_id")
                connection.execute(update_query, {"status": new_status, "req_id": request_id})
                employee_id = request_data.employee_id

                if new_status == 'approved':
                    duration_query = text("SELECT (:end_date::date - :start_date::date) + 1 AS duration")
                    duration = connection.execute(duration_query, {"start_date": request_data.start_date, "end_date": request_data.end_date}).scalar()
                    deduct_query = text("UPDATE employees SET leave_balance = leave_balance - :duration WHERE id = :emp_id")
                    connection.execute(deduct_query, {"duration": duration, "emp_id": employee_id})
                    print(f"✅ DB: Deducted {duration} days from employee {employee_id}")

                email_query = text("SELECT email FROM employees WHERE id = :emp_id")
                employee_email = connection.execute(email_query, {"emp_id": employee_id}).scalar()

                print(f"✅ DB: Successfully processed request {request_id}.")
                return {"employee_email": employee_email, "status": new_status}

            except Exception as e:
                print(f"❌ DB: Error updating leave status: {e}")
                return None