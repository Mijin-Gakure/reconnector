@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check if Python 3.11.6 is installed
FOR /F "tokens=*" %%i IN ('python --version 2^>^&1') DO SET pyver=%%i
SET correctVersion=Python 3.11.6

IF NOT "!pyver!"=="%correctVersion%" (
    echo The required Python version is not installed.
    echo Please download and install Python 3.11.6 from the official website.
    start https://www.python.org/downloads/release/python-3116/
    goto :end
)

echo Found %correctVersion%.

:: Install required Python modules
echo Installing required Python modules...
python -m pip install --upgrade pip
python -m pip install pyautogui
python -m pip install Pillow

:: No additional module installations are required for the script

echo Installation complete.

:end
pause
ENDLOCAL
