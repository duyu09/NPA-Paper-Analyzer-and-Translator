# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import webview
import threading
import json
import os
from split_text import split_text_by_token_limit
from call_api import TranslationService
from flask_server import app, set_current_doc_dir
from tempdir_manager import create_tempdir, get_current_tempdir
from analysis_pdf import parse_pdf_mineru
from key_manager import get_api_key, set_api_key, key_manager_init
from close_splash import close_splash_screen

key_manager_init('npa_api_config.ini')

class JsonStreamParser:
    """
    简易的状态机，用于从 JSON 流中提取 "translation" 字段的内容。假设keys的顺序不确定，但通常translation内容较长。
    为了简化，假设流式输出是标准的JSON格式。
    1. 找到 "translation" key
    2. 进入 value (string)
    3. 提取 string 内容并处理转义字符
       
    目前策略：
    后端积累 buffer，寻找 "translation": " ... " 模式
    """
    def __init__(self):
        self.buffer = ""
        self.in_translation = False
        self.translation_finished = False
        self.escape_next = False
        # 指向内容开始的第一个字符
        self.process_idx = 0 
        
    def process_chunk(self, chunk):
        """
        接收 chunk，返回提取到的翻译文本 (unescaped)
        同时维护 buffer 用于最终的 json.loads
        """
        self.buffer += chunk
        
        # 如果还没找到 translation 字段，且还没完成翻译
        if not self.in_translation and not self.translation_finished:
            # 尝试寻找 "translation": "
            pattern = '"translation":'
            idx = self.buffer.find(pattern)
            if idx != -1:
                # 找到了 key，寻找值开始的引号
                # 从 key 后面找第一个 "
                quote_idx = self.buffer.find('"', idx + len(pattern))
                if quote_idx != -1:
                    self.in_translation = True
                    # 截断 buffer，只保留 content 部分用于后续处理
                    # 为了不破坏 buffer (需要完整 json)，我们维护一个 process_idx
                    self.process_idx = quote_idx + 1 # 指向内容开始的第一个字符
                    # 处理当前 buffer 中剩余的部分
                    return self._extract_content_from_buffer()
        elif self.in_translation:
            return self._extract_content_from_buffer()
            
        return ""

    def _extract_content_from_buffer(self):
        """
        从 self.process_idx 开始提取内容，直到遇到非转义的 "
        """
        result = []
        # 遍历 buffer 中未处理的部分
        while self.process_idx < len(self.buffer):
            char = self.buffer[self.process_idx]
            
            if self.escape_next:
                # 无论是啥，都作为普通字符（转义后的）
                # JSON 转义: \" -> ", \\ -> \, \n -> newline
                # 简单映射
                if char == 'n': result.append('\n')
                elif char == 't': result.append('\t')
                elif char == '"': result.append('"')
                elif char == '\\': result.append('\\')
                else: result.append(char)
                
                self.escape_next = False
            else:
                if char == '\\':
                    self.escape_next = True
                elif char == '"':
                    # 结束引号
                    self.in_translation = False # 结束
                    self.translation_finished = True

                    # 函数目标是 output translation streaming。
                    # JSON 结束了，不再输出 text。
                    self.process_idx += 1
                    return "".join(result)
                else:
                    result.append(char)
            
            self.process_idx += 1
            
        return "".join(result)

    def get_full_json(self):
        try:
            # 尝试修复截断的 JSON (如果有) -> 依赖流结束
            start = self.buffer.find('{')
            err_end = self.buffer.rfind('}')
            if start != -1 and err_end != -1:
                return json.loads(self.buffer[start:err_end+1])
            return json.loads(self.buffer)
        except:
            return None

