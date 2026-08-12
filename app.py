import os
import json
from openai import OpenAI
import streamlit as st

# Lấy API Key từ Secrets của Streamlit (bảo mật tuyệt đối)
api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Model Router", page_icon="🚀", layout="centered")

st.title("🚀 AI Model Router & Prompt Optimizer")
st.write("Nhập yêu cầu của bạn, AI sẽ tự động chọn mô hình thích hợp và tối ưu câu lệnh.")

# Khung nhập yêu cầu
query = st.text_area("Yêu cầu của bạn:", placeholder="Ví dụ: Viết code Python crawl dữ liệu web...")

if st.button("Phân tích & Tối ưu Prompt", type="primary"):
    if not query.strip():
        st.warning("Vui lòng nhập yêu cầu!")
    else:
        with st.spinner("AI đang phân tích và chọn mô hình..."):
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
                
                # Hiển thị kết quả ra màn hình
                st.success("Đã phân tích thành công!")
                
                st.info(f"**Mô hình đề xuất:** {data.get('model_name')}\n\n**Lý do:** {data.get('reason')}")
                
                st.text_area("System Prompt gợi ý:", value=data.get('system_prompt'), height=100)
                st.text_area("User Prompt tối ưu:", value=data.get('optimized_prompt'), height=120)
                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {str(e)}")