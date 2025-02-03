import tkinter as tk
import threading
import time
import winsound  # For generating beep sound on Windows

class SafetyCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Safety Check")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="", font=("Arial", 16))
        self.label.pack(pady=20)

        self.yes_button = tk.Button(root, text="Yes", command=self.on_yes)
        self.yes_button.pack(pady=10)

        self.is_safe = False
        self.check_interval = 60  # Check every 60 seconds
        self.response_time = 30  # 30 seconds to respond
        self.alert_mode = True  # Set to True to start the alert mode

        if self.alert_mode:
            self.start_checking()

    def start_checking(self):
        self.label.config(text="Are you safe?")
        self.yes_button.pack(pady=10)  # Show the Yes button
        self.root.after(self.check_interval * 1000, self.wait_for_response)

    def wait_for_response(self):
        self.label.config(text="Please respond within 30 seconds.")
        self.root.after(self.response_time * 1000, self.alert_user)

    def alert_user(self):
        if not self.is_safe:
            # Start beeping in a separate thread
            threading.Thread(target=self.beep_for_30_seconds).start()
            self.label.config(text="Location is being shared to registered mobile number and the nearest police station.")
            self.yes_button.pack_forget()  # Hide the Yes button

    def beep_for_30_seconds(self):
        end_time = time.time() + 30  # Beep for 30 seconds
        while time.time() < end_time:
            winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms

    def on_yes(self):
        self.is_safe = True
        self.label.config(text="We will check on you after 1 minute.")
        self.yes_button.pack_forget()  # Hide the Yes button
        self.root.after(60000, self.reset_check)  # Wait for 1 minute before resetting

    def reset_check(self):
        self.is_safe = False
        self.start_checking()  # Restart the safety check

if __name__ == "__main__":
    root = tk.Tk()
    app = SafetyCheckApp(root)
    root.mainloop()