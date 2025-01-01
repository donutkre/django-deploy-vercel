import os
import subprocess
from django.contrib.auth.models import User

def install_dependencies():
    """Install required dependencies from requirements.txt."""
    print("Installing dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

def apply_migrations():
    """Apply Django migrations."""
    print("Applying migrations...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)

def load_initial_data():
    """Load initial data from CSV or fixtures."""
    print("Loading initial data...")
    subprocess.run(["python", "manage.py", "load_data"], check=True)

def create_superuser():
    """Create a Django superuser."""
    print("Creating superuser...")
    try:
        User.objects.create_superuser("admin", "admin@example.com", "admin123!!!")
        print("Superuser created successfully.")
    except Exception as e:
        print(f"Superuser creation failed: {e}")

def run_server():
    """Run the Django development server."""
    print("Starting the development server...")
    subprocess.run(["python", "manage.py", "runserver"], check=True)

if __name__ == "__main__":
    install_dependencies()
    apply_migrations()
    load_initial_data()
    create_superuser()
    run_server()
