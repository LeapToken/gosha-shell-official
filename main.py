import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading
import subprocess
from tkinter.ttk import Frame
import openai
import os
import sys
import requests
import time
from datetime import datetime
import webbrowser

last_api_call_time = 0

scanning_in_progress = False

# Set up your OpenAI API credentials
openai.api_key = "ENTER API KEY HERE"

messages = []

# Function to ensure a minimum time interval between API calls
def ensure_rate_limit():
    global last_api_call_time
    current_time = time.time()
    time_since_last_call = current_time - last_api_call_time
    if time_since_last_call < 2.0:  # Adjust the time interval as needed
        time.sleep(2.0 - time_since_last_call)
    last_api_call_time = time.time()

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
# Modify your analyze_code function to include rate limiting
def analyze_code():
    # Check if the OpenAI API key has been set
    if openai.api_key == "ENTER API KEY HERE":
        green_color = "\033[92m"  # ANSI escape code for green color
        reset_color = "\033[0m"  # Reset color to default
        print(green_color + "Please set the variable to your OpenAI API key!" + reset_color)
        return  # Exit the function early

    def background_task():
        selected_file = file_dropdown.get()

        with open(selected_file, "r") as file:
            code = file.read()

        ensure_rate_limit()  # Ensure rate limit compliance

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

def restart_program():
    """Restarts the current program based on the selected operating system, ensuring the terminal closes if applicable."""
    try:
        os_choice = os_dropdown.get()
        python_executable = sys.executable
        script_file = sys.argv[0]

        if os_choice == 'Windows':
            # For Windows, using start command without a window to detach the process
            subprocess.Popen(f'start /b {python_executable} {script_file}', shell=True)
        elif os_choice in ['MacOS', 'Linux']:
            # For MacOS and Linux, creating a completely detached process in a new terminal window might not close the original one
            # A workaround is needed for these OSes, possibly involving additional scripting to close terminals, which can be complex and vary greatly between setups
            if os_choice == 'MacOS':
                # Attempt to run the script in a way that doesn't keep the terminal open. This might not close the existing terminal window but doesn't open a new one.
                subprocess.Popen(
                    f'osascript -e \'tell application "Terminal" to do script "exec {python_executable} \\"{script_file}\\""\'',
                    shell=True)
            else:
                # For Linux, the method to close the terminal after execution depends on the terminal emulator
                # This example uses gnome-terminal to run the script then exits, but it might not close the original terminal
                subprocess.Popen(f'gnome-terminal -- {python_executable} {script_file}', shell=True)

        # Exiting the current script to allow the new instance to run independently
        sys.exit()

    except Exception as e:
        print(f"Error restarting the program: {e}")

# View all installed packages in a separate thread
def view_installed_packages():
    def view_packages_thread():
        try:
            selected_os = os_dropdown.get()
            if selected_os == 'Windows':
                subprocess.run(["cmd.exe", "/C", "pip list"], check=True, shell=True, cwd=os.path.dirname(__file__))
            elif selected_os in ['MacOS', 'Linux']:
                subprocess.run(["pip", "list"], check=True, cwd=os.path.dirname(__file__))
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    # Start the view packages process in a background thread
    threading.Thread(target=view_packages_thread).start()

def install_package():
    package_name = package_entry.get()  # Assuming package_entry is defined somewhere
    cmd_option = cmd_options_dropdown.get()  # Assuming cmd_options_dropdown is defined somewhere

    if package_name:
        install_button.config(text="Installing...", state=tk.DISABLED)
        install_thread = threading.Thread(target=install_package_thread, args=(package_name, cmd_option))
        install_thread.start()

# Thread function to perform the actual installation
def install_package_thread(package_name, cmd_option):
    if cmd_option and cmd_option not in [' ', '']:
        if cmd_option in ['-U', '-q', '-e', '-i', '--extra-index-url']:
            command = ["pip", "install", cmd_option, package_name]
        else:
            command = ["pip", "install", package_name, cmd_option]
    else:
        command = ["pip", "install", package_name]

    try:
        if run_in_background.get():  # If the checkbox is checked
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command, check=True)
        install_button.config(text="Run", state=tk.NORMAL)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        install_button.config(text="Run", state=tk.NORMAL)

