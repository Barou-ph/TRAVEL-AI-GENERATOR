import streamlit as st
import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import random

# =========================
# 🔑 INIT
# =========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# 🗄️ DATABASE
# =========================
conn = sqlite3.connect("content.db", check_same_thread=False)
c = conn.cursor()

c.execute(
    """
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    content TEXT
)
"""
)
conn.commit()

# =========================
# 📚 CASE LIBRARY (CỰC QUAN TRỌNG)
# =========================
CASE_LIBRARY = [
    "team sales mất động lực sau quý KPI thấp",
    "team IT ít giao tiếp, làm việc rời rạc",
    "công ty tăng trưởng nhanh, nhân sự mới chưa gắn kết",
    "team burnout sau thời gian chạy dự án liên tục",
    "leader muốn giữ chân nhân sự giỏi",
]

# =========================
# ✈️ UI
# =========================
st.title("🏢 Team Building AI - BÁN ĐƯỢC THẬT")

mode = st.selectbox(
    "Chọn mode", ["Content (Facebook)", "Case-based (B2B chuẩn)", "Sales Insight"]
)

# =========================
# ✏️ INPUT
# =========================
tour_name = st.text_input("Tên tour")
destinations = st.text_input("Địa điểm")
time = st.text_input("Thời gian")
price = st.text_input("Giá")

col1, col2 = st.columns(2)

with col1:
    company_size = st.selectbox("Quy mô", ["<20", "20-50", "50-200", "200+"])
    industry = st.text_input("Ngành (IT, Sales...)")

with col2:
    goal = st.selectbox(
        "Mục tiêu", ["Gắn kết", "Tăng động lực", "Giữ chân nhân sự", "Giải tỏa stress"]
    )
    style = st.selectbox(
        "Phong cách", ["Sắc sảo", "Nhẹ nhàng", "Chuyên nghiệp", "Hài hước"]
    )

# =========================
# 🤖 GENERATORS
# =========================


def generate_content():
    prompt = f"""
Viết bài quảng cáo Facebook cho tour team building theo phong cách tự nhiên, dễ đọc, giống người bán thật.

Thông tin:
- Tour: {tour_name}
- Địa điểm: {destinations}
- Thời gian: {time}
- Giá: {price}
- Quy mô: {company_size}
- Ngành: {industry}
- Mục tiêu: {goal}

FORMAT BẮT BUỘC:

1. MỞ ĐẦU:
- Nhẹ nhàng, relatable
- Không dạy đời, không phân tích

2. GIỚI THIỆU TOUR:
Viết kiểu:
"Tour này có gì?"

3. BULLET POINT (QUAN TRỌNG):
- Mỗi dòng 1 ý
- Có emoji (✅ hoặc 🎯)
- Nội dung cụ thể, dễ hình dung

Ví dụ:
✅ Hoạt động gắn kết: ...
✅ Không gian: ...
✅ Trải nghiệm: ...
✅ Dịch vụ: ...

4. GIÁ:
💰 GIÁ: {price}

5. ƯU ĐÃI (nếu hợp lý):
🎁 ...

6. CTA:
- Nhẹ nhàng
- Không ép mua
- Ví dụ: "Inbox để mình gửi lịch trình chi tiết"

YÊU CẦU:

- KHÔNG dùng mấy từ kiểu:
  "góc nhìn", "thực tế", "giải pháp", "doanh nghiệp thường sai"
- KHÔNG viết như consultant
- KHÔNG phân tích dài dòng
- VIẾT NHƯ NGƯỜI BÁN TOUR

- Có 2–4 emoji (đúng chỗ)
- Câu ngắn, dễ đọc
- Xuống dòng rõ ràng

Độ dài: 120–180 từ
"""

    res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "Bạn là người bán tour, viết content Facebook dễ đọc, có tính bán hàng, không viết như chuyên gia.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=400,
    )

    return res.choices[0].message.content


def generate_normal_content():
    prompt = f"""
Viết content Facebook cho team building nhưng theo hướng sắc sảo, thực tế.

Thông tin:
- Tour: {tour_name}
- Địa điểm: {destinations}
- Thời gian: {time}
- Quy mô: {company_size}
- Ngành: {industry}
- Mục tiêu: {goal}

YÊU CẦU:

- Mở đầu bằng 1 nhận định thẳng (có thể hơi gây tranh cãi)
  ví dụ: "Team building không giải quyết được vấn đề nếu làm sai cách"

- Phân tích ngắn: vì sao doanh nghiệp thường làm sai

- Đưa ra góc nhìn khác (cách làm đúng)

- Kết thúc bằng CTA mở

- Không viết kiểu truyền cảm hứng
- Không kể lể dài dòng
- Không sáo rỗng

Tone:
- Giống người hiểu doanh nghiệp
- Hơi "cứng", logic, không nịnh

120-150 từ
"""

    res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "Bạn là consultant B2B, không phải copywriter",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )

    return res.choices[0].message.content


def generate_sales_insight():
    prompt = f"""
Bạn là sales team building B2B.

Phân tích khách hàng:
- Quy mô: {company_size}
- Ngành: {industry}
- Mục tiêu: {goal}

Hãy đưa ra:

1. Insight thật của khách hàng này
2. Nỗi đau họ KHÔNG nói ra
3. Lý do họ sẽ từ chối team building
4. Góc tiếp cận để chốt deal

Ngắn gọn, thực tế, không lý thuyết.
"""

    res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Bạn là sales B2B giỏi"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )

    return res.choices[0].message.content


# =========================
# 🚀 ACTION
# =========================
if st.button("🔥 Generate"):

    if mode == "Case-based (B2B chuẩn)":
        output = generate_content()

    elif mode == "Sales Insight":
        output = generate_sales_insight()

    else:
        output = generate_normal_content()

    st.text_area("📄 Output", output, height=300)

    # save DB
    c.execute("INSERT INTO history (type, content) VALUES (?, ?)", (mode, output))
    conn.commit()

# =========================
# 📚 HISTORY
# =========================
st.subheader("📚 History")

rows = c.execute("SELECT * FROM history ORDER BY id DESC LIMIT 5").fetchall()

for row in rows:
    st.text(f"Mode: {row[1]}")
    st.code(row[2])
