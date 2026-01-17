# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import configparser
import os

# --- 配置常量 ---
_SECTION_NAME = 'Credentials'
_VALID_KEYS = {'zhipu-api-key', 'mineru-api-key'}

# --- 全局状态 ---
# 默认为 None，表示模块尚未初始化
_config_file_path = None

def key_manager_init(ini_path: str):
    """
    初始化模块：设置 INI 文件路径。
    
    逻辑：
    1. 设置全局路径变量。
    2. 检查该路径的文件是否存在。
    3. 若不存在，创建新文件并写入默认的空键值结构。
    4. 若存在，检查是否包含必要的 Section，若缺失则补全。
    """
    global _config_file_path
    _config_file_path = ini_path
    
    # 确保目录结构存在（如路径是 configs/key.ini，需先创建 configs 目录）
    directory = os.path.dirname(_config_file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # 如果文件不存在，直接创建
    if not os.path.exists(_config_file_path):
        _create_default_config()
        return

    # 如果文件存在，校验内容结构的完整性
    config = configparser.ConfigParser()
    try:
        config.read(_config_file_path, encoding='utf-8')
        if not config.has_section(_SECTION_NAME):
            # 文件存在但格式不对（没有指定的Section），尝试修复或追加
            # 注意：这里选择追加而不是覆盖，以防用户有其他配置
            config.add_section(_SECTION_NAME)
            for key in _VALID_KEYS:
                config.set(_SECTION_NAME, key, '')
            with open(_config_file_path, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
    except configparser.Error:
        # 文件损坏无法解析，重建默认文件
        _create_default_config()

def _create_default_config():
    """内部函数：创建并写入默认的空配置结构"""
    if _config_file_path is None:
        return

    config = configparser.ConfigParser()
    config[_SECTION_NAME] = {key: '' for key in _VALID_KEYS}
    
    with open(_config_file_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def _check_initialized():
    """内部函数：确保模块已初始化"""
    if _config_file_path is None:
        raise RuntimeError("KeyManager not initialized. Please call 'key_manager_init(path)' first.")

def _validate_key_name(key_name: str):
    """内部函数：验证 API Key 名称是否合法"""
    if key_name not in _VALID_KEYS:
        raise ValueError(f"Invalid API key name: '{key_name}'. "
                         f"Allowed values are: {', '.join(_VALID_KEYS)}")

def get_api_key(key_name: str) -> str:
    """
    读取指定的 API Key。
    
    Args:
        key_name: 'zhipu-api-key' 或 'mineru-api-key'
    """
    _check_initialized()     # 检查是否已初始化
    _validate_key_name(key_name)
    
    config = configparser.ConfigParser()
    # 此时文件一定存在，因为 init 阶段已经保证了
    config.read(_config_file_path, encoding='utf-8')
    
    return config.get(_SECTION_NAME, key_name, fallback='')

def set_api_key(key_name: str, new_value: str):
    """
    设置指定的 API Key 值。
    
    Args:
        key_name: 'zhipu-api-key' 或 'mineru-api-key'
        new_value: 新的 API Key 字符串
    """
    _check_initialized()     # 检查是否已初始化
    _validate_key_name(key_name)
    
    config = configparser.ConfigParser()
    config.read(_config_file_path, encoding='utf-8')
    
    # 双重保险：虽然 init 保证了 section 存在，但防止运行期间文件被外部修改
    if not config.has_section(_SECTION_NAME):
        config.add_section(_SECTION_NAME)
        
    config.set(_SECTION_NAME, key_name, new_value)
    
    with open(_config_file_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)