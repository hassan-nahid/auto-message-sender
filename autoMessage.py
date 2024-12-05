import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui


class AutoMessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Message Sender")
        self.running = False
        self.count = 0
        self.include_counter = tk.BooleanVar(value=True)

        # UI Components
        self.label_message = tk.Label(root, text="Message:")
        self.label_message.pack(pady=5)
        self.entry_message = tk.Entry(root, width=40)
        self.entry_message.pack(pady=5)

        self.label_delay = tk.Label(root, text="Delay (seconds):")
        self.label_delay.pack(pady=5)
        self.delay_dropdown = ttk.Combobox(
            root, values=["0.1", "0.3", "0.5", "1.0", "2.0"], state="readonly"
        )
        self.delay_dropdown.pack(pady=5)
        self.delay_dropdown.set("0.3")  # Default value

        self.counter_checkbox = tk.Checkbutton(
            root, text="Include Counter", variable=self.include_counter
        )
        self.counter_checkbox.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.start_sending)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_sending)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.status_label = tk.Label(root, text="Status: Stopped", fg="red")
        self.status_label.pack(pady=10)

    def start_sending(self):
        message = self.entry_message.get().strip()
        try:
            delay = float(self.delay_dropdown.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please select a valid delay value.")
            return

        if not message:
            messagebox.showerror("Invalid Input", "Message cannot be empty.")
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running", fg="green")

        # Start a separate thread to send messages
        threading.Thread(
            target=self.send_messages, args=(message, delay), daemon=True
        ).start()

    def send_messages(self, message, delay):
        self.count = 0
        try:
            # Initial delay to allow the user to focus on the target
            time.sleep(3)  # 3-second delay before the first message

            while self.running:
                self.count += 1
                time.sleep(delay)  # User-defined delay for subsequent messages
                if self.include_counter.get():
                    full_message = f"{message} {self.count}"
                else:
                    full_message = message
                pyautogui.typewrite(full_message)
                pyautogui.press("enter")
                print(f"Sent message: {full_message}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop_sending()

    def stop_sending(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg="red")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMessageApp(root)
    root.mainloop()
