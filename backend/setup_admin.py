"""
Setup script to create the initial admin user.
Run this once after setting up the database.

Usage: python setup_admin.py
"""
import sys
from getpass import getpass
from core.database import SessionLocal, init_db
from core.models import User


def setup_admin(reset_password=False):
    init_db()
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin and reset_password:
            print(f"\n=== Reset password for: {existing_admin.username} ===\n")
            password = getpass("Enter new password: ")
            if len(password) < 8:
                print("Error: Password must be at least 8 characters.")
                sys.exit(1)
            
            confirm_password = getpass("Confirm password: ")
            if password != confirm_password:
                print("Error: Passwords do not match.")
                sys.exit(1)
            
            existing_admin.set_password(password)
            db.commit()
            print(f"\nPassword reset successfully for '{existing_admin.username}'!")
            return
        
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
        if db.query(User).filter(User.username == username).first():
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
        
        db.add(admin)
        db.commit()
        
        print(f"\nAdmin user '{username}' created successfully!")
        print("\nYou can now log in to the dashboard.")
    finally:
        db.close()


if __name__ == '__main__':
    reset = '--reset' in sys.argv or '-r' in sys.argv
    setup_admin(reset_password=reset)
