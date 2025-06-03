import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    os.path.join('src', 'main.py'),
    '--clean',
    '--noconfirm',
    '--onedir',
    '--noupx',
    '--windowed',
    '--name=ScreenTune',
    '--icon=src/assets/icon.png',
    '--add-data=../frontend/dist/screen-tune/browser:frontend',
    '--add-data=src/assets:assets',
    '--add-data=pyproject.toml:.',
    '--log-level=WARN'
])