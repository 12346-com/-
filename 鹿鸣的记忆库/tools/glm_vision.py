#!/usr/bin/env python3
"""
GLM-4.6V 图片识别脚本（优化版）
- 自动压缩图片，避免超时
- 支持命令行调用
"""
import urllib.request
import json
import base64
import sys
import os
import io
from PIL import Image

API_KEY = "WBJGLKXBKEHYC0ZZI7IZ6SDVO6KN5AG6QQ5HRN15"
API_URL = "https://ai.gitee.com/v1/chat/completions"

def recognize_image(img_path, prompt="请描述这张图片的内容，重点是文字和选项"):
    """识别图片内容，自动压缩大图"""
    try:
        # 打开并压缩图片
        img = Image.open(img_path)
        max_size = 800
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            print(f"图片已压缩: {img.size}", file=sys.stderr)
        
        # 转 base64
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        data = json.dumps({
            "model": "GLM-4.6V",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
            ]}]
        }).encode('utf-8')
        
        req = urllib.request.Request(API_URL, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        })
        
        response = urllib.request.urlopen(req, timeout=120)
        result = json.loads(response.read().decode('utf-8'))
        return result.get('choices', [{}])[0].get('message', {}).get('content', '识别失败')
    except Exception as e:
        return f"识别出错: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 glm_vision.py <图片路径> [提示词]")
        sys.exit(1)
    
    img_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "请描述这张图片的内容，重点是文字和选项"
    
    result = recognize_image(img_path, prompt)
    print(result)