class Api:
    def __init__(self):
        self.service = None
        self.should_stop = False
        self._window = None

    def set_window(self, window):
        self._window = window

    # --- 被 JS 调用的方法 ---
    def get_api_key_frontend(self, key_name):
        return get_api_key(key_name)

    def open_file(self, mineru_api_key=None):
        """打开文件对话框"""
        file_types = ('受支持的文件 (*.md;*.pdf)', 'All files (*.*)')
        result = self._window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if result:
            try:
                if result[0].endswith('.pdf'):
                    if mineru_api_key is None or mineru_api_key == "":
                        self._window.evaluate_js('alert("解析PDF文件需要MinerU API Key")')
                        return None
                    # result[0] 是真正的文件路径字符串
                    pdf_path = result[0]
                    temp_dir = create_tempdir()
                    parse_pdf_mineru(mineru_api_key, pdf_path, temp_dir)
                    set_current_doc_dir(temp_dir)
                    with open(temp_dir + "/full.md", 'r', encoding='utf-8') as f:
                        set_api_key('mineru-api-key', mineru_api_key)  # 解析成功即自动保存
                        return f.read()
                else:  # md
                    doc_dir = os.path.dirname(result[0])
                    set_current_doc_dir(doc_dir)
                    with open(result[0], 'r', encoding='utf-8') as f:
                        return f.read()
            except Exception as e:
                self._window.evaluate_js(f'alert("读取失败: {str(e)}")')
        return None

    def save_file(self, content):
        """保存文件对话框"""
        file_types = ('Markdown Files (*.md)', 'All files (*.*)')
        result = self._window.create_file_dialog(webview.SAVE_DIALOG, save_filename="translation.md", file_types=file_types)

        if result:
            try:
                # pywebview 的 save_dialog 返回的也是元组/列表，即使只保存一个文件
                filename = result[0] if isinstance(result, (tuple, list)) else result
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                return "保存成功！"
            except Exception as e:
                return f"保存失败: {str(e)}"
        return "取消保存"

    def start_translation(self, api_key, content, model, src, tgt):
        """启动翻译线程"""
        self.should_stop = False
        self.service = TranslationService(api_key)
        set_api_key('zhipu-api-key', api_key)  # 自动保存api key
        
        # 1. 切分文本
        chunks = split_text_by_token_limit(content, 18000)
        
        def run():
            global_term_table = {}
            
            try:
                for i, chunk_text in enumerate(chunks):
                    if self.should_stop:
                        break
                        
                    # 准备解析器
                    parser = JsonStreamParser()
                    
                    # 更新 UI 提示当前进度
                    # self._window.evaluate_js(f'onChunkReceived("\\n\\n--- Part {i+1}/{len(chunks)} ---\\n\\n")')
                    # 调用 API
                    generator = self.service.stream_translation(chunk_text, model, src, tgt, global_term_table)
                    for chunk_part in generator:
                        if self.should_stop:
                            break
                        
                        # A. 累积并解析流
                        text_delta = parser.process_chunk(chunk_part)
                        
                        # B. 如果有提取出的文本，发送给 UI
                        if text_delta:
                            # 使用 json.dumps 安全转义字符串，传给前端
                            safe_chunk = json.dumps(text_delta)
                            self._window.evaluate_js(f'onChunkReceived({safe_chunk})')
                    
                    # C. 本块结束，解析完整 JSON 以更新术语表
                    final_json = parser.get_full_json()
                    if final_json:
                        if "term_table" in final_json and isinstance(final_json["term_table"], dict):
                            global_term_table.update(final_json["term_table"])
                            print(f"Chunk {i+1} Term Table Update: {len(final_json['term_table'])} items")
                    else:
                        print(f"Chunk {i+1} JSON Parse Failed")
                
                # 正常结束或手动停止，都调用 Finished 回调
                self._window.evaluate_js('onTranslationFinished()')
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                safe_err = json.dumps(str(e))
                self._window.evaluate_js(f'onTranslationError({safe_err})')

        threading.Thread(target=run, daemon=True).start()

    def stop_translation(self):
        """设置停止标志位"""
        self.should_stop = True

if __name__ == '__main__':
    PYFILE_BASEURL = os.path.dirname(os.path.abspath(__file__))
    api = Api()
    
    # 创建窗口
    window = webview.create_window(
        '“核动力”——PDF及Markdown论文解析&翻译器  (@duyu09 - 11250717@stu.lzjtu.edu.cn)', 
        app,
        js_api=api,
        width=1275,
        height=850,
        min_size=(900, 600),
        text_select=True,
        easy_drag=False
    )
    
    api.set_window(window)
    close_splash_screen()  # 关闭splash screen
    # 启动
    webview.start(debug=False)
    