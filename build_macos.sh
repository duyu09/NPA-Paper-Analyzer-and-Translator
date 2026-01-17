#!/bin/bash

# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
RED='\033[0;31m'
BOLD_RED='\033[1;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

echo -e "${BOLD_RED}[Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University]${RESET}"
echo -e "${BOLD_RED}[Building N.P.A. on macOS]${RESET}"

# Step 00. Checking Environment...
echo -e "${BOLD_RED}[Step 00. Checking Environment...]${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${BOLD_RED}[ERROR] Python3 is not installed or not added to PATH.${RESET}"
    exit 1
fi
PY_IDENTITY=$(python3 -c "import sys; print('CPython' if (sys.implementation.name == 'cpython' and 'conda' not in sys.version.lower() and 'continuum' not in sys.version.lower()) else 'NON_OFFICIAL')")

if [ "$PY_IDENTITY" != "CPython" ]; then
    echo -e "${BOLD_RED}[ERROR] Non-official Python distribution detected. Please download Python from python.org${RESET}"
    exit 1
fi
echo -e "${GREEN}Environment Checked.${RESET}"

# Step 01. Unzip libs.zip
echo -e "${BOLD_RED}[Step 01. Unzip libs.zip]${RESET}"
if ! command -v tar &> /dev/null; then
    echo -e "${BOLD_RED}[ERROR] 'tar' command not found.${RESET}"
    exit 1
fi
tar -xf "./libs.zip" -C "./static/js"

# Step 02. Creating Virtual Environment...
echo -e "${BOLD_RED}[Step 02. Creating Virtual Environment...]${RESET}"
python3 -m venv npa

# Step 03. Activating Virtual Environment...
echo -e "${BOLD_RED}[Step 03. Activating Virtual Environment...]${RESET}"
source ./npa/bin/activate

# Step 04. Installing Dependencies...
echo -e "${BOLD_RED}[Step 04. Installing Dependencies...]${RESET}"
pip install -r requirements.txt

# Step 05. Building...
echo -e "${BOLD_RED}[Step 05. Building...]${RESET}"
python3 -m nuitka --standalone --macos-create-app-bundle \
--macos-app-icon=./npa-icon.icns \
--output-filename=NPA \
--include-data-dir=./static=static \
--show-progress \
--remove-output \
--lto=yes \
--assume-yes-for-downloads \
--company-name="DuYu, Lanzhou Jiaotong University" \
--product-name="N.P.A.-'Nuclear-Powered-Level' Paper Analyzer & Translator" \
--file-version=1.0.0.0 \
--product-version=1.0.0.0 \
--file-description="N.P.A.-'Nuclear-Powered-Level' Paper Analyzer & Translator" \
--copyright="Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University" \
--macos-app-name="NPA" \
--macos-app-version=1.0.0.0 \
--macos-app-mode=gui \
main.py

echo -e "${BOLD_RED}[Step 06. Build Completed and Clear Virtual Environment...]${RESET}"
deactivate
rm -rf ./npa

echo -e "${BOLD_RED}[Step 07. All Completed]${RESET}"