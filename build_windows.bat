REM Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
@echo off
setlocal
setlocal enabledelayedexpansion
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "Red=%ESC%[31m"
set "BoldRed=%ESC%[1;31m"
set "Green=%ESC%[32m"
set "Yellow=%ESC%[33m"
set "Reset=%ESC%[0m"

echo %BoldRed%[Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University]%Reset%
echo %BoldRed%[Building N.P.A. on Windows]%Reset%

echo %BoldRed%[Step 00. Checking Environment...]%Reset%
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %BoldRed%[ERROR] Python is not installed or not added to PATH.%Reset%
    pause
    exit /b 1
)
for /f "delims=" %%i in ('python -c "import sys; print('CPython' if (sys.implementation.name == 'cpython' and 'conda' not in sys.version.lower() and 'continuum' not in sys.version.lower()) else 'NON_OFFICIAL')" 2^>nul') do (
    set "PY_IDENTITY=%%i"
)
if /i "!PY_IDENTITY!" NEQ "CPython" (
    echo %BoldRed%[ERROR] Non-official Python distribution detected. Please download Python from python.org%Reset%
    pause
    exit /b 1
)
%Green%Environment Checked.%Reset%

echo %BoldRed%[Step 01. Unzip libs.zip]%Reset%
where /q tar.exe
if %ERRORLEVEL% NEQ 0 (
    echo %BoldRed%[ERROR] 'tar' command not found. Your Windows version might be older than Win10 1803. Please manually extract .\static\js\libs.zip to .\static\js, comment out "Step 01" in the script, and then re-run the script.%Reset%
    pause
    exit /b 1
)
tar -xf ".\libs.zip" -C ".\static\js"

echo %BoldRed%[Step 02. Creating Virtual Environment...]%Reset%
python -m venv npa

echo %BoldRed%[Step 03. Activating Virtual Environment...]%Reset%
call .\npa\Scripts\activate

echo %BoldRed%[Step 04. Installing Dependencies...]%Reset%
pip install -r requirements.txt

echo %BoldRed%[Step 05. Building...]%Reset%
python -m nuitka --onefile --standalone ^
--windows-icon-from-ico=.\npa-icon.ico ^
--output-filename=npa_v1.0.0_windows_x86-64.exe ^
--include-data-dir=.\static=static ^
--show-progress ^
--remove-output ^
--lto=yes ^
--assume-yes-for-downloads ^
--windows-console-mode=disable ^
--company-name="DuYu, Lanzhou Jiaotong University" ^
--product-name="N.P.A.-'Nuclear-Powered-Level' Paper Analyzer & Translator" ^
--file-version=1.0.0.0 ^
--product-version=1.0.0.0 ^
--file-description="N.P.A.-'Nuclear-Powered-Level' Paper Analyzer & Translator" ^
--copyright="Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University" ^
--onefile-windows-splash-screen-image=.\splash-screen-v1.0-small.png ^
main.py

echo %BoldRed%[Step 06. Build Completed and Clear Virtual Environment...]%Reset%
call deactivate
rd /s /q .\npa

echo %BoldRed%[Step 07. All Completed]%Reset%
pause