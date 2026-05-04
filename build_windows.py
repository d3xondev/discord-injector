#!/usr/bin/env python3
"""
Build Windows EXE from discord.py
Run on Windows with: python build_windows.py
"""
import subprocess
import sys
import os
import shutil

def build_exe():
    print("[*] Building Windows executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable
        '--console',                    # Console mode
        '--name', 'DiscordInjector',
        '--add-data', 'discord.py:.',  # Include source
        'discord.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        exe_path = os.path.join('dist', 'DiscordInjector.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024*1024)
            print(f"[+] SUCCESS: {exe_path} ({size_mb:.1f} MB)")
            return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Build failed: {e}")
        return False
    except FileNotFoundError:
        print("[-] PyInstaller not found. Install: pip install pyinstaller")
        return False

if __name__ == '__main__':
    success = build_exe()
    sys.exit(0 if success else 1)
