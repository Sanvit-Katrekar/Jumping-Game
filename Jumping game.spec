# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Jumping game.py'],
             pathex=['C:\\Users\\katre\\Desktop\\Python Projects\\Game Jump'],
             binaries=[],
             datas=[('Images/*.png', '.'), ('Images/bg.jpg', '.'), ('Images/Player 1/*.png', '.'), ('Images/Player 2/*.png', '.'), ('Text Files/controls.txt', '.'), ('Music/*.mp3', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Jumping game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='gamejumpIcon.ico')
