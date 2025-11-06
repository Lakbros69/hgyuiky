# 🔐 Create Admin User - Quick Guide

## 🚀 Method 1: Using the Quick Script (EASIEST)

### Step 1: Run the Script
```bash
python create_admin.py
```

### Step 2: Follow the Prompts
```
Enter admin username (default: admin): [Press Enter or type username]
Enter admin email (default: admin@gamefi.com): [Press Enter or type email]
Enter admin password: [Type strong password]
Confirm password: [Type same password]
```

### Step 3: Success! 
You'll see:
```
✅ SUCCESS! Admin user created
```

---

## 🛠️ Method 2: Django Command

### Step 1: Run Django Command
```bash
python manage.py createsuperuser
```

### Step 2: Enter Details
```
Username: admin
Email: admin@gamefi.com
Password: ********
Password (again): ********
```

---

## 🎮 Access Admin Panel

### After Creating Admin:

1. **Start Server** (if not running):
   ```bash
   python manage.py runserver
   ```

2. **Open Admin Panel**:
   - URL: http://localhost:8000/admin/
   - Or: http://127.0.0.1:8000/admin/

3. **Login**:
   - Username: `admin` (or what you chose)
   - Password: [your password]

---

## 📝 What You Can Do in Admin Panel

✅ **Store Management**
- Add/Edit products (Free Fire Diamonds, PUBG UC)
- Set prices and quantities
- Upload product images
- Mark items as featured

✅ **Payment Verification**
- View payment requests
- See payment screenshots
- Approve/Reject payments
- Add coins to user wallets

✅ **Order Processing**
- View pending orders
- See in-game IDs for delivery
- Mark orders as processing/completed
- Cancel and refund orders

✅ **Tournament Management**
- Create tournaments
- Set entry fees and prizes
- Manage participants
- Award prizes

✅ **User Management**
- View all users
- Add/Deduct coins
- View transaction history
- Manage referrals

---

## ⚠️ Common Issues

### "User already exists"
**Solution:**
```bash
# Change password for existing admin
python manage.py changepassword admin
```

### "No module named 'django'"
**Solution:**
```bash
# Install Django
pip install -r requirements.txt
```

### "Can't find create_admin.py"
**Solution:**
```bash
# Make sure you're in the project directory
cd d:\trouna
python create_admin.py
```

### Admin panel not loading
**Solution:**
```bash
# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🔒 Security Tips

1. **Use Strong Password**:
   - At least 8 characters
   - Mix of letters, numbers, symbols
   - Don't use "admin123" or "password"

2. **Change Default Username**:
   - Don't use "admin" in production
   - Use something unique

3. **Keep Credentials Safe**:
   - Don't share admin access
   - Log out when done
   - Use secure connection (HTTPS in production)

---

## 📊 Admin Features Overview

### Dashboard Shows:
- Recent user registrations
- Pending payments
- Pending orders
- Recent transactions
- Tournament status

### Quick Actions:
- Bulk approve payments
- Bulk process orders
- Award prizes to multiple winners
- Add coins to users
- Create tournaments

### Search & Filter:
- Find users by username/email
- Filter orders by status
- Search payments by transaction ID
- View orders by date

---

## 🎯 Quick Commands Reference

```bash
# Create admin
python create_admin.py

# OR using Django
python manage.py createsuperuser

# Change admin password
python manage.py changepassword admin

# Start server
python manage.py runserver

# Access admin
http://localhost:8000/admin/

# View main site
http://localhost:8000/
```

---

## 💡 Testing Admin Panel

1. **Create Test Payment Request** (as regular user):
   - Login as user
   - Go to wallet
   - Buy coins
   - Upload fake screenshot

2. **Approve in Admin**:
   - Login to admin
   - Go to Payment Requests
   - Select request
   - Click Approve
   - Coins added automatically!

3. **Process Test Order**:
   - User buys item from store
   - Admin sees order
   - Mark as processing
   - Mark as completed
   - User gets notification!

---

## 🆘 Need Help?

### Check:
1. Server is running (`python manage.py runserver`)
2. No errors in terminal
3. Database migrations are done (`python manage.py migrate`)
4. Static files collected (`python manage.py collectstatic`)

### Logs Location:
- Terminal output shows errors
- Admin actions are logged
- Transaction history in database

---

**Created:** November 2025
**For:** Gaming Platform Admin Setup
