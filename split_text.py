# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import re

def split_text_by_token_limit(text, token_limit, buffer_ratio=0.95):
    """
    文本切分：
    1. 还原性：合并后与原文 100% 一致（包括空格、换行）。
    2. 公式保护：LaTeX 公式不会被从中间切断。
    3. 代码处理：代码块允许被切分（主要依靠换行符），适应长文本。
    """
    
    # --- 1. 预处理：保护 LaTeX 公式 (Masking) ---
    # 策略：找到所有 LaTeX 公式，替换为唯一的占位符，这样后续的标点切分逻辑就会把整个公式视为一个“单词”
    # 匹配规则：
    # 1. $$...$$ (块级公式，允许换行)
    # 2. $...$ (行内公式，非贪婪，通常不跨行)
    # 这里使用了非贪婪匹配 .*?
    latex_pattern = r'(\$\$[\s\S]*?\$\$|\$[^\n\$]*?\$)'
    
    placeholders = []
    
    def mask_match(match):
        # 将原始内容存入列表
        content = match.group(0)
        placeholders.append(content)
        # 返回占位符，格式设计为不含任何标点，避免被误切
        return f"__MASK_LATEX_{len(placeholders)-1}__"
    
    # 执行替换保护。protected_text 是“脱敏”后的文本，公式变成了 __MASK_LATEX_0__ 等
    protected_text = re.sub(latex_pattern, mask_match, text)
    
    
    # --- 2. 核心切分逻辑 (基于脱敏文本) ---
    
    # 定义切分符正则：
    # 包含：句号、问号、感叹号、分号 (代码常用)、换行符
    # 关键：保留了 \n，这对代码块切分至关重要
    split_pattern = r'([。！？.?!;\n]+)'
    
    # 初步拆分 (使用捕获组 () 确保标点保留在列表中)
    raw_segments = re.split(split_pattern, protected_text)
    
    # --- 3. 重新组合为“原子句子” ---
    sentences = []
    current_sent = ""
    
    for seg in raw_segments:
        if not seg:
            continue
            
        current_sent += seg
        
        # 如果当前片段是分隔符，则认为句子结束
        if re.match(split_pattern, seg):
            sentences.append(current_sent)
            current_sent = ""
            
    # 处理末尾残留
    if current_sent:
        sentences.append(current_sent)
        
    
    # --- 4. 装箱逻辑 (Bin Packing) 与 动态还原 ---
    
    chunks = []
    current_chunk_text = ""
    current_chunk_len = 0
    
    threshold = token_limit * buffer_ratio
    
    for sent in sentences:
        # 核心逻辑：时刻计算“还原后”的真实长度
        # 因为 __MASK_LATEX_0__ 很短，但实际公式可能很长
        real_text_sent = restore_text(sent, placeholders)
        cost = estimate_cost(real_text_sent)
        
        # 情况 A: 单个句子（或单行极长代码）直接超标
        if cost > threshold:
            # 1. 先封存当前已有的内容
            if current_chunk_text:
                chunks.append(restore_text(current_chunk_text, placeholders))
                current_chunk_text = ""
                current_chunk_len = 0
            
            # 2. 放入这个超长句子（含公式还原）
            # 注意：如果这里是一个超大的 LaTeX 块，它会被完整保留（不切断），尽管超过了 token 限制，但为了语义完整性，这是必须的妥协。
            # 如果是超长代码行，也会被保留。
            chunks.append(real_text_sent) 
            continue
            
        # 情况 B: 累加后超标
        if current_chunk_len + cost > threshold:
            # 封箱
            chunks.append(restore_text(current_chunk_text, placeholders))
            # 开启新箱子
            current_chunk_text = sent # 注意：这里累积仍使用带Mask的文本，为了性能
            current_chunk_len = cost
        else:
            # 加入当前箱子
            current_chunk_text += sent
            current_chunk_len += cost
            
    # --- 5. 收尾 ---
    if current_chunk_text:
        chunks.append(restore_text(current_chunk_text, placeholders))
        
    return chunks

def restore_text(text, placeholders):
    """
    辅助函数：将占位符还原为原始文本
    """
    if "__MASK_LATEX_" not in text:
        return text
        
    def replace_back(match):
        try:
            idx = int(match.group(1))
            return placeholders[idx]
        except (ValueError, IndexError):
            # 容错处理，理论上不会走到这里
            return match.group(0)
    
    return re.sub(r'__MASK_LATEX_(\d+)__', replace_back, text)

def estimate_cost(text):
    """
    Token 消耗估算 (逻辑不变)
    """
    cost = 0.0
    for char in text:
        code = ord(char)
        if code < 128:
            cost += 0.35
        elif 0x4E00 <= code <= 0x9FFF:
            cost += 0.65
        else:
            cost += 1.3
    return cost
