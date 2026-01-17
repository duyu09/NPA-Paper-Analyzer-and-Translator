# Copyright (c) 2025~2026 DuYu (qluduyu09@163.com; 11250717@stu.lzjtu.edu.cn), Lanzhou Jiaotong University
import os
import time
import requests
import zipfile
import io

def parse_pdf_mineru(api_key: str, file_path: str, output_dir: str) -> dict:
    """
    使用 MinerU API 解析单个 PDF 文件并解压结果到指定目录。
    
    Args:
        api_key (str): MinerU 的 API Token (不需要带 Bearer 前缀，函数内部会自动处理)。
        file_path (str): 本地 PDF 文件的绝对或相对路径。
        output_dir (str): 解析结果存放的文件夹路径。
        
    Returns:
        dict: {'code': 0, 'msg': '...'} (0表示成功，1表示失败)
    """
    
    # 1. 基础校验与配置
    if not os.path.exists(file_path):
        return {"code": 1, "msg": f"文件不存在: {file_path}"}
    
    file_name = os.path.basename(file_path)
    base_url = "https://mineru.net/api/v4"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 2. 申请上传链接 (Batch API)
    try:
        apply_url = f"{base_url}/file-urls/batch"
        payload = {
            "files": [
                {"name": file_name, "data_id": "task_001"} # data_id 可自定义，此处作为单次任务标识
            ],
            "model_version": "vlm" # 根据文档默认推荐，也可选 pipeline
        }
        
        resp = requests.post(apply_url, headers=headers, json=payload)
        resp_json = resp.json()
        
        if resp.status_code != 200 or resp_json.get("code") != 0:
            return {"code": 1, "msg": f"申请上传链接失败: {resp_json.get('msg', resp.text)}"}
            
        batch_id = resp_json["data"]["batch_id"]
        upload_url = resp_json["data"]["file_urls"][0] # 因为是单文件，取第一个
        
        print(f"[1/4] 任务创建成功，Batch ID: {batch_id}")

    except Exception as e:
        return {"code": 1, "msg": f"请求API异常: {str(e)}"}

    # 3. 上传文件
    try:
        with open(file_path, 'rb') as f:
            # 文档特别说明：上传文件时，无须设置 Content-Type 请求头
            upload_resp = requests.put(upload_url, data=f)
            
        if upload_resp.status_code != 200:
            return {"code": 1, "msg": f"文件上传失败，HTTP状态码: {upload_resp.status_code}"}
            
        print("[2/4] 文件上传成功，等待解析...")
        
    except Exception as e:
        return {"code": 1, "msg": f"文件上传过程发生错误: {str(e)}"}

    # 4. 轮询查询任务状态
    query_url = f"{base_url}/extract-results/batch/{batch_id}"
    max_retries = 1000 # 最大轮询次数，防止死循环
    wait_seconds = 3  # 每次轮询间隔秒数
    download_url = None
    
    for _ in range(max_retries):
        try:
            # 查询状态
            q_resp = requests.get(query_url, headers=headers)
            q_data = q_resp.json()
            
            if q_data.get("code") != 0:
                return {"code": 1, "msg": f"查询任务状态失败: {q_data.get('msg')}"}
            
            # 获取单文件的结果
            extract_results = q_data["data"]["extract_result"]
            # 找到对应文件名的结果
            target_file_result = next((item for item in extract_results if item["file_name"] == file_name), None)
            
            if not target_file_result:
                return {"code": 1, "msg": "未在任务结果中找到该文件"}
                
            state = target_file_result["state"]
            
            if state == "done":
                download_url = target_file_result["full_zip_url"]
                print("[3/4] 解析完成，准备下载结果...")
                break
            elif state == "failed":
                err_msg = target_file_result.get("err_msg", "未知错误")
                return {"code": 1, "msg": f"解析失败: {err_msg}"}
            else:
                # running, waiting-file, pending, converting 等状态
                progress = target_file_result.get("extract_progress", {})
                processed = progress.get("extracted_pages", 0)
                total = progress.get("total_pages", "?")
                print(f"    ...当前状态: {state} (进度: {processed}/{total})")
                time.sleep(wait_seconds)
                
        except Exception as e:
            # 网络抖动允许重试，不直接退出
            print(f"轮询警告: {str(e)}")
            time.sleep(wait_seconds)
    else:
        return {"code": 1, "msg": "解析超时，请稍后检查 MinerU 控制台"}

    # 5. 下载并解压结果
    if not download_url:
        return {"code": 1, "msg": "解析完成但未获取到下载链接"}
        
    try:
        # 下载 ZIP 文件
        zip_resp = requests.get(download_url)
        if zip_resp.status_code != 200:
            return {"code": 1, "msg": "下载结果文件失败"}
            
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 在内存中解压
        with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
            z.extractall(output_dir)
            
        print(f"[4/4] 结果已保存至: {output_dir}")
        return {"code": 0, "msg": ""}
        
    except Exception as e:
        return {"code": 1, "msg": f"下载或解压失败: {str(e)}"}
