@echo off
REM Quick batch script to create admin user
REM Double-click this file to run

echo.
echo ============================================================
echo   Gaming Platform - Create Admin User (Windows)
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Run the admin creation script
python create_admin.py

echo.
echo ============================================================
echo   Done! Press any key to exit...
echo ============================================================
pause
