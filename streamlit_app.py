import streamlit as st
import google.generativeai as genai

# ส่วนเชื่อมต่อกับรหัสลับที่เราจะไปตั้งใน Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("📊 Ruejai Project Dashboard")

# ก๊อปปี้ข้อมูลที่คุณพิมพ์ไว้ใน AI Studio มาวางในนี้ครับ
SYSTEM_PROMPT = """
คุณคือผู้ช่วยสรุปงานโปรเจกต์ RueJai App...
[ใส่ข้อมูล Progress รายเดือนของคุณที่นี่]
"""

if st.button("สรุปรายงานสำหรับผู้บริหาร"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(SYSTEM_PROMPT + "\nช่วยสรุป Progress งานเป็นข้อๆ")
    st.markdown(response.text)
