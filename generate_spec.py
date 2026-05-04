#!/usr/bin/env python3
"""
Generate PyInstaller spec for cross-platform building
This creates a .spec file that can be used on Windows or in wine/docker
"""
import os

SPEC_CONTENT = '''# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['discord.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['os', 'subprocess', 'time', 'pathlib', 'glob'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DiscordInjector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''

if __name__ == '__main__':
    with open('discord.spec', 'w') as f:
        f.write(SPEC_CONTENT)
    print("[+] Created discord.spec - use with PyInstaller on Windows:")
    print("    pyinstaller discord.spec")
