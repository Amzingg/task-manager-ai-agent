# db.py
import sqlite3

DB_PATH = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            duedate TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

def add_task(task, duedate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks(task, duedate) VALUES (?, ?)", (task, duedate))
    conn.commit()
    conn.close()

def get_tasks(filter_status="all"):
    """Get tasks with optional filtering"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if filter_status == "all":
        cursor.execute("SELECT id, task, duedate, status FROM tasks ORDER BY id DESC")
    elif filter_status == "pending":
        cursor.execute("SELECT id, task, duedate, status FROM tasks WHERE status = 'pending' ORDER BY id DESC")
    elif filter_status == "completed":
        cursor.execute("SELECT id, task, duedate, status FROM tasks WHERE status = 'completed' ORDER BY id DESC")
    else:
        cursor.execute("SELECT id, task, duedate, status FROM tasks ORDER BY id DESC")
    
    data = cursor.fetchall()
    conn.close()
    return data

def mark_task_done(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    """Update task status (pending/completed)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_task_stats():
    """Get task statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
    pending = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    completed = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total': total,
        'pending': pending,
        'completed': completed
    }