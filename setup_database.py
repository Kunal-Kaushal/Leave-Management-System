import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# --- DATABASE CONNECTION SETUP ---
# The proxy is running on localhost:5432, so we connect there.
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_USER = "postgres" # Default user for Cloud SQL PostgreSQL
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "leave_management"

# A basic check to ensure the password was loaded
if not DB_PASSWORD:
    raise ValueError("❌ DB_PASSWORD environment variable not found. Please set it in your .env file.")

# Create the connection string for PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a database engine
engine = create_engine(DATABASE_URL)



def get_leave_balance(employee_email:str)->float | None:
    """
    Retrieves the current leave balance for a given employee from the database.
    
    Args:
        employee_email: The email of the employee to look up.
        
    Returns:
        The leave balance as a float, or None if the employee is not found.
    """
    with engine.connect() as connection:
        query = text("SELECT leave_balance FROM employees WHERE email = :email")
        result = connection.execute(query, {"email": employee_email}).scalar_one_or_none()
        
        if result is not None:
            print(f"✅ Found leave balance for {employee_email}: {result}")
            return float(result)
        else:
            print(f"⚠️ No employee found with email: {employee_email}")
            return None



# --- CREATE TABLES AND INSERT DATA ---
try:
    with engine.connect() as connection:
        print("🚀 Successfully connected to Cloud SQL!")

        # Create employees table using PostgreSQL syntax
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                leave_balance FLOAT NOT NULL
            )
        """))
        print("✅ 'employees' table is ready.")

        # Create leave_requests table using PostgreSQL syntax
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER NOT NULL REFERENCES employees(id),
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                reason TEXT,
                status VARCHAR(50) NOT NULL
            )
        """))
        print("✅ 'leave_requests' table is ready.")

        # Insert sample data (handle potential duplicates with ON CONFLICT)
        connection.execute(text("""
            INSERT INTO employees (id, name, email, leave_balance)
            VALUES (1, 'John Doe', 'john.doe@example.com', 15.5)
            ON CONFLICT (email) DO NOTHING;
        """))
        print("✅ Sample employee 'John Doe' is available.")

        # Commit the transaction to save the changes
        connection.commit()
        
except Exception as e:
    print(f"❌ An error occurred: {e}")

print("\nDatabase setup is complete! ✨")