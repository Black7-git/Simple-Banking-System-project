#!/usr/bin/env python
"""
PetRescue Setup Script
This script helps set up the PetRescue application quickly
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Main setup function"""
    print_header("PetRescue Setup Script")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install dependencies
    print_header("Installing Dependencies")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("Failed to install dependencies. Please install manually.")
        sys.exit(1)
    
    # Create directories
    print_header("Creating Directories")
    os.makedirs("media/pet_photos", exist_ok=True)
    os.makedirs("staticfiles", exist_ok=True)
    print("✓ Directories created")
    
    # Run migrations
    print_header("Setting Up Database")
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("Migration creation failed")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        print("Migration failed")
        sys.exit(1)
    
    # Collect static files
    print_header("Collecting Static Files")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Create superuser prompt
    print_header("Create Superuser Account")
    print("You need to create an admin account to access the admin panel.")
    create_admin = input("Create superuser now? (y/n): ").lower()
    
    if create_admin == 'y':
        print("\nPlease follow the prompts to create your admin account:")
        os.system("python manage.py createsuperuser")
        
        print("\nIMPORTANT: After creating the superuser, you need to set admin privileges.")
        print("You can do this by:")
        print("1. Starting the server with: python manage.py runserver")
        print("2. Logging in at http://127.0.0.1:8000/admin/")
        print("3. Going to User profiles and checking 'Is admin' for your user")
    
    # Final instructions
    print_header("Setup Complete!")
    print("To start the development server, run:")
    print("    python manage.py runserver")
    print("\nThen access the application at:")
    print("    Main Site: http://127.0.0.1:8000/")
    print("    Django Admin: http://127.0.0.1:8000/admin/")
    print("    User Admin Panel: http://127.0.0.1:8000/admin-panel/")
    print("\nFor more information, see README.md and INSTALLATION.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
