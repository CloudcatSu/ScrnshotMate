# -*- mode: python ; coding: utf-8 -*-

import re

# 版號單一來源：跟著 utils/helpers.py 的 APP_VERSION 走
APP_VERSION = re.search(
    r'APP_VERSION\s*=\s*"([^"]+)"', open('utils/helpers.py').read()
).group(1)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScrnshotMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScrnshotMate',
)
app = BUNDLE(
    coll,
    name='ScrnshotMate.app',
    icon='assets/ScrnshotMate_icon.icns',
    bundle_identifier='com.firewatersmithy.scrnshotmate',
    version=APP_VERSION,
    info_plist={
        'CFBundleShortVersionString': APP_VERSION,
        'CFBundleVersion': APP_VERSION,
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
)
