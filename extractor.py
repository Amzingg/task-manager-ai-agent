import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_task(text):
    # Get current date and time for context
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    
    prompt = f"""
You are a task extraction assistant. 

Current date: {today}
Current time: {current_time} (24-hour format)

Extract the task and due date from this input: "{text}"

Return ONLY a JSON object with this exact format:
{{
    "task": "the task description",
    "duedate": "YYYY-MM-DD HH:MM"
}}

IMPORTANT RULES:
- Use 24-hour format (00:00 to 23:59)
- Convert relative times correctly:
  * "in 5 minutes" = current time + 5 minutes
  * "tomorrow at 9am" = tomorrow's date + 09:00
  * "at 3pm" = today's date + 15:00
  * "next Monday" = calculate next Monday's date
- If time is mentioned, use it exactly
- If only date mentioned, use "09:00" as default time
- If NO date/time mentioned at all, use null for duedate
- Return ONLY the JSON, no markdown, no explanation

Examples:
Current time is 15:30
Input: "Call mom in 5 minutes"
Output: {{"task": "Call mom", "duedate": "2025-11-29 15:35"}}

Input: "Submit report tomorrow at 3pm"
Output: {{"task": "Submit report", "duedate": "2025-11-30 15:00"}}

Input: "Buy groceries"
Output: {{"task": "Buy groceries", "duedate": null}}
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        # Validate structure
        if "task" not in data:
            return {"task": None, "duedate": None}
        
        # Ensure task is not empty
        if not data["task"] or data["task"].strip() == "":
            return {"task": None, "duedate": None}
        
        # Handle null duedate
        if data.get("duedate") in [None, "null", "", "None"]:
            data["duedate"] = None
        
        # Validate and fix the datetime format if needed
        if data["duedate"]:
            try:
                # Try to parse the datetime to ensure it's valid
                parsed_dt = datetime.strptime(data["duedate"], "%Y-%m-%d %H:%M")
                # Re-format to ensure consistency
                data["duedate"] = parsed_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                # If parsing fails, set to None
                print(f"Invalid datetime format: {data['duedate']}")
                data["duedate"] = None
            
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response: {response_text}")
        return {"task": None, "duedate": None}
    except Exception as e:
        print(f"Error in extract_task: {e}")
        return {"task": None, "duedate": None}