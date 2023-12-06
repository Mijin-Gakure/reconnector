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
import datetime

CONFIG_FILE = 'config.json'

# Utility functions for JSON handling
def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            print("Loading configuration file.")
            return json.load(f)
    else:
        print("Configuration file not found, loading defaults.")
        return {}

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("Configuration saved successfully.")
    except Exception as e:
        print(f"Error saving configuration: {e}")

# GUI application
class App:
    def __init__(self, root):
        self.root = root
        self.should_stop = False
        self.timer_label = None
        self.root.title('Conan Exiles Auto-Reconnect')
        self.status_label = tk.Label(root, text='Status: Not running', fg='red')
        self.status_label.grid(row=5, column=0, columnspan=3)
        self.config = load_config()
        self.is_reconnecting = False  # New state variable
        
        # Construct the session file path based on the game path in the config
        game_path = self.config.get('game_path', '')
        if game_path:
            game_dir = os.path.dirname(game_path)
            self.session_file_path = os.path.join(game_dir, 'ConanSandbox', 'Saved', 'Logs', 'session-length-tracker.json')
        else:
            self.session_file_path = ''        

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

        # Start button
        self.start_button = tk.Button(root, text='Start', command=self.start_script)
        self.start_button.grid(row=4, column=0)

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

    def update_timer(self, remaining_time):
        if self.timer_label:
            self.timer_label.config(text=f"Next action in: {remaining_time} seconds")
            self.root.update()

    def start_script(self):
        self.should_stop = False
        self.status_label.config(text='Status: Running', fg='green')
        self.timer_label = tk.Label(self.root, text='Next action in: 0 seconds')
        self.timer_label.grid(row=6, column=0, columnspan=3)
        print("Starting script...")
        threading.Thread(target=self.script_actions, daemon=True).start()
                
    def handle_disconnect(self):
        print("Handling disconnection...")
        self.close_game()
        self.sleep_with_update(30)  # Wait before relaunching game
        self.launch_game()
        self.sleep_with_update(390)  # Wait for game to launch before clicking 'Continue'

        # Extract coordinates for the 'Continue' button from the configuration
        play_button_x, play_button_y = map(int, self.play_button_position.get().split(', '))
        self.click_button(play_button_x, play_button_y)

    def monitor_log_for_disconnect(self, check_interval=15):
        print("Checking for disconnection...")
        try:
            last_mod_time = os.path.getmtime(self.session_file_path)
            print(f"Last modification time: {last_mod_time}")
        except FileNotFoundError:
            print("Session file not found. Assuming disconnection.")
            return True

        time.sleep(check_interval)
        try:
            current_mod_time = os.path.getmtime(self.session_file_path)
            print(f"Current modification time: {current_mod_time}")
            if current_mod_time == last_mod_time:
                print("No change in session file detected. Assuming disconnection.")
                return True
        except Exception as e:
            print(f"Error accessing session file: {e}")
            return False

        print("Change detected in session file. No disconnection.")
        return False

    def script_actions(self):
        print("Script actions started.")
        while not self.should_stop:
            print("Top of script_actions loop.")

            # Check for disconnection
            if self.monitor_log_for_disconnect():
                print("Disconnect detected. Handling disconnection.")
                self.handle_disconnect()  # Step 1: Close the game

                # Step 2: Relaunch the game and click 'Continue'
                self.relaunch_game_and_click_continue()

                # Step 3: Monitor the session file independently for 390 seconds
                if not self.monitor_session_file(wait_time=120):
                    print("No reconnection detected within 120 seconds. Repeating the process.")
                    continue  # Go back to the start of the while loop

            # Wait between checks
            self.sleep_with_update(10)

            # Check if stop button was pressed
            if self.should_stop:
                print("Stop button pressed. Exiting script_actions loop.")
                break
                
            # This makes the script wait between functions
            self.sleep_with_update(10)

    def monitor_session_file(self, wait_time=180):
        print(f"Monitoring session file for {wait_time} seconds to confirm reconnection.")
        try:
            last_mod_time = os.path.getmtime(self.session_file_path)
            print(f"Initial session file mod time: {last_mod_time}")
        except FileNotFoundError:
            print(f"Session file not found: {self.session_file_path}")
            return False

        start_time = time.time()
        while time.time() - start_time < wait_time and not self.should_stop:
            try:
                current_mod_time = os.path.getmtime(self.session_file_path)
                print(f"Current session file mod time: {current_mod_time}")
                if current_mod_time != last_mod_time:
                    print("Session file modified, player likely reconnected.")
                    return True
            except Exception as e:
                print(f"Error accessing session file: {e}")
            time.sleep(10)  # how frequently it checks the session file for the time set above at wait_time for monitor_session_file, after the time is up it's knows a player has reconnected as long as there was a change
            self.update_timer(wait_time - int(time.time() - start_time))

        print("No change in session file detected.")
        return False


    def sleep_with_update(self, sleep_time):
        for remaining in range(sleep_time, 0, -1):
            self.update_timer(remaining)
            time.sleep(1)
            if self.should_stop:
                break

    def close_game(self):
        print("Attempting to close the game...")
        try:
            if os.name == 'nt':
                subprocess.run(["taskkill", "/f", "/im", "ConanSandbox.exe"], capture_output=True)
                print("Game close command issued.")
            else:
                print("Game close command not executed. Non-Windows OS detected.")
        except Exception as e:
            print(f"Error closing game: {e}")

    def stop_script(self):
        self.should_stop = True
        self.status_label.config(text='Status: Not running', fg='red')
        if self.timer_label:
            self.timer_label.config(text='')

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
        self.click_time = time.time()  # Record the time of the click
        
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
        
    def parse_log_time(self, log_line):
        # Extract and parse the timestamp from the log line
        match = re.search(r"\[([0-9]{4}\.[0-9]{2}\.[0-9]{2}-[0-9]{2}\.[0-9]{2}\.[0-9]{2}:[0-9]{3})\]", log_line)
        if match:
            timestamp_str = match.group(1)
            log_datetime = datetime.datetime.strptime(timestamp_str, "%Y.%m.%d-%H.%M.%S:%f")
            return log_datetime
        return None

    def relaunch_game_and_click_continue(self):
        print("Relaunching game.")
        self.launch_game()
        self.sleep_with_update(20)  # Wait for game to launch before clicking 'Continue'

        # Extract coordinates for the 'Continue' button from the configuration
        play_button_x, play_button_y = map(int, self.play_button_position.get().split(', '))
        self.click_button(play_button_x, play_button_y)

# Main script execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()