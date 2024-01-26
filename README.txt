Conan Exiles Auto-Reconnector Script Version 1.3
-------------------------------------

Updates: Added the function to adjust wait times, and changed the way the script detects the continue button to fix an issue for some users.

-------------------------------------

Created by Mijin, this script is tailored for "Conan Exiles", specifically for the Pandemonium PvE-C server. It automates handling disconnections, reconnecting players using a graphical user interface.

Key Functionalities
-------------------

1. Configuration Management: Manages user settings, including the game path.
2. Session Monitoring: Detects disconnections by monitoring a session file.
3. Auto-Reconnection: Relaunches the game and clicks 'Continue' upon disconnection.
4. User Interface: Offers a GUI for script activation, game path setup, and 'Continue' button training.
5. Custom Settings: Allows modification of settings like disconnect wait time and session monitor time.

This script enhances players' online activity, aiding in collecting "payouts" for staying logged in, especially during server restarts or disconnections. It benefits players by increasing in-game currency and keeps player counts high.

Installation and Setup
----------------------

1. Download reconnector.zip from the release page (scroll to the very bottom): https://github.com/Mijin-Gakure/reconnector/releases/tag/v1.3.0
   - ![Download Zip Image:](https://i.imgur.com/NCvGDJ4.png)

2. Ignore antivirus warnings (false positives). For assurance, check the GitHub source.
   - ![Warning Image:](https://i.imgur.com/wgBfvjf.png)
   - ![Download Anyway Image:](https://i.imgur.com/paLtpfh.png)

3. Extract the reconnector folder to a desired location (e.g., Desktop).
   - ![Extract Folder Image:](https://i.imgur.com/XqnnihM.png)

4. Open `reconnector.exe` from the folder.
   - ![Open reconnector.exe Image:](https://i.imgur.com/4xzf5yn.png)

5. Click 'Browse' and navigate to `ConanSandbox.exe` (usually in "C:\Program Files (x86)\Steam\steamapps\common\Conan Exiles\ConanSandbox.exe").
   - ![Find Game Path Image:](https://i.imgur.com/FKSMnv7.png, https://i.imgur.com/eQsvhzs.png)

6. Tell the script how to find the 'Continue' button position:
   - Press `Ctrl` + `PrtScn` to take a screenshot of the Conan Exiles launcher. Then open Paint (`Win` + `R`, type `mspaint`).
   - Paste (`Ctrl` + `V`) to paste the image in paint, use the selection tool to frame the 'Continue' button. Leave some margin around the button.
     - ![Selection Tool Image:](https://i.imgur.com/VvtqLFB.png)
   - Crop the image (`Ctrl` + `Shift` + `X`).
     - ![Crop Image:](https://i.imgur.com/UQivHms.png)
   - Save as `continue.png` in the reconnector folder (overwrite the existing file).

7. Lastly, I've added timer configuration options for people with slower computers or for those who want to try to increase the speed a bit.

**Disconnect Wait Time** is the amount of time the script waits after detecting a disconnection and before attempting to relaunch the game. If your computer is slower, you may want to increase this slightly to allow the game enough time to close. The default setting is usually adequate.

**Relaunch Wait Time** is the duration the script waits before attempting to reconnect after disconnecting. The default setting is recommended as it allows enough time for server restarts, should that be the reason for your disconnection.

**Session Monitor Time** is how long the script will monitor the game's session file for changes, confirming whether the game has successfully reconnected after a disconnect. This is the setting you'll want to increase if you're on a slower computer. Slower computers take longer to boot the game, so 2 minutes might not be sufficient. If the reconnector script is clicking the continue button but isn't working as intended, you likely need to increase this number; try setting it to 250.

Starting the Script:

To use the script, empty your inventory in a safe place before going AFK and head to the Teleport Hub (also known as Hall of Transference) on our Exiled Lands server. It's crucial to empty your inventory first because I cannot guarantee that you won't die while AFK. The hub is designed to be a safe zone, but occasionally it may fail, and you might die from starvation. In the event that you do die, I have set it up to respawn you back into the hub. Being in the Teleport Hub now awards you two gold per hour instead of the usual one.

If you like you can decrease the games resolution, change the graphics settings to low end laptop mode, and even adjust windows power saver settings if you like. It's possible turn your computer screen off in some circumstances, on some setups it may not be (specifically some laptops) because even forcing the screen off in CMD on them often causes them to go into sleep mode, there are work arounds through regedit that are too complex to go into detail here about.


Mod Configurations
------------------

1. Ensure your mods/load order matches the server's. Launch the game, go to 'MODS', and arrange accordingly.
   - ![Mods Image:](https://i.imgur.com/DYQz6jH.png)
   - ![Server's Load Order Image:](https://i.imgur.com/ybTjiUz.png)

Support
-------

For assistance, join my Discord: https://discord.gg/EFWjq5wwtz