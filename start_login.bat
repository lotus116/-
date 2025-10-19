@echo off

REM === AutoLogin Start Script (v13 - START /B Fix) ===
REM We are using the "python.exe script.py" method, which you
REM proved is working (from your 14:24:27 log).

REM Change directory to the script's location
cd /d %~dp0

REM Write a startup message to the log
echo [%date% %time%] BAT: Launching script... >> login_log.txt

REM 
REM --- THE FINAL COMMAND ---
REM START /B : Launch python.exe in the BACKGROUND (no new window)
REM This fixes the "CMD window stays open" problem.
REM

START "AutoLogin" /B "C:\Users\cclear116\AppData\Local\Programs\Python\Python310\python.exe" -u "C:\xyw_auto_login\auto_login.py" >> login_log.txt 2>>&1

REM This line will now be reached immediately
echo [%date% %time%] BAT: Launch command sent. .bat file exiting. >> login_log.txt