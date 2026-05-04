@echo off
REM ====================================
REM Discord Token Injector - Windows Build
REM Run this on Windows with Python 3.9+
REM ====================================

REM Install dependencies
echo [*] Installing build dependencies...
pip install pyinstaller --quiet
if errorlevel 1 goto :error

REM Run PyInstaller
echo [*] Building executable...
pyinstaller ^
  --onefile ^
  --console ^
  --name DiscordInjector ^
  --distpath dist ^
  --workpath build ^
  --specpath . ^
  discord.py

if errorlevel 1 goto :error

REM Check if build succeeded
if exist "dist\DiscordInjector.exe" (
  for /f "tokens=*" %%A in ('dir /b "dist\DiscordInjector.exe"') do (
    echo.
    echo [+] BUILD SUCCESSFUL!
    echo [+] Output: dist\DiscordInjector.exe
    echo.
  )
  exit /b 0
) else (
  goto :error
)

:error
echo.
echo [-] Build failed - check output above
exit /b 1
