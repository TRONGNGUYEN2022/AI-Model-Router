import json
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Model Router & Prompt Optimizer", page_icon="🚀", layout="centered")

st.title("🚀 AI Model Router & Prompt Optimizer (Gemini)")
st.write("Hệ thống tự động định tuyến mô hình AI và tối ưu hóa câu lệnh sử dụng Gemini API.")

# Ô nhập Google Gemini API Key
user_api_key = st.text_input("Nhập Google Gemini API Key của bạn:", type="password", placeholder="AIzaSy...")

if not user_api_key:
    st.warning("Vui lòng nhập Gemini API Key để bắt đầu sử dụng ứng dụng! (Lấy key miễn phí tại aistudio.google.com)")
else:
    try:
        client = genai.Client(api_key=user_api_key)
        
        query = st.text_area("Nhập yêu cầu của bạn:", placeholder="Ví dụ: Tạo game nhập vai với yêu cầu...")

        if st.button("Phân tích & Tối ưu Prompt", type="primary"):
            if not query.strip():
                st.warning("Vui lòng nhập nội dung yêu cầu!")
            else:
                with st.spinner("AI đang phân tích yêu cầu và tối ưu hóa..."):
                    system_instruction = """
                    Bạn là AI Router thông minh và chuyên nghiệp. Dựa trên yêu cầu của người dùng, hãy chọn mô hình AI phù hợp nhất:
                    - Nếu là code, lập trình, debug: Chọn 'Claude 3.5 Sonnet'
                    - Nếu là suy luận logic phức tạp, viết văn bản dài, phân tích sâu: Chọn 'GPT-4o' hoặc 'Gemini 1.5 Pro'
                    - Nếu là sáng tạo hình ảnh, thiết kế đồ họa: Chọn 'Midjourney v6' hoặc 'DALL-E 3'
                    - Nếu là dịch thuật, tóm tắt nhanh, hỏi đáp cơ bản: Chọn 'Gemini 1.5 Flash'
                    
                    Hãy trả về kết quả dưới dạng JSON thuần túy (không có markdown bao quanh) với các trường cấu trúc sau:
                    {
                        "model_name": "Tên mô hình AI được đề xuất",
                        "reason": "Lý do cụ thể tại sao chọn mô hình này",
                        "system_prompt": "System prompt phù hợp để điều hướng model đó",
                        "optimized_prompt": "User prompt đã được tối ưu, rõ ràng và chi tiết cho model đó"
                    }
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=query,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            response_mime_type="application/json",
                        ),
                    )
                    
                    data = json.loads(response.text)
                    
                    st.success("Phân tích và tối ưu thành công!")
                    st.info(f"**Mô hình đề xuất:** {data.get('model_name')}\n\n**Lý do lựa chọn:** {data.get('reason')}")
                    st.text_area("System Prompt gợi ý:", value=data.get('system_prompt'), height=100)
                    st.text_area("User Prompt tối ưu:", value=data.get('optimized_prompt'), height=120)
                    
    except Exception as e:
        st.error(f"Đã xảy ra lỗi (có thể do API Key không hợp lệ): {str(e)}")