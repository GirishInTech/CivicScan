# CivicScan - Complete Project Analysis

## TECH STACK
- Django 5.1 (Python 3.12)
- PostgreSQL (Supabase)
- Cloudinary (media storage)
- Leaflet.js (maps)
- scikit-learn (DBSCAN clustering)
- Geopy/Nominatim (geocoding)
- WhiteNoise (static files)
- PWA (Service Worker)

## PROJECT STRUCTURE
```
BrillianBengaluru/
├── homepage/          # Landing, offline pages
├── users/             # Auth, profiles, dashboard
├── reports/           # Reports, hotspots, map
└── BrillianBengaluru/ # Settings, root URLs
```

## DATA MODELS

### User + UserProfile
```python
User (Django built-in)
├── username, email, first_name, password
└── is_superuser, is_staff

UserProfile
├── user (OneToOne → User)
└── phone_number
```

### Report
```python
Report
├── user (FK → User, nullable)
├── photo (CloudinaryField)
├── status ('clean'/'dirty')
├── location ("lat,lng" string)
├── address (reverse geocoded)
├── review (TextField)
└── submitted_at
```

### Hotspot
```python
Hotspot
├── cluster_id (DBSCAN label)
├── latitude, longitude (centroid)
├── report_count
├── address
└── last_updated
```

## KEY ENDPOINTS
```
GET  /                          → Homepage
GET  /reports/submit/           → Report form
POST /reports/submit/           → Create report
GET  /reports/map/              → Interactive map
GET  /reports/data/             → JSON: all reports
GET  /reports/hotspots/data/    → JSON: all hotspots
GET  /users/signup/             → Signup form
GET  /users/dashboard/          → User's reports (auth)
GET  /accounts/login/           → Login
GET  /admin/                    → Django admin
```

## USER JOURNEYS

### Anonymous Report Submission
1. User visits /reports/submit/
2. Fills form (photo, status, location, review)
3. GPS captured via JavaScript
4. POST submits data
5. Backend:
   - Validates form
   - Extracts lat/lng
   - Calls Nominatim API for address (3 retries)
   - Uploads photo to Cloudinary
   - Saves Report (user=None)
6. Shows anon_success.html

### Authenticated Report
- Same flow but user=request.user
- Report appears in /users/dashboard/

### Map View
1. User visits /reports/map/
2. Leaflet.js loads
3. JavaScript fetches:
   - /reports/data/ (all reports)
   - /reports/hotspots/data/ (clusters)
4. Draws markers (red=dirty, blue=clean)
5. Draws hotspot circles (500m radius)
6. Popups show photo/details

### ML Hotspot Detection
```bash
python manage.py detect_hotspots
```
1. Queries dirty reports
2. Extracts lat/lng to DataFrame
3. Runs DBSCAN (eps=500m, min_samples=2, haversine)
4. Groups by cluster_id
5. Calculates mean coordinates
6. Deletes old hotspots
7. Creates new Hotspot objects

## IMPLEMENTED FEATURES
✅ Anonymous + authenticated reporting
✅ Photo upload (Cloudinary)
✅ GPS + reverse geocoding
✅ Interactive Leaflet map
✅ DBSCAN hotspot detection
✅ User dashboard (view own reports)
✅ PWA (offline support, service worker)
✅ Signup/login/logout

## MISSING FEATURES (FROM SYNOPSIS)
❌ Report verification workflow (pending/accepted/rejected)
❌ Authority dashboard (view ALL reports, not just admin's)
❌ Notifications (email/SMS on status change)
❌ Report editing/deletion
❌ Duplicate detection
❌ REST API (Django REST Framework)
❌ Predictive analytics
❌ Mobile app

## SECURITY ISSUES
🚨 SECRET_KEY hardcoded in .env (committed to Git!)
🚨 DEBUG=True always on
🚨 No rate limiting or CAPTCHA
🚨 No file upload validation
🚨 ALLOWED_HOSTS = ['*']
🚨 .env file in Git history (needs BFG/filter-branch)

## CODE QUALITY ISSUES
⚠️ Duplicate `location` field in Report model
⚠️ N+1 query in report_data_json
⚠️ No database indexes
⚠️ No caching
⚠️ Zero unit tests
⚠️ Hardcoded values (500m radius)
⚠️ Multiple `import os` in settings.py

## IMMEDIATE PRIORITY (YOUR REQUEST)
### Admin Report Verification System

**What's Needed:**
1. Add to Report model:
   - verified (Boolean, default False)
   - verification_status ('pending'/'accepted'/'rejected')
   - verified_by (FK to User)
   - verified_at (DateTime)

2. Create admin verification page:
   - URL: /admin/verify-reports/
   - List ALL reports (all users)
   - Filters: user, status, verification_status, date
   - Actions: Accept/Reject buttons

3. Update user dashboard:
   - Show verification badges
   - Pending (yellow), Accepted (green), Rejected (red)

**Files to Modify:**
- reports/models.py
- reports/views.py
- reports/urls.py
- reports/templates/reports/admin_verify.html (new)
- users/templates/users/dashboard.html

**Time:** 10-12 minutes

## DEPLOYMENT
- Platform: Render.com (free tier)
- Database: PostgreSQL (Supabase)
- Media: Cloudinary CDN
- Static: WhiteNoise
- WSGI: Gunicorn

## ENVIRONMENT VARIABLES (.env)
```
DATABASE_URL=postgresql://...
CLOUDINARY_URL=cloudinary://...
SECRET_KEY=django-insecure-...
PYTHON_VERSION=3.12.4
```
⚠️ All committed to GitHub - ROTATE IMMEDIATELY

## SCALABILITY BOTTLENECKS
1. No connection pooling
2. Nominatim rate limits (no caching)
3. Manual hotspot detection (no Celery)
4. Map loads all reports (no pagination)
5. No Redis caching

## SYNOPSIS ALIGNMENT
✅ PostgreSQL spatial data (partial)
✅ DBSCAN clustering
✅ Citizen uploads with photos
✅ Leaflet.js map
✅ Cloudinary optimization
❌ Django REST Framework (mentioned, not used)
❌ Authority workflow ⭐ PRIORITY
❌ Predictive analytics
❌ Mobile app (future)

## NEXT STEPS
1. Implement verification workflow (10 min)
2. Fix security issues (20 min)
3. Add rate limiting + CAPTCHA (15 min)
4. Write unit tests (1 hour)
5. Optimize database queries (30 min)
6. Add caching layer (30 min)
