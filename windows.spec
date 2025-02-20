# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./config.yaml', './'),
        ('./src/css/_fundamental.css', './src/css/'),
        ('./src/css/syntax.css', './src/css/'), 
        ('./src/css/github.css', './src/css/'), 
        ('./src/css/gothic.css', './src/css/'), 
        ('./src/css/newsprint.css', './src/css/'), 
        ('./src/css/night.css', './src/css/'), 
        ('./src/css/pixyll.css', './src/css/'), 
        ('./src/css/whitey.css', './src/css/'), 
    ],
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
    name='Jupyrender.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./src/icon/icon_256.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Jupyrender',
)