def get_python_version():
    return f"Python {sys.version}"

def execute_command(command):
    if run_in_background.get():  # If the checkbox for running in the background is checked
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.communicate()  # This is just to let the process run and finish, we're ignoring output/error
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if process.returncode == 0:
            print(f"Output:\n{output.decode()}")
        else:
            print(f"Error:\n{error.decode()}")

def execute_command_thread():
    # Get the command from the entry (assuming custom_cmd_entry is defined somewhere in your Tkinter setup)
    cmd = custom_cmd_entry.get()

    # Change the button text to "Executing..." and set it to disabled state
    execute_btn.config(text="Executing...", state=tk.DISABLED)

    def execute_with_feedback():
        execute_command(cmd)
        # After command execution is complete, revert button text and enable it again
        execute_btn.config(text="Execute", state=tk.NORMAL)

    # Start a thread to execute the command
    threading.Thread(target=execute_with_feedback).start()

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


# Function to run the selected file and print a completion message
def run_selected_file():
    selected_file = file_dropdown.get()
    try:
        # Get the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print the completion message in green
        green_color = "\033[92m"  # ANSI escape code for green color
        reset_color = "\033[0m"  # Reset color to default
        completion_message = f"'{selected_file}' completed run at ({current_time}):"
        print(green_color + completion_message + reset_color)

        with open(selected_file, "r") as file:
            code = file.read()
        exec(code)
    except Exception as e:
        print(f"Error: {e}")

# Function to print a red divider line
def print_red_divider():
    # ANSI escape code for red color
    red_color = "\033[91m"
    reset_color = "\033[0m"  # Reset color to default
    divider = red_color + "-------------------------------------------------------------" + reset_color
    print(divider)


