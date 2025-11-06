# 🎮 Custom Admin Panel Guide

## 🎯 What Is This?

This is a **separate custom admin panel** (NOT the Django admin) where you can:
- ✅ Customize your website (colors, branding, content)
- ✅ Manage payments and orders
- ✅ View statistics and analytics
- ✅ Control store items
- ✅ Manage users

## 🚀 Access Your Custom Admin Panel

### URL:
```
http://localhost:8000/dashboard/
```

### Who Can Access:
- **Staff members only** (superusers and staff)
- Regular users cannot access this panel

---

## 📊 Features Overview

### 1. **Dashboard** 📈
**URL:** `/dashboard/`

**Features:**
- Quick statistics (users, payments, orders, tournaments)
- Recent activity feed
- Revenue overview
- Quick action buttons

**What You See:**
- 4 stat cards with key metrics
- Recent users, payments, and orders
- Total revenue this week
- Quick links to common tasks

### 2. **Payment Management** 💰
**URL:** `/dashboard/payments/`

**Features:**
- View all payment requests
- Filter by status (Pending/Approved/Rejected)
- See payment screenshots
- One-click approve/reject

**How To Use:**
1. Click "Payments" in sidebar
2. View pending requests
3. Click screenshot to view full size
4. Click ✓ (approve) or ✗ (reject)
5. User gets coins automatically!

### 3. **Order Processing** 📦
**URL:** `/dashboard/orders/`

**Features:**
- View all orders with product images
- Filter by status
- See in-game IDs for delivery
- Update order status
- Add admin notes

**How To Use:**
1. Click "Orders" in sidebar
2. View pending orders
3. Note the **In-Game ID**
4. Deliver item in-game
5. Click edit button
6. Select "Completed"
7. Save - user gets notified!

### 4. **Store Management** 🏪
**URL:** `/dashboard/store/`

**Features:**
- View all store items with images
- Toggle active/inactive status
- See which items are featured
- Quick product management

**How To Use:**
- View all products
- Toggle items on/off
- (To add/edit products, use Django admin for now)

### 5. **User Management** 👥
**URL:** `/dashboard/users/`

**Features:**
- View all registered users
- Search by username/email
- Add coins to users
- View user stats

**How To Use:**
1. Search for user
2. Click "Add Coins" button
3. Enter amount and reason
4. User receives coins + notification!

### 6. **Website Customization** 🎨
**URL:** `/dashboard/settings/`

**THE MAIN FEATURE YOU WANTED!**

**Features:**
- **Change Colors**: Primary & secondary colors
- **Update Branding**: Site name, logo
- **Edit Homepage**: Hero title, description
- **Social Media**: Facebook, Instagram, Discord links
- **Payment Config**: Coin packages and pricing
- **Maintenance Mode**: Enable/disable site

**How To Customize:**

#### Change Website Colors:
1. Go to Settings
2. Find "Color Scheme" card
3. Click color picker
4. Choose your color
5. Click "Save Colors"
6. Done! Website updates instantly

#### Update Site Logo:
1. Go to Settings
2. Find "Logo & Branding" card
3. Upload new logo image
4. Click "Update Branding"

#### Change Homepage Text:
1. Go to Settings
2. Find "Homepage Content" card
3. Edit hero title and description
4. Click "Update Homepage"

#### Add Social Media Links:
1. Go to Settings
2. Find "Social Media Links" card
3. Enter your URLs
4. Click "Save Links"

#### Configure Coin Packages:
1. Go to Settings
2. Find "Payment Configuration" card
3. Edit JSON (coins: price)
4. Click "Update Packages"

---

## 🎨 User Interface

### Sidebar Navigation:
- **Dashboard**: Main overview
- **Payments**: Manage payment requests (with badge count)
- **Orders**: Process orders (with badge count)
- **Store Items**: Manage products
- **Users**: User management
- **Settings**: Website customization ⭐
- **View Website**: Go to main site
- **Logout**: Sign out

### Design Features:
- ✅ Modern gradient backgrounds
- ✅ Card-based layouts
- ✅ Smooth animations
- ✅ Mobile responsive
- ✅ Color-coded status badges
- ✅ Image previews
- ✅ Quick action buttons

---

## 📱 Mobile Responsive

Works perfectly on:
- 💻 Desktop
- 📱 Mobile phones
- 📲 Tablets

On mobile:
- Hamburger menu for sidebar
- Touch-friendly buttons
- Optimized layouts

---

## 🔐 Security

- ✅ **Staff-only access**: Only superusers and staff can access
- ✅ **Login required**: Redirects to login if not authenticated
- ✅ **CSRF protection**: All forms are protected
- ✅ **Separate from Django admin**: Different URL path

