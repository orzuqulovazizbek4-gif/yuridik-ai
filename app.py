import io
import google.generativeai as genai
import streamlit as st
from docx import Document

st.set_page_config(page_title="AI Yuridik Maslahatchi", page_icon="⚖️")

st.title("⚖️ AI Yuridik Konsultant va Hujjat Yaratuvchi")
st.write(
    "Huquqiy muammoingizni yozing. Tizim qonuniy maslahat beradi va rasmiy ariza namunasini yaratadi."
)

# API kalitni server sozlarmasidan (Secrets) avtomatik oladi
api_key = st.secrets.get("GEMINI_API_KEY", "")

user_problem = st.text_area(
    "Muammoingizni batafsil yozing:",
    placeholder="Masalan: Ish beruvchi 2 oydan beri oylik maoshimni bermayapti, qayerga murojaat qilsam bo'ladi?",
)


def create_docx(text):
  doc = Document()
  doc.add_heading("Yuridik Maslahat va Hujjat Namunasi", level=1)
  for line in text.split("\n"):
    if line.strip():
      doc.add_paragraph(line)
  bio = io.BytesIO()
  doc.save(bio)
  return bio.getvalue()


if st.button("Maslahat va Ariza Olish"):
  if not api_key:
    st.error(
      "Server sozlamalarida API kalit topilmadi. Tizim administratoriga murojaat qiling."
    )
  elif not user_problem.strip():
    st.warning("Iltimos, muammoingizni yozing!")
  else:
    with st.spinner(
        "Qonunchilik tahlil qilinmoqda va hujjat tayyorlanmoqda..."
    ):
      try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.6-flash")

        prompt = f"""
                Siz O'zbekiston Respublikasi qonunchiligi bo'yicha professional yuridik maslahatchisiz.
                Foydalanuvchi muammosi: {user_problem}
                
                Quyidagi formatda javob bering:
                1. **HUQUQIY MASLAHAT**: O'zbekiston Respublikasi qonunlari va kodekslariga asoslanib fuqaro nima qilishi kerakligini qisqa va tushunarli tushuntiring.
                2. **ARIZA / SHIKOYAT NAMUNASI**: Tegishli davlat organiga topshirish uchun tayyor rasmiy ariza shaklini tuzing. Foydalanuvchi o'z ma'lumotlarini o'rniga qo'ya oladigan qilib [Ism-sharif], [Sana] joylarini qoldiring.
                """

        response = model.generate_content(prompt)
        st.markdown(response.text)

        docx_file = create_docx(response.text)
        st.download_button(
            label="📄 Ariza va Maslahatni Word (.docx) yuklab olish",
            data=docx_file,
            file_name="Yuridik_Hujjat.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
        )
      except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")