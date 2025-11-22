import base64
import json
from typing import Tuple, Dict
import httpx

from app.config import settings


async def classify_image(image_bytes: bytes) -> Tuple[str, str, str, float, str]:
    """
    使用 Qwen 视觉模型识别图片
    返回: (英文标签, 中文标签, 音标, 置信度, 原始响应JSON)
    """
    # 将图像转为 base64
    img_b64 = base64.b64encode(image_bytes).decode()
    img_url = f"data:image/jpeg;base64,{img_b64}"
    
    # 构造符合 OpenAI Chat Completion API 格式的请求
    payload = {
        "model": settings.model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": img_url}
                    },
                    {
                        "type": "text",
                        "text": "请识别图片中的主要物体。要求：\n1. 只返回物品的通用名称，不要包含品牌名\n2. 用JSON格式返回：{\"zh\": \"中文名称\", \"en\": \"英文名称\", \"phonetic\": \"英文音标(IPA格式)\"}\n3. 只返回JSON，不要其他说明文字\n4. 音标示例：apple -> /ˈæp.əl/"
                    }
                ]
            }
        ],
        "max_tokens": 100,
        "temperature": 0.3
    }
    
    headers = {
        "Authorization": f"Bearer {settings.siliconflow_api_key}",
        "Content-Type": "application/json",
    }
    
    # 调试：打印请求信息
    print(f"Model: {settings.model_name}")
    print(f"Image size: {len(image_bytes)} bytes")
    
    timeout = httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=10.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{settings.siliconflow_base_url}/chat/completions",
            json=payload,
            headers=headers
        )
        
        # 捕获错误并打印详细信息
        if resp.status_code != 200:
            error_detail = resp.text
            print(f"API Error {resp.status_code}: {error_detail}")
            raise httpx.HTTPStatusError(
                f"API request failed: {error_detail}",
                request=resp.request,
                response=resp
            )
        
        data = resp.json()
        
        # 保存原始响应
        raw_response = json.dumps(data, ensure_ascii=False)
        
        # 解析响应
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        
        try:
            # 尝试解析JSON响应
            result = json.loads(content)
            label_zh = result.get("zh", "未知物体")
            label_en = result.get("en", "unknown")
            phonetic = result.get("phonetic", "")
            confidence = 0.8  # Qwen模型不直接返回置信度，使用固定值
        except json.JSONDecodeError:
            # 如果不是JSON格式，尝试从文本中提取
            label_zh = content.strip() if content else "未知物体"
            label_en = "unknown"
            phonetic = ""
            confidence = 0.5
        
        return label_en, label_zh, phonetic, confidence, raw_response