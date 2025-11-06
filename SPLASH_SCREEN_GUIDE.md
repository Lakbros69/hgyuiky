# 🎨 Splash Screen Guide

## Overview

The splash screen provides a professional, mobile-app-like loading experience for your Gaming Platform. It appears when users first load the website on mobile/tablet devices.

## Features

✅ **Beautiful Animations**
- Logo bounce-in effect
- Fade-in text animations
- Dual rotating spinners
- Animated loading dots
- Floating particle background

✅ **Responsive Design**
- Optimized for mobile (≤768px)
- Scaled for tablets (769px-1024px)  
- Works on desktop (optional)

✅ **Performance**
- Shows only once per session
- Auto-hides after 2.5 seconds
- Tap anywhere to skip
- Prevents body scroll while active

✅ **Customizable**
- Easy color changes
- Adjustable duration
- Mobile-only or all devices
- Custom branding

## Files Created

### 1. CSS File
**Location:** `static/css/splash.css`
- All splash screen styles
- Animations and keyframes
- Responsive breakpoints
- Particle effects

### 2. JavaScript File
**Location:** `static/js/splash.js`
- Splash screen logic
- Session management
- Auto-hide functionality
- Manual controls

### 3. HTML Template
**Location:** `templates/base.html` (updated)
- Splash screen markup
- Linked CSS and JS files

## Customization

### Change Duration

Edit `static/js/splash.js`:
```javascript
const SPLASH_DURATION = 2500; // Change to desired milliseconds
```

**Examples:**
- `1500` = 1.5 seconds
- `2500` = 2.5 seconds (default)
- `3000` = 3 seconds

### Show on All Devices

Edit `static/js/splash.js`:
```javascript
const SHOW_ON_MOBILE_ONLY = false; // Show on desktop too
```

### Change Colors

Edit `static/css/splash.css`:

**Background Gradient:**
```css
background: linear-gradient(180deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 50%, #YOUR_COLOR_1 100%);
```

**Logo Background:**
```css
.splash-logo {
    background: white; /* Change logo box color */
}
```

**Logo Icon Gradient:**
```css
.splash-logo i {
    background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
}
```

**Text Colors:**
```css
.splash-title {
    color: #FFF8F8; /* Title color */
}

.splash-subtitle {
    color: #E9DFC3; /* Subtitle color */
}
```

### Change Logo Icon

Edit `templates/base.html`:
```html
<div class="splash-logo">
    <i class="fas fa-YOUR-ICON"></i> <!-- Change icon class -->
</div>
```

**Popular Gaming Icons:**
- `fa-gamepad` (current)
- `fa-trophy`
- `fa-crown`
- `fa-bolt`
- `fa-star`
- `fa-fire`

### Change Text

Edit `templates/base.html`:
```html
<h1 class="splash-title">YOUR TITLE</h1>
<p class="splash-subtitle">Your Tagline Here</p>
```

### Adjust Animation Speed

Edit `static/css/splash.css`:

**Logo Animation:**
```css
animation: bounceIn 1s ease-out; /* Change 1s to desired duration */
```

**Spinner Speed:**
```css
animation: spin 1s linear infinite; /* Faster: 0.5s, Slower: 2s */
```

**Loading Dots:**
```css
animation: dotPulse 1.4s infinite; /* Change timing */
```

## Advanced Customization

### Add Company Logo Image

Replace icon with image in `templates/base.html`:
```html
<div class="splash-logo">
    <img src="{% static 'images/logo.png' %}" alt="Logo" style="width: 70%; height: 70%; object-fit: contain;">
</div>
```

### Disable Particle Effect

Remove particles from `templates/base.html`:
```html
<!-- Remove or comment out this section -->
<div class="splash-particles">
    <div class="particle"></div>
    ...
</div>
```

### Add Progress Bar

Add to `templates/base.html` in `.splash-content`:
```html
<div style="width: 200px; height: 4px; background: rgba(255,255,255,0.2); border-radius: 2px; margin: 2rem auto;">
    <div style="width: 0%; height: 100%; background: white; border-radius: 2px; animation: progressBar 2.5s ease-out forwards;"></div>
</div>
```

Add to `static/css/splash.css`:
```css
@keyframes progressBar {
    from { width: 0%; }
    to { width: 100%; }
}
```

## Testing

### Test Splash Screen

Open browser console and run:
```javascript
showSplash();
```
This will clear the session flag and reload the page with splash.

### Force Show on Desktop

Temporarily set in `static/js/splash.js`:
```javascript
const SHOW_ON_MOBILE_ONLY = false;
```
Then clear cache and reload.

### Skip Session Check

Comment out in `static/js/splash.js`:
```javascript
// if (splashShown) {
//     return false;
// }
```

## Troubleshooting

### Splash Not Showing

**Check:**
1. Are you on mobile/tablet? (or SHOW_ON_MOBILE_ONLY = false)
2. Clear browser cache
3. Check browser console for errors
4. Verify static files are loaded
5. Run: `python manage.py collectstatic`

### Splash Shows Every Time

**Solution:**
- Check if sessionStorage is working
- Try private/incognito mode
- Clear browser data

### Animation Glitches

**Solution:**
- Reduce particle count (remove some particles)
- Increase SPLASH_DURATION
- Simplify animations in CSS

### Logo Not Centered

**Solution:**
```css
.splash-logo {
    margin: 0 auto 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

## Performance Tips

1. **Keep it Short:** 2-3 seconds is optimal
2. **Minimize Particles:** 3-5 particles max
3. **Optimize Images:** Use compressed logos
4. **Cache Assets:** Ensure static files are cached
5. **Skip on Fast Connections:** Consider checking load time

## Browser Support

✅ **Fully Supported:**
- Chrome (Mobile & Desktop)
- Safari (iOS & macOS)
- Firefox (Mobile & Desktop)
- Edge
- Samsung Internet

✅ **Features:**
- CSS Animations
- CSS Gradients
- SessionStorage
- CSS Transforms
- Backdrop Filter

## Best Practices

1. **Keep Duration Under 3 Seconds**
   - Users expect fast loading
   - Skip option available

2. **Match Brand Colors**
   - Use your brand palette
   - Consistent with main site

3. **Optimize for Mobile**
   - Test on real devices
   - Check various screen sizes

4. **Provide Skip Option**
   - Already implemented (tap anywhere)
   - Don't force users to wait

5. **One Time Per Session**
   - Already implemented
   - Don't annoy users

## Example Configurations

### Minimal Splash (Fast)
```javascript
// splash.js
const SPLASH_DURATION = 1500;
```
```html
<!-- base.html - Remove particles -->
```

### Full Experience (Impressive)
```javascript
// splash.js
const SPLASH_DURATION = 3000;
```
```css
/* splash.css - Keep all animations */
```

### Desktop + Mobile
```javascript
// splash.js
const SHOW_ON_MOBILE_ONLY = false;
```

## Credits

Built with:
- Pure CSS3 animations
- Vanilla JavaScript
- Font Awesome icons
- Modern responsive design

---

**Last Updated:** November 2025
**Version:** 1.0
