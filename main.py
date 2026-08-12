from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import json
import os

app = FastAPI(title="AI Model Router Online")

# Khởi tạo OpenAI Client (Lấy API Key từ biến môi trường của Server Cloud)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_FALLBACK_API_KEY"))

templates = Jinja2Templates(directory="templates")

class UserRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Trang chủ hiển thị giao diện Web App"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/route")
async def route_request(request: UserRequest):
    """API endpoint nhận yêu cầu và trả về mô hình + prompt tối ưu"""
    system_instruction = """
    Bạn là AI Router thông minh và chuyên nghiệp. Dựa trên yêu cầu của người dùng, hãy chọn mô hình AI phù hợp nhất:
    - Nếu là code, lập trình, debug: Chọn 'Claude 3.5 Sonnet'
    - Nếu là suy luận logic phức tạp, viết văn bản dài, phân tích sâu: Chọn 'GPT-4o'
    - Nếu là sáng tạo hình ảnh, thiết kế đồ họa: Chọn 'Midjourney v6' hoặc 'DALL-E 3'
    - Nếu là dịch thuật, tóm tắt nhanh, hỏi đáp cơ bản: Chọn 'GPT-4o-mini'
    
    Hãy trả về cấu trúc JSON duy nhất (không kèm markdown ngoài) với các trường:
    {
        "model_name": "Tên mô hình AI được đề xuất",
        "reason": "Lý do cụ thể tại sao chọn mô hình này",
        "system_prompt": "System prompt phù hợp để điều hướng model đó",
        "optimized_prompt": "User prompt đã được tối ưu, rõ ràng và chi tiết cho model đó"
    }
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": request.query}
            ],
            response_format={"type": "json_object"}
        )
        result_data = json.loads(response.choices[0].message.content)
        return result_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))