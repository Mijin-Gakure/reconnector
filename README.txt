Conan Exiles Auto-Reconnector Script
-------------------------------------

This script is designed by me, Mijin, specifically for the "Conan Exiles" game, particularly for the Pandemonium PvE-C server. It automates the handling of disconnections and reconnects the player using a graphical user interface (GUI).

Key Functionalities
-------------------

1. Configuration Management: Loads and saves user configurations, like the game path.
2. Session Monitoring: Monitors a session file to detect disconnections.
3. Auto-Reconnection: Closes and automatically relaunches the game upon disconnection, then clicks the 'Continue' button to reconnect.
4. User Interaction: Features a GUI for starting the script, setting the game path, and training the position of the 'Continue' button.
5. Flexibility and Feedback: Allows users to stop the script anytime and provides status updates.
6. Custom Settings: Supports customization of settings like the game path and 'Continue' button position.

This script aims to enhance players' ability to collect "payouts" for online activity by remaining logged in, even during server restarts or connection losses. This benefits both the players, who earn more in-game currency, and the server owner, who maintains higher player counts.

How to Use
----------

Installation and Setup:

1. Visit the release page and download reconnector.zip: https://github.com/Mijin-Gakure/reconnector/releases/tag/v1.2.1
   Download Zip Image: https://i.imgur.com/NCvGDJ4.png

2. After downloading, you might receive a warning as the file is not digitally signed. This is a false positive. If concerned, you can verify the source files on GitHub.
   Warning Image: https://i.imgur.com/wgBfvjf.png
   Download Anyway Image: https://i.imgur.com/paLtpfh.png

3. Extract the reconnector folder from the downloaded zip file to a location of your choice (e.g., Desktop).
   Extract Folder Image: https://i.imgur.com/XqnnihM.png

4. Open reconnector.exe from the extracted folder.
   Open reconnector.exe Image: https://i.imgur.com/4xzf5yn.png

5. Click 'Browse' and navigate to ConanSandbox.exe. The default location is usually "C:\Program Files (x86)\Steam\steamapps\common\Conan Exiles\ConanSandbox.exe".
   Find Game Path Image: https://i.imgur.com/eQsvhzs.png

6. Open the Conan launcher, then click 'Train' in the GUI.
   Launcher Image: https://i.imgur.com/L9OSjfr.png
   Train Button Image: https://i.imgur.com/OcHKeSN.png

7. Hover your mouse over the 'Continue' button on the launcher and press 'Enter'. Do not click 'OK' on the pop-up.
   Hover Mouse Image: https://i.imgur.com/QlMs3jq.png

Both the game path and continue button position are now saved. You only need to perform these steps once unless a mistake is made.

Starting the Script:

To use the script, after the game is running and you're ready to AFK, open reconnector.exe and click 'Start'. The script will handle disconnections by closing and reopening the game, then clicking 'Continue' to rejoin the last server.

Setting Up Mod Configurations:

For optimal performance, ensure your mods/load order matches the server's requirements. This setup is critical for the script to function correctly.

1. Launch the game and go to 'MODS'.
   Mods Image: https://i.imgur.com/DYQz6jH.png

2. Arrange your mods to match the server's load order. For Pandemonium PvE-C, it should be Pippi, then ModControlPanel, followed by Less Building Placement Restrictions (unless I add more later).

Additional Resources:

- Setup Video: https://www.youtube.com/watch?v=UI7nRrchEK8&ab_channel=Mijin (Note: Ignore the instruction to click 'OK' on popup message in the video)
- Mod Configuration Video: https://youtu.be/20ojprrxrQM?si=GHUbW2dLyVxUAEC6&t=226 (Note: Load order importance is not mentioned in the video)

Support:

For any questions or support, feel free to contact me on Discord: https://discord.gg/Kws8AyYPeE
