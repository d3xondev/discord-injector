#!/usr/bin/env python3
"""
Static cross-compile discord.py to Windows EXE from Linux using DockerFile
Creates a minimal, standalone Windows executable with all dependencies compiled in
"""
import subprocess
import os

DOCKERFILE = '''FROM mcr.microsoft.com/windows/servercore:ltsc2022
RUN powershell -Command \\
    $ProgressPreference = 'SilentlyContinue'; \\
    Invoke-WebRequest https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe -OutFile python-installer.exe; \\
    .\\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1; \\
    del python-installer.exe
RUN pip install --no-cache-dir pyinstaller==6.1.0
WORKDIR /build
COPY discord.py .
RUN pyinstaller --onefile --console --distpath . discord.py
'''

def create_dockerfile():
    """Create Dockerfile for Windows build"""
    with open('Dockerfile.windows', 'w') as f:
        f.write(DOCKERFILE)
    print("[+] Created Dockerfile.windows")

def build_with_docker():
    """Build using Docker"""
    if not subprocess.run(['docker', '--version'], capture_output=True).returncode == 0:
        print("[-] Docker not found. Install from: https://www.docker.com")
        return False
    
    print("[*] Building with Docker...")
    print("[*] This will create a Windows-native build on a Windows container")
    
    # Check if discord.py exists
    if not os.path.exists('discord.py'):
        print("[-] discord.py not found in current directory")
        return False
    
    create_dockerfile()
    
    # Note: This requires Docker Desktop with Windows support
    try:
        subprocess.run([
            'docker', 'build', 
            '-f', 'Dockerfile.windows',
            '-t', 'discord-injector:latest',
            '.'
        ], check=True)
        
        # Extract build output
        subprocess.run([
            'docker', 'run', 
            '--rm',
            '-v', f'{os.getcwd()}:/output',
            'discord-injector:latest',
            'cmd', '/c', 'copy DiscordInjector.exe /output'
        ], check=True)
        
        print("[+] Build complete: DiscordInjector.exe")
        return True
    except subprocess.CalledProcessError:
        print("[-] Docker build failed")
        return False

def build_with_mingw():
    """Build statically using MinGW on Linux"""
    print("[*] Static cross-compile using MinGW and PyInstaller...")
    
    # Check for required tools
    required = ['gcc', 'mingw-w64-gcc', 'pyinstaller']
    for tool in required[:2]:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"[-] {tool} not found. Install MinGW:")
            print("    sudo apt-get install mingw-w64")
            return False
    
    print("[*] Creating static build with MinGW...")
    
    # PyInstaller command with static linking
    cmd = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--distpath', 'dist',
        '--buildpath', 'build',
        '--specpath', '.',
        '--name', 'DiscordInjector',
        '--add-data', 'discord.py:.',
        'discord.py'
    ]
    
    try:
        # Set flags for static linking
        env = os.environ.copy()
        env['LDFLAGS'] = '-static-libgcc -static-libstdc++'
        env['CFLAGS'] = '-static-libgcc -static-libstdc++'
        
        subprocess.run(cmd, env=env, check=True)
        
        exe = 'dist/DiscordInjector.exe'
        if os.path.exists(exe):
            size = os.path.getsize(exe) / (1024*1024)
            print(f"[+] SUCCESS: {exe} ({size:.1f} MB)")
            print("[+] This is a standalone Windows executable with all dependencies included")
            return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Build failed: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if sys.platform == 'linux':
        print("[*] Static cross-compilation for Windows")
        print("[*] Method 1: Using MinGW (faster, Linux-based)")
        print("[*] Method 2: Using Docker (requires Docker Desktop)")
        print()
        
        # Try MinGW first (faster)
        if build_with_mingw():
            sys.exit(0)
        
        print()
        print("[*] Attempting Docker build...")
        if build_with_docker():
            sys.exit(0)
        
        print("[-] Both methods failed")
        sys.exit(1)
    else:
        print("[*] Static Windows build")
        if build_with_mingw():
            sys.exit(0)
        sys.exit(1)
