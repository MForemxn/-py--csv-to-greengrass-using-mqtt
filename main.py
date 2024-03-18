import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import threading
import subprocess
import sys
import os

# Determine the directory of the main.py script
script_dir = os.path.dirname(__file__)

# Define the paths to the other scripts relative to the location of main.py
csv_script_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/csv to mqtt for aws/csv to aws.py'
can_script_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/csv to mqtt for aws/canbus to aws.py'

def run_script_external(file_name):
    """
    Runs an external Python script in a subprocess and captures its output.
    """
    try:
        # Run the script and capture output
        process = subprocess.Popen(['python', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Continuous output
        for line in process.stdout:
            print(line, end="")
        # Wait for the subprocess to finish
        process.wait()
        # Check if the process ended with an error
        if process.returncode != 0:
            # Read error output
            error_msg = process.stderr.read()
            print(f"Error running script {file_name}: {error_msg}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def execute_in_thread(target, args):
    """
    Executes a given target function with arguments in a new thread.
    """
    thread = threading.Thread(target=target, args=args)
    thread.start()

def setup_gui():
    """
    Sets up the GUI window and widgets.
    """
    window = tk.Tk()
    window.title("MQTT Script Runner")

    # Text widget for output
    output_text = scrolledtext.ScrolledText(window, width=70, height=20)
    output_text.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

    # Redirect print statements to the text widget
    def redirect_print_to_widget(text_widget):
        class TextRedirector(object):
            def __init__(self, widget):
                self.widget = widget

            def write(self, str):
                self.widget.insert(tk.END, str)
                self.widget.see(tk.END)

            def flush(self):
                pass

        sys.stdout = TextRedirector(text_widget)

    redirect_print_to_widget(output_text)

    # Buttons to run scripts
    csv_button = tk.Button(window, text="Run CSV to MQTT", command=lambda: execute_in_thread(run_script_external, (csv_script_path,)))
    csv_button.grid(column=0, row=1, padx=10, pady=10)

    can_button = tk.Button(window, text="Run CAN to MQTT", command=lambda: execute_in_thread(run_script_external, (can_script_path,)))
    can_button.grid(column=1, row=1, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_gui()
