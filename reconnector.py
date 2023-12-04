import subprocess
import time
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import threading
import re
import webbrowser

CONFIG_FILE = 'config.json'

# Utility functions for JSON handling
def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# GUI application
class App:
    def __init__(self, root):
        self.root = root
        self.should_stop = False  # Flag to control the script execution
        self.root.title('Conan Exiles Auto-Reconnect')
        self.status_label = tk.Label(root, text='Status: Not running', fg='red')
        self.status_label.grid(row=5, column=0, columnspan=3)
        self.config = load_config()

        # Labels and entries
        self.path_label = tk.Label(root, text='Path to ConanSandbox.exe (for first run):')
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.insert(0, self.config.get('game_path', ''))
        self.path_button = tk.Button(root, text='Browse', command=self.browse_file)
        self.path_label.grid(row=0, column=0, sticky='e')
        self.path_entry.grid(row=0, column=1)
        self.path_button.grid(row=0, column=2)

        # Default location label
        self.default_location_label = tk.Label(root, text='Default location: "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Conan Exiles\\ConanSandbox.exe"')
        self.default_location_label.grid(row=1, column=1, columnspan=2, sticky='w')

        # Position entry (display only)
        self.play_button_label = tk.Label(root, text='Position for "Continue" button:')
        self.play_button_position = tk.StringVar(root, value=self.config.get('play_button', 'Click "Train" to set'))
        self.play_button_entry = tk.Entry(root, textvariable=self.play_button_position, width=20, state='readonly')
        self.play_button_label.grid(row=2, column=0, sticky='e')
        self.play_button_entry.grid(row=2, column=1)

        # Train button
        self.train_button = tk.Button(root, text='Train', command=self.train_position)
        self.train_button.grid(row=2, column=2)

        # Made by label
        self.made_by_label = tk.Label(root, text='Made by Mijin for use on the Pandemonium PvE-C Server')
        self.made_by_label.grid(row=3, column=0, columnspan=3)

        # Start and Stop buttons
        self.start_button = tk.Button(root, text='Start', command=self.start_script)
        self.start_button.grid(row=4, column=0)
        self.stop_button = tk.Button(root, text='Stop', command=self.stop_script)
        self.stop_button.grid(row=4, column=1)

        # Discord button
        self.discord_button = tk.Button(root, text="Discord", command=lambda: self.open_link("https://discord.gg/4a67uWCc2h"))
        self.discord_button.grid(row=4, column=2)

        # Exit button
        self.exit_button = tk.Button(root, text='Exit', command=self.exit_script)
        self.exit_button.grid(row=4, column=3)

    def open_link(self, url):
        webbrowser.open_new(url)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("executable files", "*.exe"), ("all files", "*.*")))
        if filename:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filename)
            self.config['game_path'] = filename
            save_config(self.config)

    def start_script(self):
        self.status_label.config(text='Status: Running', fg='green')
        # Run the script actions in a separate thread to prevent UI freezing
        threading.Thread(target=self.script_actions, daemon=True).start()

    def script_actions(self):
        self.should_stop = False  # Reset the stop flag
        play_button_pos = self.play_button_position.get()

        # Verify user input
        if "Click" in play_button_pos:
            messagebox.showerror("Error", "Please train the position")
            return

        # Check if ConanSandbox.exe path is configured
        game_path = self.config.get('game_path')
        if game_path:
            log_file_path = os.path.join(os.path.dirname(game_path), 'ConanSandbox', 'Saved', 'Logs', 'ConanSandbox.log')

            # Monitor log file for disconnection and then attempt to reconnect
            while not self.should_stop:
                if self.monitor_log_for_disconnect(log_file_path, "Player disconnected"):
                    self.close_game()
                    time.sleep(30)  # Wait for 30 seconds

                self.launch_game()
                time.sleep(390)  # Wait for the game to launch and the launcher to load

                # Click the 'Continue' button
                play_button_x, play_button_y = map(int, play_button_pos.split(', '))
                self.click_button(play_button_x, play_button_y)

                # Check for "Welcomed by server" message, if not found within timeout, restart process
                if not self.monitor_log_for_disconnect(log_file_path, "Welcomed by server", timeout=150):
                    print("Failed to reconnect. Trying again...")
                    self.close_game()
                    time.sleep(30)  # Wait before trying to reconnect again
                else:
                    print("Reconnected successfully.")
                    break  # Exit loop if reconnected successfully

    def monitor_log_for_disconnect(self, log_file_path, pattern, timeout=None):
        pattern_compiled = re.compile(pattern, re.IGNORECASE)
        last_position = None
        start_time = time.time()

        while not self.should_stop and (timeout is None or time.time() - start_time < timeout):
            try:
                with open(log_file_path, 'r') as log_file:
                    if last_position is not None:
                        log_file.seek(last_position)
                    else:
                        log_file.seek(0, os.SEEK_END)

                    log_contents = log_file.read()
                    if pattern_compiled.search(log_contents):
                        last_position = log_file.tell()
                        return True
                    else:
                        last_position = log_file.tell()
            except Exception as e:
                print(f"Error reading log file: {e}")

            time.sleep(10)  # Check every 10 seconds

        return False

    def close_game(self):
        print("Closing game...")
        try:
            # Use taskkill to close the game
            if os.name == 'nt':
                os.system("taskkill /f /im ConanSandbox.exe")
        except Exception as e:
            print(f"Error closing game: {e}")

    def stop_script(self):
        self.should_stop = True  # Set the flag to stop script actions
        self.status_label.config(text='Status: Not running', fg='red')

    def exit_script(self):
        self.stop_script()  # Ensure the script is stopped
        self.root.destroy()  # Close the application

    def launch_game(self):
        """Launch Conan Exiles through Steam."""
        app_id = "440900"  # Conan Exiles AppID on Steam
        steam_url = f"steam://rungameid/{app_id}"
        try:
            if os.name == 'nt':  # If the system is Windows
                os.startfile(steam_url)
            else:
                subprocess.Popen(['xdg-open', steam_url])  # For Unix systems
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start the game through Steam: {e}")

    def click_button(self, x, y):
        """Click a button on the screen at the specified x, y coordinates."""
        print(f"Moving mouse to: x={x}, y={y}")  # Debugging output
        pyautogui.moveTo(x, y, duration=1)
        print("Click!")  # Debugging output
        pyautogui.click()
    
    def train_position(self):
        """Train the click position."""
        messagebox.showinfo("Training", "Move your mouse over the 'Continue' button and press 'Enter'.")
        self.root.update_idletasks()
        self.root.after(1000, self.capture_position)

    def capture_position(self):
        """Capture the position after a delay."""
        position = pyautogui.position()
        self.play_button_position.set(f"{position.x}, {position.y}")
        self.config['play_button'] = f"{position.x}, {position.y}"
        save_config(self.config)

# Main script execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
