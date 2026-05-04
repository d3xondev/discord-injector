#!/usr/bin/env bash
# Cross-compile discord.py from Linux to Windows EXE
# Requires: wine, python in wine, pyinstaller in wine

set -e

DISCORD_PY="discord.py"
WINE_DRIVE="$HOME/.wine/drive_c"
WINE_PYTHON="$WINE_DRIVE/Python311/python.exe"

echo "[*] Discord Token Injector - Linux to Windows Cross-Compile"
echo ""

# Check if wine is installed
if ! command -v wine &> /dev/null; then
    echo "[-] Wine not installed. Install with:"
    echo "    sudo apt-get install wine wine32 wine64"
    exit 1
fi

# Check if Python is in wine
if [ ! -f "$WINE_PYTHON" ]; then
    echo "[-] Python not found in Wine at: $WINE_PYTHON"
    echo "[*] Setup instructions:"
    echo "    1. Download Python Windows installer: https://www.python.org/downloads/"
    echo "    2. Run in wine: wine python-3.11.x.exe"
    echo "    3. Install PyInstaller: wine pip install pyinstaller"
    exit 1
fi

# Check if PyInstaller is installed in wine
if ! wine pip show pyinstaller &> /dev/null; then
    echo "[*] Installing PyInstaller in Wine..."
    wine pip install pyinstaller
fi

echo "[*] Building Windows EXE in Wine..."
wine python "$DISCORD_PY" --build || wine python -m PyInstaller --onefile --console --name DiscordInjector "$DISCORD_PY"

if [ -f "dist/DiscordInjector.exe" ]; then
    size=$(du -h dist/DiscordInjector.exe | cut -f1)
    echo "[+] SUCCESS: dist/DiscordInjector.exe ($size)"
else
    echo "[-] Build failed - EXE not found"
    exit 1
fi
