# Drip.com

## Overview

**Drip** is a modern social media platform built exclusively for **fashion lovers, creators, and trend followers**. Inspired by the intuitive interfaces of Instagram and Pinterest, this app blends **user-driven fashion sharing** with **cutting-edge AI** to revolutionize how we engage with style online.

Whether you’re planning your party look, checking out campus trends, or building an influencer following — Fashion App helps you **post, vote, recommend, and analyze outfits** in an intelligent, social-first environment.

---

## **🚀 Features at a Glance**

### **👤 User Profiles & Social Features**

- Create detailed profiles: Name, Age, Gender, Location, Fashion Preferences, Color Choices, and more.
- Follow and be followed by other users.
- Send **direct messages** to connect and collaborate.
- Get real-time **likes, comments, and saves** on your posts.
- Explore a “For You” feed based on people you follow.

---

### **📸 Post Types**

### **1. Classic Posts**

- Upload one or more images in a post.
- View zoomable photos with proper formatting.
- Likes, comments, and saves available per post.

### **2. Voting Posts**

- Upload multiple outfit choices for a single event.
- Followers **vote** for the best outfit — no likes, only votes.
- Helps users decide what to wear based on real-time feedback.

---

## **🤖 AI-Powered Features**

Drip is not just about social sharing. It uses AI to **analyze fashion** and enhance recommendations.

### **🧠 Apparel Detection (YOLOv8 + Post-processing)**

- Every uploaded image is run through an **object detection model** (YOLOv8) fine-tuned on fashion datasets like DeepFashion/OpenImages.
- Automatically detects and classifies items like tshirt, shirt, jeans, dress, etc.
- Uses this information to:
    - Categorize posts.
    - Suggest better content if no apparel is detected.
    - Store structured data in the ApparelTag model.

> Example: {"tshirt": ["image1.png"], "jeans": ["image1.png"]}
> 

### **🔍 Smart Search & Recommendations**

- Search for **outfits and users** using tags (e.g., “skirt”, “blazer”, “oversized hoodie”).
- Powered by structured YOLO-labeled tags.
- Future upgrade path to **semantic search** using NLP (e.g., “Korean streetwear”, “pastel summer looks”).

### **🚫 Obscene Content Filter (Upcoming)**

- Uses pre-trained NSFW classifiers (Yahoo/OpenNSFW) to **block inappropriate content** before posting.

---

## **🧩 Tech Stack**

| **Layer** | **Technology** |
| --- | --- |
| **Backend** | Django Rest Framework (DRF), Python |
| **Frontend** | React.js (in progress) |
| **Database** | PostgreSQL / SQLite (dev) |
| **Media Storage** | File-based with Django MEDIA_ROOT |
| **AI** | YOLOv8 (Ultralytics), Torch, Custom Filtering |
| **Authentication** | DRF Token Authentication |
| **Hosting Plan** | To be deployed via Render, Railway, or Docker-based VPS |

---

## **📱 MVP Checklist**

### **✅ Core Social Features:**

- Like / Comment / Save posts
- Create multiple-image posts
- Direct Messaging between users
- Profile creation + edit
- Photo zoom, view, and formatting
- Follow/Unfollow mechanism
- For You feed (filtered by following)
- Voting-based outfit selection posts

### **⚙️ Advanced Settings (In Progress):**

- Visibility controls (private/public posts)
- Blocked users
- Tagged brands and product links
- Notification system
- Settings screen like Instagram

### **🤖 Machine Learning:**

- Apparel detection using YOLOv8
- Post classification: Fashion vs. Non-fashion
- Obscene content filtering (via NSFW detection)
- Recommendation engine (outfit matches, similar users)
- Visual + textual similarity-based search
- Cold-start personalization via profile data

---

## **🌐 Deployment Plan**

- Backend hosted with Gunicorn + Django
- React frontend hosted via Vite + Netlify or Vercel
- PostgreSQL for production
- Static/media file hosting via AWS S3 or Django-based CDN
- Model hosting: local server + GPU inference (or move to TorchServe)

---

## **💡 Vision Ahead**

Fashion App aims to become a **decentralized fashion intelligence platform**:

- A place where people **share** and **validate outfits**.
- A tool that **helps brands discover trends and influencers**.
- A community-driven **recommendation engine** for everyday wear.

With advanced AI, we aim to build features like:

- Auto-tagging brands via image detection.
- Recommending what to wear based on weather + calendar.
- Suggesting outfit combinations from your wardrobe history.

---

## 🛠️ Installation & Setup

### Prerequisites

Ensure you have the following installed:
	•	Python (≥3.8)
	•	Node.js & npm (for frontend development)
	•	Virtual Environment (venv or conda recommended)
	•	PostgreSQL/MySQL (for production setup)

### Steps

1️⃣ Clone the repository

```shell
git clone https://github.com/pundarikaksha7/fashion-app.git
```

```shell
cd fashion-app
```

2️⃣ Create and activate a virtual environment

```shell 
python3 -m venv venv
```

```shell
source venv/bin/activate
```  

On Windows: 
```shell 
venv\Scripts\activate
```

3️⃣ Install dependencies

```shell
pip install -r requirements.txt
```

4️⃣ Apply database migrations

```shell
python3 manage.py migrate
```

5️⃣ Run the development server

```shell
python3 manage.py runserver
```

The app will be available at http://127.0.0.1:8000/

## 📜 Contribution Guidelines

We welcome contributions! Please follow these steps:

1️⃣ Fork the repository
2️⃣ Create a feature branch:

```shell
git checkout -b feature-name
```

3️⃣ Commit and push changes:

```shell
git commit -m "Added new feature"
```

```shell
git push origin feature-name
```

4️⃣ Create a pull request 🚀


## 📬 Contact & Support

For discussions, issues, or collaboration opportunities, reach out via:

📩 Email: pundarikakshamohanty@gmail.com

📢 Linkedin: linkedin.com/in/pundarikaksha7

🌐 Website: [Coming Soon]

