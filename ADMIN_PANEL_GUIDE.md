# 🎮 Gaming Platform Admin Panel Guide

## 📋 Overview

The Gaming Platform Admin Panel provides comprehensive tools for managing store products, verifying payments, processing orders, and overseeing the entire platform.

## 🔐 Accessing the Admin Panel

### URL
```
http://localhost:8000/admin/
or
http://your-domain.com/admin/
```

### Creating a Superuser
If you haven't created an admin account yet:
```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password

## 📦 Store Management

### Managing Store Items

**Location:** Admin Panel → Store Items

#### Features:
- ✅ **Add New Products:** Create Free Fire Diamonds, PUBG UC, or other items
- ✅ **Edit Products:** Update prices, quantities, descriptions, and images
- ✅ **Image Preview:** See product images directly in the list view
- ✅ **Toggle Status:** Mark items as active/inactive
- ✅ **Feature Items:** Highlight special products
- ✅ **Bulk Actions:** Update multiple items at once

#### Adding a New Product:
1. Click "ADD STORE ITEM"
2. Fill in details:
   - Name (e.g., "100 Free Fire Diamonds")
   - Item Type (Free Fire Diamonds / PUBG UC / Other)
   - Description
   - Quantity (e.g., 100)
   - Price (in coins)
   - Upload image
3. Check "Featured" to highlight on store page
4. Check "Active" to make it available for purchase
5. Click "SAVE"

#### Editing Products:
- Click on any item in the list
- Modify fields as needed
- View full image preview in edit view
- Save changes

#### Bulk Actions:
- Select multiple items using checkboxes
- Choose action from dropdown:
  - Mark as featured
  - Mark as active
  - Mark as inactive
- Click "GO"

## 💳 Payment Verification

### Managing Payment Requests

**Location:** Admin Panel → Payment Requests

#### Features:
- ✅ **View All Requests:** See pending, approved, and rejected payments
- ✅ **Screenshot Preview:** View payment proofs directly
- ✅ **Status Badges:** Color-coded status indicators
- ✅ **Quick Actions:** Approve or reject multiple requests
- ✅ **Filter Options:** By status, payment method, date

#### Verifying Payments:

##### Individual Verification:
1. Click on a payment request
2. **View Screenshot:** Click on the payment screenshot to see full size
3. **Verify Details:**
   - User information
   - Coins amount
   - Payment amount
   - Transaction ID
   - Payment method
4. **Add Admin Notes:** Optional notes for record-keeping
5. **Change Status:** Select "Approved" or "Rejected"
6. Click "SAVE"

##### Bulk Approval:
1. Select pending requests using checkboxes
2. Choose "Approve selected payment requests" from actions
3. Click "GO"
4. Coins will be automatically added to users' accounts
5. Users receive notifications

##### Bulk Rejection:
1. Select requests to reject
2. Choose "Reject selected payment requests"
3. Click "GO"
4. Users receive rejection notifications

#### What Happens When Approved:
- ✅ Coins added to user's wallet
- ✅ Transaction record created
- ✅ User receives notification
- ✅ Status changed to "Approved"
- ✅ Timestamp and processor recorded

## 📦 Order Management

### Processing Orders

**Location:** Admin Panel → Orders

#### Features:
- ✅ **Order Tracking:** View all orders with status
- ✅ **Item Preview:** See product images in list
- ✅ **Status Management:** Update order progress
- ✅ **Delivery Info:** Access in-game IDs
- ✅ **Admin Notes:** Add processing notes

#### Order Workflow:

##### 1. New Order (Pending):
- Customer places order
- Coins deducted from wallet
- Order appears as "PENDING"

##### 2. Processing Order:
1. Click on the order
2. Note the **In-Game ID** and **In-Game Name**
3. Add admin notes (optional)
4. Change status to "Processing"
5. Save
6. User receives "Order Processing" notification

##### 3. Completing Order:
After delivering items in-game:
1. Open the order
2. Add delivery confirmation in admin notes
3. Change status to "Completed"
4. Save
5. User receives "Order Completed" notification

##### Bulk Operations:
- **Mark as Processing:** Select orders → "Mark as processing"
- **Mark as Completed:** Select orders → "Mark as completed"
- **Cancel Orders:** Select orders → "Cancel and refund" (coins refunded)

#### Filtering Orders:
- By Status: Pending, Processing, Completed, Cancelled
- By Item Type: Free Fire, PUBG, Other
- By Date: Use date hierarchy
- Search: Order ID, username, in-game ID

## 🎮 Additional Management

### Tournament Management
- Create and edit tournaments
- Set room IDs and passwords
- Award prizes to winners
- Cancel with automatic refunds

### User Management
- View user profiles and stats
- Add/deduct coins manually
- View transaction history
- Manage referrals

### Transaction Tracking
- View all coin transactions
- Filter by type (deposits, purchases, prizes)
- Audit trail for all financial activities

### Notifications
- View sent notifications
- Track read/unread status
- Filter by type

## 🎨 Admin Panel Features

### Visual Enhancements:
- 🎨 **Color-Coded Status Badges:** Easy status identification
- 🖼️ **Image Previews:** Quick visual reference
- 💰 **Coin Icons:** Clear pricing display
- ⭐ **Featured Indicators:** Highlight special items
- ✅ **Status Icons:** Active/inactive indicators

### User-Friendly Interface:
- 📱 Responsive design
- 🔍 Advanced search and filtering
- 📊 Bulk actions for efficiency
- 🔔 Automatic notifications
- 📝 Detailed audit trails

## 🚀 Quick Actions

### Daily Tasks:
1. **Check Pending Payments** (Admin → Payment Requests → Status: Pending)
2. **Process Pending Orders** (Admin → Orders → Status: Pending)
3. **Update Store Items** (Admin → Store Items)

### Common Operations:

#### Approve Payment:
```
1. Payment Requests → Select pending
2. Action: "Approve selected payment requests"
3. GO
```

#### Complete Order:
```
1. Orders → Open order
2. Status: "Completed"
3. SAVE
```

#### Add New Product:
```
1. Store Items → ADD STORE ITEM
2. Fill details + upload image
3. Active ✓, Featured ✓
4. SAVE
```

## 📊 Dashboard Overview

When you log in, you'll see:
- Recent actions
- Quick links to all models
- Important statistics
- Pending items requiring attention

## ⚠️ Important Notes

### Security:
- ✅ Only share admin credentials with trusted staff
- ✅ Use strong passwords
- ✅ Log out when finished
- ✅ Review admin actions regularly

### Best Practices:
- ✅ Verify payment screenshots carefully
- ✅ Add admin notes for tracking
- ✅ Process orders promptly
- ✅ Keep store items updated
- ✅ Monitor user feedback

### Automatic Features:
- ✅ Coins added/refunded automatically
- ✅ Notifications sent to users
- ✅ Transaction records created
- ✅ Audit trails maintained

## 🆘 Troubleshooting

### Can't Access Admin?
- Verify you're a superuser: `python manage.py createsuperuser`
- Check URL: `/admin/`
- Clear browser cache

### Images Not Showing?
- Run: `python manage.py collectstatic`
- Check media files configuration
- Verify image upload permissions

### Payments Not Approving?
- Check user exists
- Verify payment request is "pending"
- Check for error messages
- Review transaction logs

## 📞 Support

For technical issues:
1. Check error logs
2. Verify database connection
3. Review admin action history
4. Contact technical support

---

**Last Updated:** November 2025
**Version:** 1.0
