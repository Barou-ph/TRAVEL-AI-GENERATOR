import os
from openai import OpenAI
from dotenv import load_dotenv
import ollama


def generate_tour_content(title, location, price, month, audience):

    prompt = f"""
Write a Facebook travel advertisement.

Tour: {title}
Location: {location}
Price: {price}
Month: {month}
Target audience: {audience}

Include:
- catchy headline
- short itinerary
- CTA
"""

    response = ollama.generate(model="llama3", prompt=prompt)

    return response["response"]


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_tour_content(tour_name, destinations, price, time, style):

    prompt = f"""
Viết bài quảng cáo Facebook cho tour du lịch.

Tour: {tour_name}
Điểm đến: {destinations}
Giá: {price}
Thời gian: {time}
Phong cách: {style}

Yêu cầu:
- Hook hấp dẫn
- Lịch trình ngắn
- Có emoji
- CTA
- <=120 từ
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )

    return response.choices[0].message.content


tour = generate_tour_content(
    "Tour Nhật Bản 5N4Đ", "Tokyo, Fuji, Kyoto", "28.900.000 VNĐ", "Tháng 4", "trẻ trung"
)

print(tour)