---

## ⚡ Quick Workflows

### Approve a Payment:
```
1. Dashboard → Payments
2. Filter: Pending
3. View screenshot
4. Click ✓ Approve
5. Done! User gets coins
```

### Complete an Order:
```
1. Dashboard → Orders
2. Filter: Pending
3. Note In-Game ID
4. Deliver item in-game
5. Click Edit button
6. Select "Completed"
7. Save
```

### Change Website Colors:
```
1. Dashboard → Settings
2. Color Scheme card
3. Pick colors
4. Save
5. View website to see changes!
```

### Add Coins to User:
```
1. Dashboard → Users
2. Search user
3. Click "Add Coins"
4. Enter amount
5. Save
```

---

## 🎯 Key Differences from Django Admin

| Feature | Django Admin | Custom Admin Panel |
|---------|--------------|-------------------|
| URL | `/admin/` | `/dashboard/` |
| Purpose | Database management | Website customization |
| Design | Standard Django UI | Modern, branded UI |
| Features | CRUD operations | Business workflows |
| Customization | Limited | Full control |
| User-friendly | Technical | Non-technical friendly |

---

## 🔧 Technical Details

### Files Created:

1. **Views**: `core/custom_admin_views.py`
   - Dashboard, payments, orders, settings logic

2. **URLs**: `core/custom_admin_urls.py`
   - All dashboard routes

3. **Templates**: `templates/custom_admin/`
   - base.html (sidebar, header)
   - dashboard.html (stats, activity)
   - payments.html (payment management)
   - orders.html (order processing)
   - settings.html (website customization)

4. **CSS**: `static/css/custom_admin.css`
   - Modern styling for admin panel

### URL Structure:
```
/dashboard/                  → Dashboard
/dashboard/payments/         → Payments list
/dashboard/payments/ID/approve/ → Approve payment
/dashboard/payments/ID/reject/  → Reject payment
/dashboard/orders/           → Orders list
/dashboard/orders/ID/update/ → Update order
/dashboard/store/            → Store items
/dashboard/users/            → Users list
/dashboard/users/ID/add-coins/ → Add coins
/dashboard/settings/         → Website settings
```

---

## 🎨 Customization Options

### Change Admin Panel Colors:
Edit `static/css/custom_admin.css` (lines 1-20):
```css
:root {
    --primary-color: #0118D8;     /* Your color */
    --secondary-color: #1B56FD;   /* Your color */
}
```

### Add More Settings:
Edit `templates/custom_admin/settings.html`:
- Add new form sections
- Add more customization options

### Extend Functionality:
Edit `core/custom_admin_views.py`:
- Add new views
- Add new features

---

## 💡 Pro Tips

1. **Use Settings Page**: This is where you customize your website!
2. **Quick Actions**: Use dashboard quick action buttons for fast access
3. **Filter Tables**: Use status filters to find what you need
4. **View Screenshots**: Click payment screenshots to verify
5. **Admin Notes**: Add notes when processing orders
6. **Mobile Friendly**: Access from your phone anytime

---

## 🆘 Troubleshooting

### Can't Access Dashboard?
**Solution:**
- Make sure you're logged in as staff/superuser
- URL is `/dashboard/` not `/admin/`
- Check: `http://localhost:8000/dashboard/`

### Settings Not Saving?
**Solution:**
- Check browser console for errors
- Ensure forms have CSRF token
- Verify you have staff permissions

### Images Not Loading?
**Solution:**
```bash
python manage.py collectstatic
```

### Changes Not Reflecting?
**Solution:**
- Hard refresh: Ctrl + F5
- Clear browser cache
- Check if changes saved successfully

---

## 🚀 What's Next?

### Immediate Use:
1. **Login**: http://localhost:8000/dashboard/
2. **Explore**: Check out all sections
3. **Customize**: Go to Settings page
4. **Manage**: Process payments and orders

### Future Enhancements:
- Analytics graphs
- Email templates customization
- Tournament creation interface
- Bulk operations
- Export data
- Advanced reporting

---

## 📞 Key Points

✅ **Two Separate Admin Panels:**
- Django Admin (`/admin/`) - For database management
- Custom Panel (`/dashboard/`) - For website customization

✅ **Main Purpose:**
- Customize website appearance
- Manage business operations
- User-friendly interface

✅ **Settings Page:**
- This is where you customize the website!
- Colors, branding, content, etc.

---

## 🎉 You're Ready!

Access your custom admin panel:
```
http://localhost:8000/dashboard/
```

Login with your admin credentials and start customizing!

---

**Created:** November 3, 2025
**Version:** 1.0
**Purpose:** Custom website management panel
