import os
import json
from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="AI Model Router & Prompt Optimizer", page_icon="🚀", layout="centered")

st.title("🚀 AI Model Router & Prompt Optimizer")
st.write("Hệ thống tự động định tuyến mô hình AI và tối ưu hóa câu lệnh dựa trên yêu cầu của bạn.")

# Tạo ô nhập API Key trên giao diện
user_api_key = st.text_input("Nhập OpenAI API Key của bạn:", type="password", placeholder="sk-...")

if not user_api_key:
    st.warning("Vui lòng nhập OpenAI API Key để bắt đầu sử dụng ứng dụng!")
else:
    # Khởi tạo OpenAI client với key người dùng vừa nhập
    client = OpenAI(api_key=user_api_key)
    
    # Khung nhập yêu cầu của người dùng
    query = st.text_area("Nhập yêu cầu của bạn:", placeholder="Ví dụ: Viết một đoạn code Python crawl dữ liệu web hoặc vẽ một bức tranh phong cảnh...")

    if st.button("Phân tích & Tối ưu Prompt", type="primary"):
        if not query.strip():
            st.warning("Vui lòng nhập nội dung yêu cầu!")
        else:
            with st.spinner("AI đang phân tích yêu cầu và tối ưu hóa..."):
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
                            {"role": "user", "content": query}
                        ],
                        response_format={"type": "json_object"}
                    )
                    data = json.loads(response.choices[0].message.content)
                    
                    st.success("Phân tích và tối ưu thành công!")
                    
                    # Hiển thị kết quả đề xuất mô hình
                    st.info(f"**Mô hình đề xuất:** {data.get('model_name')}\n\n**Lý do lựa chọn:** {data.get('reason')}")
                    
                    # Hiển thị các câu lệnh đã tối ưu
                    st.text_area("System Prompt gợi ý:", value=data.get('system_prompt'), height=100)
                    st.text_area("User Prompt tối ưu:", value=data.get('optimized_prompt'), height=120)
                    
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi (có thể do API Key không hợp lệ hoặc hết hạn mức): {str(e)}")