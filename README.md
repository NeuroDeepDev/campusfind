<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ██████╗ █████╗ ███╗   ███╗██████╗ ██╗   ██╗███████╗               ║
║   ██╔════╝██╔══██╗████╗ ████║██╔══██╗██║   ██║██╔════╝               ║
║   ██║     ███████║██╔████╔██║██████╔╝██║   ██║███████╗               ║
║   ██║     ██╔══██║██║╚██╔╝██║██╔═══╝ ██║   ██║╚════██║               ║
║   ╚██████╗██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝███████║               ║
║    ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝               ║
║                                                                       ║
║              ███████╗██╗███╗   ██╗██████╗                            ║
║              ██╔════╝██║████╗  ██║██╔══██╗                           ║
║              █████╗  ██║██╔██╗ ██║██║  ██║                           ║
║              ██╔══╝  ██║██║╚██╗██║██║  ██║                           ║
║              ██║     ██║██║ ╚████║██████╔╝                           ║
║              ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### 🎓 **CAMPUS LOST & FOUND MANAGEMENT SYSTEM**

```
┌─────────────────────────────────────────────────────────┐
│  Recover Lost Items • Connect Community • Fast & Simple │
└─────────────────────────────────────────────────────────┘
```

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## 🚀 **SYSTEM CAPABILITIES**

```
┌──────────────────────────────────────────────────────────────┐
│                    CORE FUNCTIONALITIES                      │
└──────────────────────────────────────────────────────────────┘
```

### 📊 **Item Management**
```
├─ Lost Item Reporting
│  ├─ Submit lost item details with description
│  ├─ Add location, date, and time information
│  ├─ Category classification system
│  └─ Photo/image upload support
│
├─ Found Item Registration
│  ├─ Register found items with details
│  ├─ Geolocation tracking
│  ├─ Timestamp recording
│  └─ Item condition documentation
│
└─ Item Status Tracking
   ├─ Active/Inactive status management
   ├─ Claimed/Unclaimed filtering
   ├─ Historical record keeping
   └─ Automatic status updates
```



### 📝 **Claim Processing**
```
├─ Claim Submission
│  ├─ Item claim request system
│  ├─ Proof of ownership verification
│  ├─ Contact information exchange
│  └─ Claim status tracking
│
├─ Claim Management
│  ├─ Review pending claims
│  ├─ Approve/reject functionality
│  ├─ Notification system
│  └─ Claim history logging
│
└─ Recovery Workflow
   ├─ Found-to-claimed pipeline
   ├─ Handoff coordination
   └─ Completion confirmation
```


## ⚙️ **TECHNICAL ARCHITECTURE**

```
┌──────────────────────────────────────────────────────────────┐
│                     TECH STACK                               │
└──────────────────────────────────────────────────────────────┘
```

### 🔧 **Backend Framework**
```python
Framework    : Django 5.x
Language     : Python 3.x
Database     : SQLite3
ORM          : Django ORM
Template     : Django Templates
```

### 🎨 **Frontend Stack**
```javascript
HTML5        : Semantic markup
CSS3         : Modern styling + animations
JavaScript   : Vanilla JS (ES6+)
Fonts        : Google Fonts (Poppins, Rajdhani, Orbitron)
Icons        : Unicode emoji icons
```

### 📦 **Core Dependencies**
```
Django       : Web framework
Pillow       : Image processing
SQLite3      : Database engine
```

---

## 🛠️ **INSTALLATION & SETUP**

```
┌──────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT PROTOCOL                         │
└──────────────────────────────────────────────────────────────┘
```

### **Step 1: Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### **Step 2: Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt
```

### **Step 3: Database Initialization**
```bash
# Run migrations
python manage.py migrate

# Load initial data (fixtures)
python manage.py loaddata core/fixtures/initial_data.json
```

### **Step 4: Launch Server**
```bash
# Start development server
python manage.py runserver
```

### **Step 5: Access Application**
```
🌐 Open browser and navigate to:
   http://127.0.0.1:8000/
```

---

## 📁 **PROJECT STRUCTURE**

```
CampusFind/
│
├─ core/                    # Main application
│  ├─ models.py            # Database models
│  ├─ views.py             # View controllers
│  ├─ urls.py              # URL routing
│  ├─ api_urls.py          # API endpoints
│  ├─ forms.py             # Form definitions
│  ├─ templates/           # HTML templates
│  └─ fixtures/            # Initial data
│
├─ static/                 # Static assets
│  ├─ style.css           # Global styles
│  └─ script.js           # Client-side logic
│
├─ media/                  # User uploads
│
├─ campusfind/            # Project settings
│  ├─ settings.py         # Configuration
│  ├─ urls.py             # Root URL config
│  └─ wsgi.py             # WSGI config
│
├─ db.sqlite3             # Database file
├─ manage.py              # Django CLI
└─ requirements.txt       # Dependencies
```
---

## 📄 **LICENSE**

```
This project is open-source and available for educational purposes.
```

---

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             Built with ❤️ for Campus Communities             ║
║                                                              ║
║              Recover • Connect • Simplify                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**CampusFind** - *Making Lost Items Found Again*

</div>
