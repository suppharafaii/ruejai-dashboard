import streamlit as st
import google.generativeai as genai

# เชื่อมต่อ API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ไม่พบ API Key ในระบบ")

st.title("📊 Ruejai Project Dashboard")

# ข้อมูลของคุณ Fai
SYSTEM_PROMPT = """
คุณคือ Product Owner ของ RueJai App
- กุมภาพันธ์ 2026: เชื่อมต่อระบบกับ CPW และ Dotlife เสร็จสิ้น
- เป้าหมาย: สรุปรายงานสำหรับผู้บริหาร
"""

if st.button("🚀 สรุปรายงานสำหรับผู้บริหาร"):
    try:
        # ใช้คำสั่งเรียกแบบเจาะจงรุ่นที่เสถียรที่สุด
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(SYSTEM_PROMPT + "\nสรุปงานเป็นข้อๆ ให้หน่อย")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("ลองเปลี่ยนรุ่นเป็น 'gemini-pro' ในโค้ดดูอีกครั้งครับ")
