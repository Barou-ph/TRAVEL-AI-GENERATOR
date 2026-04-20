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
    content TEXT
)
"""
)
conn.commit()

# =========================
# 📚 CASE LIBRARY
# =========================
CASE_LIBRARY = [
    "mất động lực sau thời gian KPI thấp",
    "ít giao tiếp, làm việc rời rạc",
    "nhân sự mới không hòa nhập",
    "burnout sau thời gian chạy dự án",
    "leader muốn giữ chân người giỏi nhưng chưa có cách",
]

# =========================
# ✈️ UI
# =========================
st.title("🏢 Team Building AI")

tour_name = st.text_input("Tên tour")
destinations = st.text_input("Địa điểm")
time = st.text_input("Thời gian")
price = st.text_input("Giá")

col1, col2 = st.columns(2)

with col1:
    group_size = st.text_input("Số lượng khách (vd: 20 người, 50 pax)")
    customer_type = st.text_input("Đối tượng khách (team sales, IT, nhân sự mới...)")

with col2:
    goal = st.selectbox(
        "Mục tiêu", ["Gắn kết", "Tăng động lực", "Giữ chân nhân sự", "Giải tỏa stress"]
    )
    urgency = st.selectbox("Độ gấp", ["Bình thường", "Còn ít slot", "Cao điểm"])

# =========================
# 🤖 GENERATORS
# =========================


def generate_hook(goal, case):
    prompt = f"""
Viết 1 câu mở đầu cho bài bán team building.

- Dựa trên tình huống: {case}
- Mục tiêu: {goal}

Yêu cầu:
- Ngắn (1-2 dòng)
- Đúng vấn đề
- Không triết lý
- Không chung chung
"""
    res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=60,
    )
    return res.choices[0].message.content.strip()


def generate_content():
    # chọn case
    base_case = random.choice(CASE_LIBRARY)

    # FIX: gắn đúng đối tượng khách → tránh lệch insight
    if customer_type:
        case = f"{customer_type} đang gặp vấn đề: {base_case}"
    else:
        case = base_case

    hook = generate_hook(goal, case)

    prompt = f"""
Viết bài quảng cáo Facebook bán tour team building.

BẮT BUỘC mở đầu bằng câu này:
"{hook}"

Thông tin:
- Tour: {tour_name}
- Địa điểm: {destinations}
- Thời gian: {time}
- Giá: {price}
- Số lượng khách: {group_size}
- Đối tượng khách: {customer_type}
- Tình huống: {case}

FORMAT BẮT BUỘC:

- Sau đoạn mở, xuống dòng

Tour này có gì?

✅ Hoạt động cụ thể (gắn trực tiếp với vấn đề team)
✅ Không gian / trải nghiệm
✅ Giá trị thật team nhận được
✅ Dịch vụ đi kèm

👉 Vì sao nên đi tour này:
- 2-3 bullet cực cụ thể (không chung chung)

💰 Giá: {price}
"""

    # FOMO logic
    if urgency == "Còn ít slot":
        prompt += "\n🎁 Chỉ còn vài slot cho tháng này\n"
    elif urgency == "Cao điểm":
        prompt += "\n🎁 Mùa cao điểm, nên đặt sớm để giữ lịch\n"

    prompt += """

💬 CTA:
- Viết tự nhiên
- Không ép mua

YÊU CẦU:

- Viết để người đọc thấy “đúng vấn đề của team mình”
- Không viết kiểu event vui vẻ chung chung
- Không dùng mấy từ kiểu:
  "góc nhìn", "thực tế", "giải pháp", "doanh nghiệp thường"
- Không viết như consultant
- Viết như người bán tour thật
- Câu ngắn, dễ đọc
- Có emoji hợp lý

Độ dài: 120-180 từ
"""

    res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "Bạn là người bán team building, viết content Facebook để chốt khách.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.85,
        max_tokens=400,
    )

    return res.choices[0].message.content


# =========================
# 🚀 ACTION
# =========================
if st.button("🔥 Generate"):
    output = generate_content()

    st.text_area("📄 Output", output, height=300)

    c.execute("INSERT INTO history (content) VALUES (?)", (output,))
    conn.commit()

# =========================
# 📚 HISTORY
# =========================
st.subheader("📚 History")

rows = c.execute("SELECT * FROM history ORDER BY id DESC LIMIT 5").fetchall()

for row in rows:
    st.code(row[1])
