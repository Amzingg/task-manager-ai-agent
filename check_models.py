import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_task(text):
    prompt = f"""
    You are a task extraction assistant. Extract the task and due date from the user's input.
    
    User input: "{text}"
    
    Return a JSON object with exactly this format:
    {{
        "task": "the task description",
        "duedate": "YYYY-MM-DD HH:MM or null if no date mentioned"
    }}
    
    Rules:
    - If no date is mentioned, set duedate to null (not None, not "None")
    - Return ONLY the JSON object, no other text
    - Do not wrap in markdown code blocks
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Debug: Print what we received
        print(f"Raw response: {response_text}")
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Debug: Print cleaned response
        print(f"Cleaned response: {response_text}")
        
        # Parse JSON
        data = json.loads(response_text)
        
        # Validate the response has required fields
        if "task" not in data:
            print("Error: 'task' field missing from response")
            return {"task": None, "duedate": None}
        
        # Convert null to None for consistency
        if data.get("duedate") == "null" or data.get("duedate") == "":
            data["duedate"] = None
            
        print(f"Extracted data: {data}")
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Failed to parse: {response_text}")
        return {"task": None, "duedate": None}
    except Exception as e:
        print(f"Error: {e}")
        return {"task": None, "duedate": None}