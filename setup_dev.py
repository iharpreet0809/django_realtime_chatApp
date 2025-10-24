#!/usr/bin/env python
"""
Development setup script for Django Chat Application
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Django Chat Application for Development")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected. Consider activating your venv.")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return
    
    # Test database connection
    if not run_command("python manage.py test_db", "Testing database connection"):
        print("⚠️  Database connection failed. Make sure MySQL is running and credentials are correct.")
    
    # Make migrations
    run_command("python manage.py makemigrations", "Creating migrations")
    
    # Apply migrations
    run_command("python manage.py migrate", "Applying migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Create superuser prompt
    print("\n📝 You may want to create a superuser account:")
    print("   python manage.py createsuperuser")
    
    print("\n🎉 Setup complete! You can now run:")
    print("   python manage.py runserver")
    print("\n📚 Available URLs:")
    print("   - Main app: http://localhost:8000/")
    print("   - Admin: http://localhost:8000/admin/")
    print("   - API docs: http://localhost:8000/swagger/")

if __name__ == "__main__":
    main()