import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ---------- CORE TOOL 1: Calculator ----------
def calculator(a: float, b: float, operation: str):
    """Perform basic arithmetic on two numbers.
    operation must be one of: add, subtract, multiply, divide.
    """
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                return "Error: cannot divide by zero"
            return a / b
        else:
            return f"Error: unknown operation '{operation}'"
    except Exception as e:
        return f"Calculator error: {e}"


# ---------- CORE TOOL 2: Weather Lookup ----------
def get_weather(latitude: float, longitude: float):
    """Get the current weather for a location.
    Provide the latitude and longitude of the requested city
    (e.g. Mumbai = 19.07, 72.87 | Ratnagiri = 16.99, 73.31).
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(data)  # raw JSON for debugging

        if "current_weather" not in data:
            return "Weather data unavailable for this location."

        return data["current_weather"]
    except requests.exceptions.RequestException as e:
        return f"Weather lookup failed: {e}"
    except Exception as e:
        return f"Unexpected error fetching weather: {e}"


# ---------- CORE TOOL 3: Word/Text Utility ----------
def text_utility(text: str, operation: str):
    """Perform simple text operations.
    operation must be one of: count (word count), reverse.
    """
    try:
        if not text:
            return "Error: no text provided"

        if operation == "count":
            return len(text.split())
        elif operation == "reverse":
            return text[::-1]
        else:
            return f"Error: unknown operation '{operation}'"
    except Exception as e:
        return f"Text utility error: {e}"


# ---------- EXTENSION TOOL: To-Do List Manager ----------
todo_list = []

def todo_manager(action: str, item: str = ""):
    """Manage a simple in-memory to-do list.
    action must be one of: add, list, complete.
    item is the task text, required for 'add' and 'complete'.
    """
    try:
        if action == "add":
            if not item:
                return "Error: no item provided to add"
            todo_list.append(item)
            return f"Added: {item}"
        elif action == "list":
            if not todo_list:
                return "Your to-do list is empty"
            return todo_list
        elif action == "complete":
            if item in todo_list:
                todo_list.remove(item)
                return f"Completed and removed: {item}"
            return f"'{item}' not found in the list"
        else:
            return f"Error: unknown action '{action}'"
    except Exception as e:
        return f"To-do manager error: {e}"


tools = [
    calculator,
    get_weather,
    text_utility,
    todo_manager,
]


def run_agent():
    print("AI Agent ready. Type 'quit' or 'exit' to stop.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input,
                config={"tools": tools},
            )
            print("Agent:", response.text)
        except Exception as e:
            print(f"Agent error: {e}")


if __name__ == "__main__":
    run_agent()