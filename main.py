import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import webbrowser
import openai
import os
import sys
import requests

# Set up your OpenAI API credentials
openai.api_key = "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"

messages = []

def custom_chat_gpt(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": chat_reply})
    return chat_reply

def generate_explanation(error_message):
    prompt = f"Error: {error_message}"
    explanation = custom_chat_gpt(prompt)
    return explanation

def execute_external_code():
    try:
        selected_file = file_dropdown.get()

        with open(selected_file, "r") as file:
            code = file.read()

        subprocess.run(["python", "-c", code], check=True)

    except Exception as e:
        print(f"Error: {e}")

# Analyze code using ChatGPT
def analyze_code():
    def background_task():
        selected_file = file_dropdown.get()

        with open(selected_file, "r") as file:
            code = file.read()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code analyzer."},
                {"role": "user", "content": code}
            ]
        )

        analysis_result = response.choices[0].message.content

        # Create a new tkinter window to display the analysis
        analysis_window = tk.Toplevel()
        analysis_window.title("Code Analysis")

        analysis_text = tk.Text(analysis_window, wrap=tk.WORD, height=20, width=60)
        analysis_text.pack(pady=10)
        analysis_text.insert(tk.END, analysis_result)

        # Re-enable the button after generating analysis
        analyze_button.config(state=tk.NORMAL)
        analyze_button.config(text="Analyze Code")

    # Disable the button and change its text to "Analyzing..."
    analyze_button.config(text="Analyzing...", state=tk.DISABLED)

    # Start the background task in a separate thread
    threading.Thread(target=background_task).start()

def install_package():
    package_name = package_entry.get()
    if package_name:
        # Disable the button and change its text to "Installing..."
        install_button.config(text="Installing...", state=tk.DISABLED)

        # Execute package installation
        install_thread = threading.Thread(target=install_package_thread, args=(package_name,))
        install_thread.start()

def install_package_thread(package_name):
    try:
        subprocess.run(["pip", "install", package_name], check=True)

        # Update the button text and enable the button after installation
        install_button.config(text="Install Package", state=tk.NORMAL)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        # Update the button text and enable the button if an error occurs during installation
        install_button.config(text="Install Package", state=tk.NORMAL)

def get_python_version():
    return f"Python {sys.version}"

def check_for_updates():
    try:
        response = requests.get("https://www.python.org/downloads/")
        response.raise_for_status()

        latest_version = response.text.split('<strong>Python ')[1].split('</strong>')[0]

        if latest_version > sys.version:
            update_message = "New version is available."
            update_button.config(text="Hide")
        else:
            update_message = "Your Python version is up to date."
            update_button.config(text="Check for Updates")

        update_label.config(text=update_message)

    except requests.exceptions.RequestException as e:
        update_label.config(text="Error checking for updates.")

def toggle_update_message():
    if update_button["text"] == "Check for Updates":
        check_for_updates()
        update_button.config(text="Hide")
    else:
        update_label.config(text="")
        update_button.config(text="Check for Updates")

# Get the list of files in the current directory
file_list = os.listdir()

# Filter out directories and non-Python files
current_file = os.path.basename(__file__)  # Get the name of the current file
file_list = [file for file in os.listdir() if file.endswith(".py") and file != current_file]

root = tk.Tk()
root.title("Gosha's SmartShell")

style = ttk.Style()
style.configure("TButton", foreground="blue", font=("Helvetica", 12))

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

file_label = ttk.Label(button_frame, text="Select File: ")
file_label.grid(row=0, column=0, padx=5)

file_dropdown = ttk.Combobox(button_frame, values=file_list, state="readonly")
file_dropdown.grid(row=0, column=1, padx=5)
file_dropdown.current(0)

analyze_button = ttk.Button(button_frame, text="Analyze Code", command=analyze_code)
analyze_button.grid(row=0, column=2, padx=5, pady=5)

package_label = ttk.Label(button_frame, text="Package: ")
package_label.grid(row=1, column=1, padx=5, pady=10)

package_entry = ttk.Entry(button_frame)
package_entry.grid(row=1, column=1, padx=5)

install_button = ttk.Button(button_frame, text="Install Package", command=install_package)
install_button.grid(row=1, column=2, padx=5)

# Inside the root window setup, create a button to toggle updates
update_button = ttk.Button(root, text="Check for Updates", command=toggle_update_message)
update_button.pack(anchor="nw", padx=10, pady=5)

# Create a label to display update information
update_label = ttk.Label(root, text="", font=("Helvetica", 10, "italic"))
update_label.pack(anchor="nw", padx=10, pady=5)

# Create a label for displaying Python version
version_label = ttk.Label(root, text=get_python_version(), font=("Helvetica", 10, "bold"))
version_label.pack(anchor="nw", padx=10, pady=5)

root.mainloop()
