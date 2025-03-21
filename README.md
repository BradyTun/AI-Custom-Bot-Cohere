
# **AI Chatbot Platform**

AIONAT is a **Flask-based AI chatbot platform** that allows users to create, edit, and interact with their AI-powered chatbots. The project integrates **Cohere AI** for generating bot responses and supports **profile picture uploads** with cropping functionality.

---

## **🚀 Features**

✅ **Create & Edit Bots** – Set a name, personality, and profile picture.

✅ **Chat in Real-Time** – Messages update dynamically without page refresh.

✅ **Delete Bots** – Type `"Delete <bot_name>"` in the chat to remove a bot.

✅ **Public & Private Bots** – Choose whether to share your bot.

✅ **Flask SQLAlchemy Database** – Uses SQLite for development & PostgreSQL for production.

---

## **📦 Installation & Setup**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/aionat-chatbot.git
cd aionat-chatbot
```

### **2️⃣ Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**

Create a **`.env`** file in the root directory and add:

```
COHERE_KEY=your_cohere_api_key
DATABASE_URL=sqlite:///database.db  # Using SQLite for development
SECRET_KEY=your_secret_key
```

---

## **🛠 Database Migration**

Before running the app, initialize and upgrade the database:

```bash
flask db upgrade
```

This applies any pending database migrations.

---

## **🚀 Running the App**

To start the Flask application, run:

```bash
python app.py
```

The server will be available at  **`http://127.0.0.1:5000/`** .

---

## **🔧 Deployment**

For production, the app uses  **Gunicorn** . If deploying (e.g., on Heroku), use:

```bash
web: flask db upgrade; gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
```

---

## **🛠 Tech Stack**

* **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
* **Database:** SQLite (Dev), PostgreSQL (Prod)
* **AI Model:** Cohere AI (for chatbot responses)
* **Frontend:** Tailwind CSS, JavaScript (Dynamic chat updates)
* **Image Processing:** Cropper.js for profile picture cropping

---

## **🤝 Contributing**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added feature X"`).
4. Push the branch (`git push origin feature-branch`).
5. Open a  **Pull Request** .
