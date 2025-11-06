#!/usr/bin/env python
"""
Quick script to create an admin user
Run: python create_admin.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    """Create admin user if it doesn't exist"""
    print("=" * 60)
    print("🎮 Gaming Platform - Create Admin User")
    print("=" * 60)
    print("\nPress Enter for default values in parentheses\n")
    
    # Username
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"\n❌ User '{username}' already exists!")
        print(f"💡 Try a different username or use: python manage.py changepassword {username}")
        return False
    
    # Email
    email = input("Enter admin email (default: admin@gamefi.com): ").strip() or "admin@gamefi.com"
    
    # Password
    print("\n🔐 Password Requirements:")
    print("   - At least 8 characters")
    print("   - Not too common")
    print()
    
    password = input("Enter admin password: ").strip()
    if not password:
        print("❌ Password cannot be empty!")
        return False
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        return False
    
    confirm_password = input("Confirm password: ").strip()
    if password != confirm_password:
        print("❌ Passwords don't match!")
        return False
    
    # Create admin
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Admin user created")
        print("=" * 60)
        print(f"\n👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"🔑 User ID: {user.user_id}")
        print(f"💰 Coins: {user.coins}")
        print(f"🎫 Referral Code: {user.referral_code}")
        
        print("\n" + "🎮 ACCESS ADMIN PANEL ".center(60, "="))
        print(f"\n   URL: http://localhost:8000/admin/")
        print(f"   OR:  http://127.0.0.1:8000/admin/")
        print(f"\n   Username: {username}")
        print(f"   Password: {'*' * len(password)}")
        
        print("\n" + "📝 WHAT YOU CAN DO ".center(60, "="))
        print("\n   ✓ Manage store products")
        print("   ✓ Verify payment requests")
        print("   ✓ Process orders")
        print("   ✓ Manage tournaments")
        print("   ✓ View all users and transactions")
        
        print("\n" + "🚀 NEXT STEPS ".center(60, "="))
        print("\n   1. Start server: python manage.py runserver")
        print("   2. Open: http://localhost:8000/admin/")
        print("   3. Login with credentials above")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    try:
        success = create_admin()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
