import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import threading

def run_csv_to_mqtt():
    """
    Placeholder function for running the CSV to MQTT script.
    Replace the content of this function with the actual logic or call to your script.
    """
    # Add actual logic here
    print("Running CSV to MQTT script...")
    # Simulate some work
    import time
    time.sleep(2)
    print("CSV to MQTT script completed successfully.")

def run_can_to_mqtt():
    """
    Placeholder function for running the CAN to MQTT script.
    Replace the content of this function with the actual logic or call to your script.
    """
    # Add actual logic here
    print("Running CAN to MQTT script...")
    # Simulate some work
    import time
    time.sleep(2)
    print("CAN to MQTT script completed successfully.")

def execute_in_thread(target):
    """
    Executes a given target function in a new thread.
    """
    thread = threading.Thread(target=target)
    thread.start()

def run_script(script_func):
    """
    Runs the specified script function in a thread and catches any exceptions.
    """
    try:
        execute_in_thread(script_func)
    except Exception as e:
        messagebox.showerror("Error", str(e))

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
    csv_button = tk.Button(window, text="Run CSV to MQTT", command=lambda: run_script(run_csv_to_mqtt))
    csv_button.grid(column=0, row=1, padx=10, pady=10)

    can_button = tk.Button(window, text="Run CAN to MQTT", command=lambda: run_script(run_can_to_mqtt))
    can_button.grid(column=1, row=1, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_gui()
