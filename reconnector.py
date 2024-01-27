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
import sys

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

        # Removed position entry and train button as they are not needed with image recognition
        # Removed made by label as it does not affect functionality

        # Start button
        self.start_button = tk.Button(root, text='Start', command=self.start_script)
        self.start_button.grid(row=2, column=0)  # Changed to row 2 to fill in space left by removed elements

        # Discord button
        self.discord_button = tk.Button(root, text="Discord", command=lambda: self.open_link("https://discord.gg/4a67uWCc2h"))
        self.discord_button.grid(row=2, column=2)  # Changed to row 2 to fill in space left by removed elements

        # Exit button
        self.exit_button = tk.Button(root, text='Exit', command=self.exit_script)
        self.exit_button.grid(row=2, column=3)  # Changed to row 2 to fill in space left by removed elements

  # Time settings
        self.time_settings_label = tk.Label(root, text='Time Settings (seconds):')
        self.time_settings_label.grid(row=7, column=0, columnspan=3)

        self.disconnect_wait_label = tk.Label(root, text='Disconnect Wait Time:')
        self.disconnect_wait_entry = tk.Entry(root, width=20)
        self.disconnect_wait_entry.insert(0, self.config.get('disconnect_wait_time', 30))
        self.disconnect_wait_label.grid(row=8, column=0, sticky='e')
        self.disconnect_wait_entry.grid(row=8, column=1)

        self.relaunch_wait_label = tk.Label(root, text='Relaunch Wait Time:')
        self.relaunch_wait_entry = tk.Entry(root, width=20)
        self.relaunch_wait_entry.insert(0, self.config.get('relaunch_wait_time', 390))
        self.relaunch_wait_label.grid(row=9, column=0, sticky='e')
        self.relaunch_wait_entry.grid(row=9, column=1)

        # Insert the new GUI elements here for session monitor time
        self.session_monitor_label = tk.Label(root, text='Session Monitor Time:')
        self.session_monitor_entry = tk.Entry(root, width=20)
        self.session_monitor_entry.insert(0, self.config.get('session_monitor_time', 120))  # Default value 120
        self.session_monitor_label.grid(row=11, column=0, sticky='e')
        self.session_monitor_entry.grid(row=11, column=1)

        self.save_time_settings_button = tk.Button(root, text='Save Time Settings', command=self.save_time_settings)
        self.save_time_settings_button.grid(row=12, column=1)

    def open_link(self, url):
        webbrowser.open_new(url)

    def save_time_settings(self):
        # Get values from the GUI entries
        disconnect_wait_time = int(self.disconnect_wait_entry.get())
        relaunch_wait_time = int(self.relaunch_wait_entry.get())
        session_monitor_time = int(self.session_monitor_entry.get())
        session_monitor_time = int(self.session_monitor_entry.get())
        self.config['session_monitor_time'] = session_monitor_time

        # Update the config dictionary
        self.config['disconnect_wait_time'] = disconnect_wait_time
        self.config['relaunch_wait_time'] = relaunch_wait_time
        self.config['session_monitor_time'] = session_monitor_time

        # Save the updated config to the file
        save_config(self.config)

        # Show a message box indicating successful save
        messagebox.showinfo("Settings Saved", "Time settings have been updated and saved.")       

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

    def click_continue_button(self):
        print("Locating the 'Continue' button on the screen...")

        # Determine the directory of the executable
        if getattr(sys, 'frozen', False):
            # If running as a standalone executable
            application_dir = os.path.dirname(sys.executable)
        else:
            # If running as a script
            application_dir = os.path.dirname(os.path.abspath(__file__))

        # Path to the continue button image
        continue_button_path = os.path.join(application_dir, 'continue.png')

        # Locate the 'Continue' button on screen and click it
        continue_button_location = pyautogui.locateOnScreen(continue_button_path, confidence=0.8)
        if continue_button_location:
            continue_button_x, continue_button_y = pyautogui.center(continue_button_location)
            pyautogui.click(continue_button_x, continue_button_y)
            print("Clicked the 'Continue' button.")
        else:
            print("Could not find the 'Continue' button on screen.")
                
    def handle_disconnect(self):
        print("Handling disconnection...")
        self.close_game()
        self.sleep_with_update(self.config.get('disconnect_wait_time', 30))  # Wait before relaunching game
        self.launch_game()
        self.sleep_with_update(self.config.get('relaunch_wait_time', 390))  # Wait for game to launch
        self.click_continue_button()  # Click the 'Continue' button using image recognition

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
                self.handle_disconnect()

            # Use the session monitor time from the configuration
            session_monitor_time = self.config.get('session_monitor_time', 120)  # Default value 120
            if not self.monitor_session_file(wait_time=session_monitor_time):
                print(f"No reconnection detected within {session_monitor_time} seconds. Attempting reconnection.")
                self.handle_disconnect()  # Attempt to reconnect

            # Wait between checks
            self.sleep_with_update(10)

            # Check if stop button was pressed
            if self.should_stop:
                print("Stop button pressed. Exiting script_actions loop.")
                break
                
            # This makes the script wait between functions
            self.sleep_with_update(10)

    def monitor_session_file(self, wait_time):
        session_monitor_time = wait_time  # Use wait_time as the session monitor time
        print(f"Monitoring session file for {session_monitor_time} seconds to confirm reconnection.")
        try:
            last_mod_time = os.path.getmtime(self.session_file_path)
            print(f"Initial session file mod time: {last_mod_time}")
        except FileNotFoundError:
            print(f"Session file not found: {self.session_file_path}")
            return False

        start_time = time.time()
        while time.time() - start_time < session_monitor_time and not self.should_stop:
            try:
                current_mod_time = os.path.getmtime(self.session_file_path)
                print(f"Current session file mod time: {current_mod_time}")
                if current_mod_time != last_mod_time:
                    print("Session file modified, player likely reconnected.")
                    return True
            except Exception as e:
                print(f"Error accessing session file: {e}")
            time.sleep(10)
            self.update_timer(session_monitor_time - int(time.time() - start_time))

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
        
    def parse_log_time(self, log_line):
        # Extract and parse the timestamp from the log line
        match = re.search(r"\[([0-9]{4}\.[0-9]{2}\.[0-9]{2}-[0-9]{2}\.[0-9]{2}\.[0-9]{2}:[0-9]{3})\]", log_line)
        if match:
            timestamp_str = match.group(1)
            log_datetime = datetime.datetime.strptime(timestamp_str, "%Y.%m.%d-%H.%M.%S:%f")
            return log_datetime
        return None

    def click_continue_button(self):
        print("Locating the 'Continue' button on the screen...")

        # Determine the directory of the executable or script
        application_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

        # Path to the continue button image
        continue_button_path = os.path.join(application_dir, 'continue.png')

        # Locate the 'Continue' button on screen and click it
        continue_button_location = pyautogui.locateOnScreen(continue_button_path, confidence=0.8)
        if continue_button_location:
            continue_button_x, continue_button_y = pyautogui.center(continue_button_location)
            pyautogui.click(continue_button_x, continue_button_y)
            print("Clicked the 'Continue' button.")
        else:
            print("Could not find the 'Continue' button on screen.")

# Main script execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()