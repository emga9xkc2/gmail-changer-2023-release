
@taskkill /IM "chromedriver.exe" /F
@rmdir /s /q "%appdata%\myscript"
@rmdir /s /q "%appdata%\nightowl\myscript"
@rmdir /s /q "%temp%\gen_py"
powershell.exe -executionpolicy ByPass -File python.ps1
@py ../main.py
@timeout /t 100