# Function to scan and update all installed packages
def scan_and_update_packages():
    global scanning_in_progress

    # Disable the Scan button while scanning is in progress
    scan_button.config(state=tk.DISABLED)
    scan_button.config(text="Scanning...")

    def scan_thread():
        try:
            # Run the "pip list --outdated" command to list outdated packages
            subprocess.run(["pip", "list", "--outdated"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        # Re-enable the Scan button and reset its text
        scan_button.config(state=tk.NORMAL)
        scan_button.config(text="Scan")
        scanning_in_progress = False

    # Start scanning in a separate thread
    scanning_in_progress = True
    threading.Thread(target=scan_thread).start()

def update_all_packages():
    # Disable the Update button while updating is in progress and change its text
    updatelib.config(state=tk.DISABLED)
    updatelib.config(text="Updating...")

    def update_thread():
        try:
            # Run the "pip list --outdated" command and capture its output
            result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True, check=True)
            lines = result.stdout.split('\n')[2:]  # Skip the header lines
            packages = [line.split(' ')[0] for line in lines if line]

            # Update each package
            for package in packages:
                if run_in_background.get():  # If the checkbox for running in the background is checked
                    subprocess.run(["pip", "install", "--upgrade", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run(["pip", "install", "--upgrade", package], check=True)
                print(f"Updated {package}")  # Optional: Update GUI or console with progress
        except subprocess.CalledProcessError as e:
            print(f"Error during update: {e}")

        # Re-enable the Update button and reset its text after updates are complete
        updatelib.config(state=tk.NORMAL)
        updatelib.config(text="Update Lib")
        print("All packages are up-to-date!")

    # Start the update process in a separate thread
    threading.Thread(target=update_thread).start()

def get_num_rows(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        return 0

# Get the list of files in the current directory
file_list = os.listdir()

# Filter out directories and non-Python files
current_file = os.path.basename(__file__)  # Get the name of the current file
file_list = [file for file in os.listdir() if file.endswith(".py") and file != current_file]

root = tk.Tk()
root.title("Gosha's SmartShell")

run_in_background = tk.BooleanVar(value=False)

style = ttk.Style()
style.configure("TButton", foreground="blue", font=("Helvetica", 12))

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

file_label = ttk.Label(button_frame, text="Select File: ")
file_label.grid(row=0, column=0, padx=5)

file_dropdown = ttk.Combobox(button_frame, values=file_list, state="readonly")
file_dropdown.grid(row=0, column=1, padx=5)
file_dropdown.current(0)

# Run button
run_button = ttk.Button(button_frame, text="Run File", command=run_selected_file)
run_button.grid(row=0, column=2, padx=5, pady=5)

# Divider button
divider_button = ttk.Button(button_frame, text="Divider", command=print_red_divider)
divider_button.grid(row=0, column=3, padx=5, pady=5)

# Analyze Code button
analyze_button = ttk.Button(button_frame, text="AI Code Analysis", command=analyze_code)
analyze_button.grid(row=1, column=2, padx=5, pady=5)

file_label = ttk.Label(button_frame, text="pip install: ")
file_label.grid(row=2, column=0, padx=5)

background_checkbox = tk.Checkbutton(button_frame, text="Run CMD as background task", variable=run_in_background)
background_checkbox.grid(row=3, column=1, padx=5, pady=5)

package_entry = ttk.Entry(button_frame)
package_entry.grid(row=2, column=1, padx=5)

# Install Package button
install_button = ttk.Button(button_frame, text="Run", command=install_package)
install_button.grid(row=2, column=3, padx=5, pady=5)

# Create a button to view installed packages
view_packages_button = ttk.Button(button_frame, text="View Libraries", command=view_installed_packages)
view_packages_button.grid(row=2, column=4, padx=5, pady=5)

# Create a Scan button
scan_button = ttk.Button(button_frame, text="Scan", command=scan_and_update_packages)
scan_button.grid(row=2, column=5, padx=5, pady=5)

updatelib = ttk.Button(button_frame, text="Update Lib", command=update_all_packages)
updatelib.grid(row=3, column=5, padx=5, pady=5)

# OS Choices
os_choices = ['Windows', 'MacOS', 'Linux']
os_label = ttk.Label(button_frame, text="*Select OS: ")
os_label.grid(row=4, column=0, padx=5, pady=5)

os_dropdown = ttk.Combobox(button_frame, values=os_choices, state="readonly")
os_dropdown.grid(row=4, column=1, padx=5, pady=5)
os_dropdown.current(0)  # Default to Windows

# Restart button
restart_button = ttk.Button(button_frame, text="↻", command=restart_program)
restart_button.grid(row=0, column=5, padx=5, pady=5)

# Library Install Options
cmd_options = ['', '-q', '-e', '-U', '-i', '--no-deps', '--user', '--force-reinstall', '--extra-index-url', '--no-cache-dir', '--pre', '--require-hashes']
cmd_options_dropdown = ttk.Combobox(button_frame, values=cmd_options, state="readonly")
cmd_options_dropdown.grid(row=2, column=2, padx=5)
cmd_options_dropdown.current(0)  # Default to the first option

cmd_frame: Frame = ttk.Frame(root)
cmd_frame.pack(pady=10, padx=10, fill="x", expand=True)

custom_cmd_label = Label(cmd_frame, text="Custom CMD:")
custom_cmd_label.grid(column=0, row=1, sticky=E, padx=5)

custom_cmd_entry = Entry(cmd_frame, width=30)
custom_cmd_entry.grid(column=1, row=1, padx=5)

execute_btn = ttk.Button(cmd_frame, text="Execute", style="TButton", command=execute_command_thread)
execute_btn.grid(column=2, row=1, padx=5)

# Create a button to toggle updates
update_button = ttk.Button(root, text="Check for Updates", command=toggle_update_message)
update_button.pack(anchor="nw", padx=10, pady=5)

# Create a label to display update information
update_label = ttk.Label(root, text="", font=("Helvetica", 10, "italic"))
update_label.pack(anchor="nw", padx=10, pady=5)

# Create a label for displaying Python version and center the text horizontally
version_label = ttk.Label(root, text=f"{get_python_version()} | Gosha's SmartShell v1.3.1", font=("Helvetica", 10, "bold"))
version_label.pack(fill="x", padx=10, pady=5)

root.mainloop()
