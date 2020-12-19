# -*- mode: python ; coding: utf-8 -*-

a = Analysis(['main.py'],
             pathex=['C:\\Users\\z\\dev\\Progress-Sheet-Updater'],
             datas=[('C:\\Users\\z\\AppData\\Roaming\\Python\\Python39\\site-packages\\google_api_python_client-1.12.8.dist-info\\*', 'google_api_python_client-1.12.8.dist-info')]
)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SheetUpdater.exe',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='icon.ico')
