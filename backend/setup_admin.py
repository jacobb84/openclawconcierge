"""
Setup script to create the initial admin user.
Run this once after setting up the database.

Usage: python setup_admin.py
"""
import sys
from getpass import getpass
from app import create_app
from models import db, User


def setup_admin():
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            response = input("Do you want to create another admin? (y/n): ").strip().lower()
            if response != 'y':
                print("Setup cancelled.")
                return
        
        print("\n=== OpenClaw Concierge Admin Setup ===\n")
        
        # Get username
        username = input("Enter admin username: ").strip()
        if not username:
            print("Error: Username cannot be empty.")
            sys.exit(1)
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            print(f"Error: User '{username}' already exists.")
            sys.exit(1)
        
        # Get password
        password = getpass("Enter admin password: ")
        if len(password) < 8:
            print("Error: Password must be at least 8 characters.")
            sys.exit(1)
        
        confirm_password = getpass("Confirm password: ")
        if password != confirm_password:
            print("Error: Passwords do not match.")
            sys.exit(1)
        
        # Create admin user
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"\nAdmin user '{username}' created successfully!")
        print("\nYou can now log in to the dashboard.")


if __name__ == '__main__':
    setup_admin()
