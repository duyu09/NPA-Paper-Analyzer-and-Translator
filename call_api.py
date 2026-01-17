# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
from zai import ZhipuAiClient
import json

class TranslationService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None

    def _init_client(self):
        self.client = ZhipuAiClient(api_key=self.api_key)

    def update_api_key(self, new_key):
        self.api_key = new_key
        self.client = None

    def stream_translation(self, content, model, source_lang, target_lang, term_table=None):
        self._init_client()
        
        # 构建术语表描述
        term_desc = "目前没有术语表。"
        if term_table:
            term_desc = f"当前的术语表（JSON格式）：\n{json.dumps(term_table, ensure_ascii=False, indent=2)}"
            # print(term_desc)

        system_prompt = f"""
你是一位精通人工智能领域的专业学术翻译专家。
任务：将用户提供的{source_lang} Markdown 论文翻译成流畅、专业的{target_lang}。

本次翻译任务包含术语一致性维护。
{term_desc}

请你严格按照 JSON 格式输出，不要输出任何 Markdown 标记（如 ```json）。
输出的 JSON 对象必须包含以下两个字段：
1. "term_table": 一个字典，包含本次翻译中出现的新增或修正的专有名词（键为原文，值为译文）。该表应累积之前的术语。
2. "translation": 翻译后的正文内容（字符串）。请注意，待译文本开头若有空格、换行等特殊符号，也要相应地保留！

翻译规则：
1. **保留格式**：严禁修改原文的 Markdown 标题、粗体、列表结构。
2. **保留公式**：凡是 LaTeX 公式（如 $x^2$ 或 $$...$$），必须原样保留，**绝对不要**翻译或修改公式中的变量名。也就是LaTex公式的格式和写法严格原封不动保留。
3. **术语准确**：使用人工智能及计算机科学领域的标准中文术语，并优先参考提供的术语表。
4. **代码保留**：代码块（```code```）中的内容不翻译。
5. **引用保留**：参考文献引用保持原样。

请直接输出 JSON 数据流。
"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                # thinking={
                # "type": "disabled",    # 启用深度思考模式 (遵循示例)
                # },
                response_format={
                    "type": "json_object"
                },
                stream=True,
                max_tokens=90000, # 稍微调大一点以防截断
                temperature=0.2,
                top_p=0.8,
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[API Error]: {str(e)}"