#!/bin/bash

# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
Red='\033[0;31m'
BoldRed='\033[1;31m'
Green='\033[0;32m'
Yellow='\033[0;33m'
Reset='\033[0m'

echo -e "${BoldRed}[Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University]${Reset}"
echo -e "${BoldRed}[Building N.P.A. on Linux]${Reset}"

# Step 00. Checking Environment
echo -e "${BoldRed}[Step 00. Checking Environment...]${Reset}"

if ! command -v python3 &> /dev/null; then
    echo -e "${BoldRed}[ERROR] Python3 is not installed or not added to PATH.${Reset}"
    read -p "Press enter to exit..."
    exit 1
fi

PY_IDENTITY=$(python3 -c "import sys; print('CPython' if (sys.implementation.name == 'cpython' and 'conda' not in sys.version.lower() and 'continuum' not in sys.version.lower()) else 'NON_OFFICIAL')" 2>/dev/null)

if [ "$PY_IDENTITY" != "CPython" ]; then
    echo -e "${BoldRed}[ERROR] Non-official Python distribution detected. Please install official Python.${Reset}"
    read -p "Press enter to exit..."
    exit 1
fi
echo -e "${Green}Environment Checked.${Reset}"

# Step 01. Unzip libs.zip
echo -e "${BoldRed}[Step 01. Unzip libs.zip]${Reset}"
if ! command -v unzip &> /dev/null; then
    echo -e "${BoldRed}[ERROR] 'unzip' command not found. Please install it (e.g., sudo apt install unzip).${Reset}"
    read -p "Press enter to exit..."
    exit 1
fi
unzip -o "./libs.zip" -d "./static/js" > /dev/null

# Step 02. Creating Virtual Environment
echo -e "${BoldRed}[Step 02. Creating Virtual Environment...]${Reset}"
if [ -d "npa" ]; then
    rm -rf npa
fi
python3 -m venv npa

# Step 03. Activating Virtual Environment
echo -e "${BoldRed}[Step 03. Activating Virtual Environment...]${Reset}"
source ./npa/bin/activate

# Step 04. Installing Dependencies
echo -e "${BoldRed}[Step 04. Installing Dependencies...]${Reset}"
pip install -r requirements.txt

# Step 05. Building
echo -e "${BoldRed}[Step 05. Building...]${Reset}"
python3 -m nuitka --onefile --standalone \
--output-filename=npa_v1.0.0_linux_x86-64 \
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
main.py

# Step 06. Build Completed and Clear Virtual Environment
echo -e "${BoldRed}[Step 06. Build Completed and Clear Virtual Environment...]${Reset}"
deactivate
rm -rf ./npa

# Step 07. All Completed
echo -e "${BoldRed}[Step 07. All Completed]${Reset}"
read -p "Press enter to continue..."