# app.py - Fixed Layout
import streamlit as st
from extractor import extract_task
from db import init_db, add_task, get_tasks, update_task_status, delete_task, get_task_stats
from reminder import get_due_tasks, send_due_reminders
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Task Manager AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Animations
st.markdown("""
<style>
    /* Animated gradient background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 1rem;
    }
    
    /* Floating animation for header */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .main-header {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        text-align: center;
        animation: float 3s ease-in-out infinite;
    }
    
    /* Gradient text animation */
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 5s ease infinite;
        margin-bottom: 0.5rem;
    }
    
    /* Slide in animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .section-box {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .section-box:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transform: translateY(-3px);
    }
    
    /* Pulse animation for section titles */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #e9ecef;
        animation: pulse 3s ease-in-out infinite;
    }
    
    /* Bounce animation for stats */
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        animation: bounce 0.5s ease;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Slide from left animation */
    @keyframes slideFromLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .task-item {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        animation: slideFromLeft 0.4s ease-out;
        transition: all 0.3s ease;
    }
    
    .task-item:hover {
        background: #e9ecef;
        border-left-width: 8px;
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .task-completed {
        background: #d4edda;
        border-left-color: #28a745;
        opacity: 0.8;
    }
    
    /* Shake animation for overdue alerts */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes alertPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }
    
    .due-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-weight: 600;
        animation: alertPulse 2s ease-in-out infinite, shake 0.5s ease-in-out;
    }
    
    /* Button animations */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button:active {
        transform: translateY(0px) scale(0.98);
    }
    
    /* Input animations */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    .stTextInput input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Checkbox animation */
    .stCheckbox {
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        transform: scale(1.2);
    }
    
    /* Sparkle effect */
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-color: #667eea !important;
        border-top-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

init_db()

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">✨ AI Task Manager</div>
    <p style="color: #6c757d; font-size: 1.1rem;">Intelligent task management powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Email Configuration Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📧 Email Configuration</div>', unsafe_allow_html=True)
    user_email = st.text_input("Enter your email for reminders", placeholder="your.email@gmail.com", key="email_input")
    st.markdown('</div>', unsafe_allow_html=True)

# Create New Task Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Create New Task</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("Describe your task", placeholder="e.g., Submit report by December 5th at 2pm", label_visibility="collapsed", key="task_input")
    with col2:
        add_button = st.button("✨ Add Task", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if add_button:
    if not user_input.strip():
        st.error("⚠️ Please enter a task description")
    else:
        with st.spinner("🤖 AI is processing your task..."):
            result = extract_task(user_input)
            if result.get("task"):
                add_task(result["task"], result.get("duedate"))
                st.success(f"✅ Task created: **{result['task']}**")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Couldn't understand the task. Please try again.")

# Dashboard Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    stats = get_task_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📋 TOTAL TASKS</div>
            <div class="stat-number">{stats['total']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-label">⏳ PENDING</div>
            <div class="stat-number">{stats['pending']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-label">✅ COMPLETED</div>
            <div class="stat-number">{stats['completed']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Your Tasks Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Your Tasks</div>', unsafe_allow_html=True)
    
    # Filter buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        filter_all = st.button("📋 All", use_container_width=True, key="filter_all")
    with col2:
        filter_pending = st.button("⏳ Pending", use_container_width=True, key="filter_pending")
    with col3:
        filter_completed = st.button("✅ Completed", use_container_width=True, key="filter_completed")
    
    # Determine filter
    if 'current_filter' not in st.session_state:
        st.session_state.current_filter = "all"
    
    if filter_all:
        st.session_state.current_filter = "all"
    elif filter_pending:
        st.session_state.current_filter = "pending"
    elif filter_completed:
        st.session_state.current_filter = "completed"
    
    tasks = get_tasks(st.session_state.current_filter)
    
    if not tasks:
        st.info(f"🎯 No {st.session_state.current_filter} tasks found.")
    else:
        for tid, task, dd, status in tasks:
            is_completed = status == "completed"
            
            # Parse due date
            if dd:
                try:
                    due_dt = datetime.strptime(dd, "%Y-%m-%d %H:%M")
                    due_date_str = due_dt.strftime("%b %d, %Y at %I:%M %p")
                except:
                    due_date_str = dd
            else:
                due_date_str = "No deadline"
            
            # Task card
            col1, col2, col3 = st.columns([0.5, 5, 0.8])
            
            with col1:
                checkbox = st.checkbox("Done", value=is_completed, key=f"check_{tid}", label_visibility="collapsed")
                if checkbox != is_completed:
                    update_task_status(tid, "completed" if checkbox else "pending")
                    st.rerun()
            
            with col2:
                if is_completed:
                    st.markdown(f"""
                    <div class="task-item task-completed">
                        <div style="text-decoration: line-through; color: #6c757d;">
                            <strong>{task}</strong><br>
                            <small>📅 {due_date_str}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="task-item">
                        <strong style="color: #212529;">{task}</strong><br>
                        <small style="color: #6c757d;">📅 {due_date_str}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️", key=f"del_{tid}", use_container_width=True):
                    delete_task(tid)
                    st.success("Deleted!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Due Tasks Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚠️ Due Tasks</div>', unsafe_allow_html=True)
    due = get_due_tasks()
    
    if due:
        st.warning(f"⚠️ You have {len(due)} overdue task(s)!")
        for tid, task, dd in due:
            try:
                due_dt = datetime.strptime(dd, "%Y-%m-%d %H:%M")
                dd_display = due_dt.strftime("%b %d, %Y at %I:%M %p")
            except:
                dd_display = dd
            
            st.markdown(f"""
            <div class="due-alert">
                🚨 <strong>OVERDUE:</strong> {task} — Due: {dd_display}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✨ All caught up! No overdue tasks.")
    st.markdown('</div>', unsafe_allow_html=True)

# Send Reminders Section
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📬 Send Email Reminders</div>', unsafe_allow_html=True)
    
    if st.button("📧 Send Reminders Now", use_container_width=True, key="send_reminders"):
        if not user_email:
            st.error("⚠️ Please enter your email address first")
        else:
            with st.spinner("📤 Sending reminders..."):
                count = send_due_reminders(user_email)
                if count > 0:
                    st.success(f"✅ Successfully sent {count} reminder(s)!")
                    st.rerun()
                else:
                    st.info("📭 No due tasks to remind about")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="section-box" style="text-align: center; margin-top: 2rem;">
    <p style="color: #6c757d; margin: 0;">Made with ❤️ using Streamlit & Gemini AI</p>
</div>
""", unsafe_allow_html=True)