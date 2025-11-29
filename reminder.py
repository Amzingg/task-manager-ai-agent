# reminder.py
import sqlite3
from datetime import datetime
from email_service import send_email
from db import mark_task_done

DB_PATH = "tasks.db"

def get_due_tasks():
    """
    Returns list of (id, task, duedate) for tasks that are pending and whose duedate <= now.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, duedate FROM tasks WHERE status='pending' AND duedate IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    due = []
    now = datetime.now()
    for tid, task, dd in rows:
        try:
            duedate = datetime.strptime(dd, "%Y-%m-%d %H:%M")
            if duedate <= now:
                due.append((tid, task, dd))
        except Exception:
            # skip parse errors
            continue
    return due

def send_due_reminders(user_email):
    """
    Sends email reminders for all due tasks to user_email.
    Marks tasks as done after sending successfully.
    Returns number of reminders attempted (success or not).
    """
    due = get_due_tasks()
    count = 0
    for tid, task, dd in due:
        subject = f"Task Reminder: {task}"
        message = f"Your task is due now or overdue.\n\nTask: {task}\nDue: {dd}\n\n-- Task Manager AI Agent"
        ok = send_email(user_email, subject, message)
        # Mark as done only if email send succeeded
        if ok:
            mark_task_done(tid)
        count += 1
    return count
