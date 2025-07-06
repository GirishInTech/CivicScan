# 🧹 CivicScan

**CivicScan** is a Django-based full-stack web application designed to empower citizens of Bengaluru to report and track public cleanliness issues. This platform is part of a broader ambition to create a cleaner, more aware India by leveraging technology for civic participation.

---

## 🌍 Project Vision

> "Cleanliness is not just about sanitation; it's a mindset."

CivicScan aims to encourage community participation in keeping public spaces clean. The app provides a simple, accessible way for people to:

- Report cleanliness issues (with photos & location)
- View others' reports on an interactive map
- Help authorities prioritize problem areas

---

## 🚀 Live Demo

🌐 Hosted on Render: [https://civicscan.onrender.com](https://civicscan.onrender.com)

---

## 🔧 Tech Stack

- **Backend**: Django 5.1, Python 3.12  
- **Frontend**: HTML5, CSS3, JavaScript, Leaflet.js  
- **Database**: PostgreSQL (Render)  
- **Media Storage**: Cloudinary  
- **Deployment**: Render (Free Plan)  
- **Version Control**: Git & GitHub  

---

## 🛠 Features Implemented

### ✅ 1. User Management

- Signup/Login with validation
- User profiles
- Session-based authentication

### ✅ 2. Clean Report Submission

- Submit photos, cleanliness status, and review
- Auto-location detection with reverse geocoding
- Conditional UI for anonymous vs. logged-in users
- User feedback after submission

### ✅ 3. Admin Dashboard (Map View)

- Interactive Leaflet.js map
- Color-coded markers: Red = Dirty, Blue = Clean
- Marker popups show status, location, photo preview
- Lightbox for full image view
- JSON API for map data

### ✅ 4. Clean & Responsive Design

- Centralized `base.html` with `{% block content %}`
- Navbar with dynamic menu based on auth status
- Mobile-first layout with media queries

### ✅ 5. Backend Optimization

- Machine Learning: scikit-learn (DBSCAN clustering)
- Media storage via Cloudinary
- Static files handled with WhiteNoise
- Render environment variables for security
- Logs & debugging with logging module

### ✅ 6. AI-Powered Hotspot Detection

- Clusters multiple "dirty" reports using DBSCAN (scikit-learn)
- Automatically detects high-density complaint areas
- Saves hotspot data with location and report count
- Visualizes hotspots as red circles on the map (Leaflet.js)
- Helps authorities focus on most affected areas

---

## 🧠 Future Enhancements

| Feature               | Description                             |
|-----------------------|-----------------------------------------|
| Edit/Delete Reports   | Allow users to manage submissions       |
| Search by Area        | Address-based filtering for admin map   |
| Filter by Status      | View only "dirty" or "clean" areas      |
| Live Map Updates      | Polling or refresh option for new data  |
| AI Hotspot Detection  | Predict areas needing urgent action     |
| Heatmap Layer         | Use heatmaps to show issue density      |
| Dynamic Hotspot Radius| Adjust circle size by report count      |
| Hotspot Time Filter   | Show hotspots only from past 7 days     |

---

## 🖼️ Hotspot Visualization Example

> CivicScan uses AI (DBSCAN clustering) to find high-frequency cleanliness issues and shows them as red heat zones on the map:

![Hotspot Detection in Action](static/images/hotspot_demo.gif)

---

## 📂 Project Structure (Simplified)

BrillianBengaluru/
├── homepage/ Static content & landing
├── users/ Auth & profile
├── reports/ Report submission & map
├── templates/ Jinja templates
├── static/ Custom CSS, JS, icons
├── media/ (Optional) local fallback
├── manage.py
├── requirements.txt
├── render.yaml Render deployment config
├── .env (not committed)


---

## ⚠️ Security & Environment

- All secrets (DB, Cloudinary, SECRET_KEY) loaded via environment variables
- `.env` file is ignored via `.gitignore`
- Render handles env securely through Dashboard

---

## 💡 Motivation

This project reflects a deep personal goal: to contribute meaningfully to India's cleanliness movement. Bengaluru is only the beginning. CivicScan aspires to evolve with AI, community feedback, and city-level expansion.

> "Don’t wait for change. Report it. Inspire it."

---

## 👨‍💻 Author

**Girish Yandigeri**  
MCA Student @ RVCE  
- [GitHub](https://github.com/gallant-giri)  
- [LinkedIn](https://www.linkedin.com/in/girish-yandigeri-136517200/)

---

## 🙌 Acknowledgements

- Django & Python community  
- Leaflet.js & OpenStreetMap  
- Cloudinary for free media storage  
- Render.com for free hosting  
- Friends and mentors who encouraged this dream 💙  

---

## 📜 License

This project is for educational and demonstration purposes.  
**MIT License coming soon.**

---

Want to contribute ideas, suggest features, or collaborate?  
**Reach out! Let’s build something good together for our cities. 🧼**
