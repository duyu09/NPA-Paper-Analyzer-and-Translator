# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import tempfile

_current_temp_obj = None

def create_tempdir():
    """
    创建新的临时目录。
    如果之前已存在临时目录，则会自动触发旧目录的销毁。
    Returns:
        str: 新创建的临时目录绝对路径
    """
    global _current_temp_obj

    _current_temp_obj = tempfile.TemporaryDirectory()
    
    # 返回绝对路径
    return _current_temp_obj.name

def get_current_tempdir():
    """
    获取当前已创建的临时目录路径。
    Returns:
        str or None: 当前目录路径，如果尚未创建则返回 None
    """
    if _current_temp_obj:
        return _current_temp_obj.name
    return None