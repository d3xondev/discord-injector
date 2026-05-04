#!/usr/bin/env python3
"""
Static executable builder for Windows
Creates a minimal, self-contained Windows EXE with all dependencies bundled

Usage:
  Windows:  python build_static.py
  Linux:    Requires: wine + Python + pyinstaller in wine OR native Windows build
  
This script:
  1. Verifies Python/PyInstaller is installed
  2. Bundles all dependencies into single EXE (-onefile flag)
  3. Creates minimal, portable executable (~9-15 MB)
  4. No external dependencies required on target system
"""
import subprocess
import sys
import os
import shutil

def check_pyinstaller():
    """Verify PyInstaller is installed"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', 'pyinstaller'],
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("[*] Installing PyInstaller...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'pyinstaller', '--quiet'],
            check=True
        )
        print("[+] PyInstaller installed")
        return True
    except subprocess.CalledProcessError:
        print("[-] Failed to install PyInstaller")
        print("[*] Try: python -m pip install pyinstaller")
        return False

def build_exe():
    """Build Windows executable"""
    if not os.path.exists('discord.py'):
        print("[-] discord.py not found in current directory")
        return False
    
    print("[*] Building static Windows executable...")
    print("[*] This bundles all dependencies into single EXE file")
    print()
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable
        '--console',                    # Console window
        '--name', 'DiscordInjector',   # Output name
        '--distpath', './dist',         # Output directory
        '--workpath', './build',        # Build directory
        '--specpath', '.',              # Spec file location
        '--noupx',                      # Skip UPX compression
        'discord.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        
        # Check for Windows EXE
        if sys.platform == 'win32':
            exe = 'dist\\DiscordInjector.exe'
        else:
            exe = './dist/DiscordInjector'
        
        if os.path.exists(exe):
            size_mb = os.path.getsize(exe) / (1024*1024)
            print()
            if sys.platform == 'win32':
                print(f"[+] SUCCESS: {exe} ({size_mb:.1f} MB)")
                print("[+] Windows executable ready for deployment")
            else:
                print(f"[+] Linux binary created: {exe} ({size_mb:.1f} MB)")
                print("[-] For Windows EXE, build on Windows system")
            return True
        else:
            print("[-] Build output not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[-] Build failed: {e}")
        return False

def main():
    print("="*50)
    print("Discord Token Injector - Static Build")
    print("="*50)
    print()
    
    # Check platform
    if sys.platform not in ['win32', 'linux']:
        print(f"[-] Unsupported platform: {sys.platform}")
        print("[*] Supported: Windows, Linux")
        return 1
    
    if sys.platform == 'win32':
        print("[*] Building on Windows (native)")
    else:
        print("[*] Building on Linux (cross-compile/wine required)")
    
    print()
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return 1
    else:
        print("[+] PyInstaller already installed")
    
    print()
    
    # Build executable
    if build_exe():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
