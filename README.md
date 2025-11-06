# Gaming Tournament Platform

A complete Django-based gaming tournament platform for **Free Fire** and **PUBG Mobile** with modern dark neon theme UI, wallet system, in-game item store, and admin panel.

## 🎮 Features

### For Players
- **Tournament System**: Join Free Fire and PUBG tournaments with entry fees and prize pools
- **Wallet System**: Add coins via QR payment (eSewa, Khalti, Bank transfer) with manual admin verification
- **Item Store**: Purchase Free Fire Diamonds, PUBG UC, and other in-game items
- **Leaderboard**: Track top players and tournament winners
- **Profile Management**: View stats, tournament history, and transaction records
- **Referral System**: Earn 10 coins for each successful referral
- **Notifications**: Real-time updates for tournaments, payments, and orders

### For Admins
- **Tournament Management**: Create, edit, cancel tournaments, and set winners
- **Payment Verification**: Approve/reject coin purchase requests with screenshots
- **Order Management**: Process and deliver in-game items to players
- **User Management**: View and manage user accounts, adjust coin balances
- **Comprehensive Dashboard**: Monitor all platform activities

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd d:/trouna
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The platform will be available at: **http://127.0.0.1:8000/**

## 📱 Accessing the Platform

### User Interface
- **Home**: http://127.0.0.1:8000/
- **Tournaments**: http://127.0.0.1:8000/tournaments/
- **Store**: http://127.0.0.1:8000/store/
- **Wallet**: http://127.0.0.1:8000/wallet/
- **Leaderboard**: http://127.0.0.1:8000/leaderboard/
- **Register**: http://127.0.0.1:8000/register/
- **Login**: http://127.0.0.1:8000/login/

### Admin Panel
- **URL**: http://127.0.0.1:8000/admin/
- Login with the superuser credentials you created

## 🎨 Design & UI

- **Theme**: Dark neon gaming aesthetic (black + purple + blue gradients)
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Animations**: Smooth transitions and hover effects
- **Icons**: Font Awesome 6 icons throughout

## ⚙️ Admin Panel Features

### 1. Tournament Management
- Create tournaments with title, game type, entry fee, prize pool, date/time
- Set room ID and password for participants
- Start, complete, or cancel tournaments
- Set participant positions and award prizes automatically

### 2. Payment Verification
- View all payment requests with screenshots
- Approve payments to add coins to user wallets
- Reject invalid payment requests
- Automatic transaction logging

### 3. Order Management
- View all store orders
- Mark orders as processing or completed
- Cancel orders and refund coins
- Add admin notes for delivery status

### 4. User Management
- View all registered users
- Add or deduct coins from user accounts
- View user statistics and tournament history
- Manage referral bonuses

### 5. Payment QR Management
- Upload QR codes for eSewa, Khalti, and Bank transfers
- Set account details and payment instructions
- Enable/disable payment methods

### 6. Store Item Management
- Add new in-game items (Free Fire Diamonds, PUBG UC, etc.)
- Set prices in coins
- Mark items as featured
- Enable/disable items

## 💡 How It Works

### For Users:
1. **Register**: Create an account and get a unique user ID
2. **Add Coins**: Select a coin package, make payment via QR, upload screenshot
3. **Wait for Approval**: Admin verifies payment and adds coins to wallet
4. **Join Tournaments**: Browse tournaments and join using coins
5. **Buy Items**: Purchase in-game items from the store
6. **Win Prizes**: Compete in tournaments and earn coins

### For Admins:
1. Login to admin panel
2. Create tournaments and set details
3. Upload payment QR codes
4. Verify payment requests and approve/reject
5. Process store orders and deliver items
6. Award tournament prizes to winners

## 📊 Database Models

- **User**: Extended auth user with coins, referral code, tournament stats
- **Tournament**: Tournament details, participants, prizes
- **TournamentParticipant**: Junction table for tournament enrollments
- **Transaction**: All wallet transactions (deposits, wins, purchases)
- **PaymentRequest**: Coin purchase requests with screenshots
- **PaymentQR**: Admin's payment QR codes and details
- **StoreItem**: In-game items for sale
- **Order**: Store purchase orders
- **Notification**: User notifications

## 🔐 Security Notes

1. **Change SECRET_KEY**: In `gaming_platform/settings.py`, change the SECRET_KEY before deployment
2. **DEBUG Mode**: Set `DEBUG = False` in production
3. **ALLOWED_HOSTS**: Update ALLOWED_HOSTS with your domain
4. **Media Files**: Ensure proper permissions for media file uploads
5. **HTTPS**: Use HTTPS in production for secure payments

## 📝 Additional Setup (Optional)

### Static Files for Production
```bash
python manage.py collectstatic
```

### Create Sample Data
After running the server, login to admin and:
1. Create Payment QR codes (eSewa, Khalti, Bank)
2. Add some store items (Free Fire Diamonds, PUBG UC)
3. Create sample tournaments
4. Test the complete user flow

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3 (Dark Neon Theme), JavaScript
- **Icons**: Font Awesome 6.4.0
- **Image Processing**: Pillow 10.1.0

## 📧 Support

For any issues or questions, please create an admin account and manage the platform through the admin panel at `/admin/`.

## 🎯 Quick Start Checklist

- [ ] Install Python and pip
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Run migrations
- [ ] Create superuser
- [ ] Start development server
- [ ] Login to admin panel
- [ ] Upload payment QR codes
- [ ] Create store items
- [ ] Create sample tournaments
- [ ] Test user registration and login
- [ ] Test complete purchase flow

## 🎮 Enjoy Your Gaming Platform!

Your platform is now ready to host exciting Free Fire and PUBG tournaments!
