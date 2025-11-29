# 🧠 AI Task Manager Agent

An intelligent task management system powered by Google's Gemini AI. Simply describe your tasks in natural language, and the AI automatically extracts task details, due dates, and times!

## ✨ Features

- 🤖 **AI-Powered Extraction** - Natural language task input
- 📅 **Smart Date Detection** - Understands "tomorrow at 3pm", "in 5 minutes", etc.
- 📊 **Dashboard** - Visual statistics and overview
- ✅ **Task Management** - Complete, delete, and filter tasks
- 📧 **Email Reminders** - Automatic reminders for due tasks
- 🎨 **Beautiful UI** - Modern design with animations 
- 💾 **Persistent Storage** - SQLite database


## 📦 Installation

1. Clone the repository
```bash
git clone [your-repo-url]
cd task-manager-agent
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

4. Run the app
```bash
streamlit run app.py
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash
- **Database**: SQLite
- **Email**: SMTP (Gmail)
- **Language**: Python 3.8+

## 📸 Screenshots

<img width="1255" height="596" alt="Screenshot 2025-11-29 163250" src="https://github.com/user-attachments/assets/8241ef9b-e6cc-4e53-bf89-6f0d03d8a665" />
<img width="1240" height="581" alt="image" src="https://github.com/user-attachments/assets/7809cef0-2ca7-44c8-91db-8ddb4be6c322" />



## 🎯 Usage Examples

- "Submit report by December 5th at 2pm"
- "Call mom tomorrow at 9am"
- "Buy groceries in 30 minutes"
- "Meeting next Monday at 10am"

## 👨‍💻 Author

Amrutha Gy

## 📄 License

MIT License
