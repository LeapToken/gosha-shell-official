---

# Gosha's SmartShell

Gosha's SmartShell is an Open-Source python management tool available for everyone. It's a customizable and user-friendly interface packed with powerful features. Whether you're a tech enthusiast or a casual user, Gosha's SmartShell is designed to enhance your digital experience!

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system (check by running `python --version` or `python3 --version` in your terminal/command prompt).
- `pip` installed (Python's package installer).
- `git` installed (for cloning github repo)

## Installation

To install the necessary libraries for this project, follow these steps:

1. Clone the repository to your local machine:
```
git clone https://github.com/LeapToken/gosha-shell-official.git
```
2. Navigate to the project directory:
```
cd gosha-shell-official
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```

## Configuration

Before running the application, you need to configure it by setting up your OpenAI API key and ensuring all environment variables or configuration files are correctly set.

1. OpenAI API Key:
   - Obtain an API key from [OpenAI](https://openai.com/).
   - Replace `ENTER API KEY HERE` in the code with your actual API key.

2. Additional Configuration:
   - Ensure any file paths or external resources the script depends on are correctly set up in your environment.

## Usage

To use this project, follow these steps:

1. Navigate to the project directory
```
cd gosha-shell-official
```
2. Run the main script (assuming `main.py` is your entry script):
```
python main.py
```
3. Follow the `README` instructions below for detailed usage

### Short Guide

- `Select File: [dropdown]`: Shows files in the same directory as `main.py (SmartShell)`.
- `Run File`: Executes the current selected file in the dropdown.
- `Divider`: Prints a red line that separates code in the shell.
- `↻`: Restarts the SmartShell (Very Buggy).
- `AI Code Analysis`: Analyzes current selected file in the dropdown using ChatGPT.
- `pip install: [input] [dropdown]`: Custom `pip install` command with customized settings.
- `Run`: Executes the customized `pip install` command.
- `View Libraries`: Shows all installed libraries in the current environment in the shell.
- `Scan`: Scans for outdated packages.
- `Update Lib`:  Updates all outdated libraries.
- `Run CMD as background task`: Runs some command as background tasks.
- `*Select OS: [dropdown]`: By selecting your current OS, you will prevent errors for some functions.
- `Custom CMD: [input]`: Allows custom command to be executed.
- `Execute`: Executes the custom command.
- `Check for Updates`: Checks if your current Python Interpreter version is up-to-date.

### Important things to know
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) WARNING: Before launching SmartShell, make sure that the directory it is in has another .py file to prevent the `file_dropdown.current(0)` error (Meaning that the `Select File: [dropdown]` does not detect any .py files.
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) The `Run CMD as background task` only affects `Run`, `Update Lib`, `Execute`.
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Choosing a different OS than your own will cause some errors  in some functions.
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) The SmartShell is in early development and has a ton of bugs that will be fixed in further updates! If you wish to address any issues with the current version of the program, please refer to the LINK

### Functions Overview (For Developers)

- `ensure_rate_limit()`: Ensures API call rate limits are respected.
- `custom_chat_gpt(user_input)`: Sends user input to the ChatGPT model and returns its response.
- `generate_explanation(error_message)`: Generates explanations for errors using ChatGPT.
- `execute_external_code()`: Executes code from an external file safely.
- `analyze_code()`: Analyzes the current file (selected in the dropdown) using ChatGPT.
- `restart_program()`: Restarts Gosha's SmartShell (Very Buggy).
- `view_installed_packages()`: Runs 'pip list' command using terminal based on OS selection.
- `install_package()`: Collects package_name and cmd_option inputs for `install_package_thread`.
- `install_package_thread(package_name, cmd_option)`: Runs 'pip install [cmd_option] [package_name]'.
- `get_python_version()`: Checks current Python Interpreter version.
- `execute_command(command)`: Starts subprocess for custom command.
- `execute_command_thread()`: 'Execute' button configuration.
- `check_for_updates()`: Checks if the current Python version is up-to-date.
- `toggle_update_message()`: 'Check for Updates' button configuration.
- `run_selected_file()`: Runs current selected file in the dropdown.
- `print_red_divider()`: Outputs a red line to separate code.
- `scan_and_update_packages`: Scans outdated libraries (DOES NOT UPDATE THE PACKAGES).
- `update_all_packages()`: Updates the outdated libraries.
- `install_library(library_entry=None)`: UNUSED THE OFFICIAL PROGRAM (CAN BE DELETED)
- `get_num_rows()`: Calculates the number of rows in the current selected file in the dropdown (UNUSED IN THE OFFICAL PROGRAM)

## Contributing

Contributions to this project are welcome! Here's how you can help:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distribute under the MIT License. See `LICENSE` for more information.

## Contact

Georgii Taraskin - leaptoken@gmail.com

---
