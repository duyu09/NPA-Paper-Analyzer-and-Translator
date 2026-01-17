# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import os
from flask import Flask, send_from_directory

_current_doc_dir = ""
PYFILE_BASEURL = os.path.dirname(os.path.abspath(__file__))  # 应对打包后的Python脚本

app = Flask(__name__)

def set_current_doc_dir(doc_dir):
    global _current_doc_dir
    _current_doc_dir = doc_dir

@app.route('/images/<path:filename>')
def serve_images(filename):
    """
    这个函数会被 Webview 中的图片请求触发。
    例如：HTML 中有 <img src="/images/001.jpg">
    Flask 就会收到 filename="001.jpg"
    """
    global _current_doc_dir
    img_dir = os.path.join(_current_doc_dir, "images")
    return send_from_directory(img_dir, filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    full_abs_path = os.path.abspath(os.path.join(PYFILE_BASEURL, "static/js", filename))
    dir_name, file_name = os.path.split(full_abs_path)
    return send_from_directory(dir_name, file_name)

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(PYFILE_BASEURL, "static"), "index.html")

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(os.path.join(PYFILE_BASEURL, "static"), "npa-icon.png")
