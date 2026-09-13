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
    import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# 1. SEO va Sahifa Sozlamalari
st.set_page_config(
    page_title="LexiDraft AI — Yuridik Konsultant",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Meta-teglar (Google va brauzerlar uchun)
st.markdown("""
    <meta name="description" content="O'zbekiston qonunchiligi bo'yicha AI yuridik konsulatsiyasi va rasmiy hujjatlar yaratuvchi tizim.">
    <meta name="keywords" content="yuridik maslahat, ariza yaratish, O'zbekiston qonunlari, AI yurist">
""", unsafe_allow_html=True)

# 2. Gemini API Sozlamasi
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi! Streamlit Secrets bo'limiga GEMINI_API_KEY joylang.")

model = genai.GenerativeModel('gemini-1.5-flash')

# Word hujjat yaratish funksiyasi
def create_docx(text):
    doc = Document()
    doc.add_heading('Yuridik Hujjat va Maslahat', level=1)
    for paragraph in text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# Interfeys: Sarlavha
st.title("⚖️ LexiDraft AI")
st.caption("O'zbekiston Respublikasi qonunchiligiga asoslangan intellektual yuridik yordamchi")

# Funksiya 1: Rasmiy Huquqiy Ogohlantirish
st.warning("⚠️ **Eslatma:** Tizim sun'iy intellektga asoslangan. Berilgan maslahatlar axborot xarakterida bo'lib, rasmiy advokatlik xizmatini o'rnini bosmaydi.")

# Yon panel (Sidebar)
with st.sidebar:
    st.header("⚙️ Sozlamalar")
    
    # Funksiya 2: Yuridik Sohani Tanlash
    category = st.selectbox(
        "Huquqiy sohani tanlang:",
        ["Umumiy maslahat", "Mehnat huquqi", "Fuqarolik va Mulk", "Oila huquqi", "Tadbirkorlik va Shartnomalar", "Ma'muriy huquq"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 Ko'rsatma")
    st.write("Muammoingizni imkon qadar batafsil bayon eting. Tizim O'zbekiston kodekslariga havolalar bilan javob beradi va rasmiy ariza namunasini tuzadi.")

# Funksiya 3: Tayyor Namuna Savollari
st.subheader("📋 Tezkor shablonlar (Tanlash uchun bosing):")
col1, col2 = st.columns(2)

selected_sample = ""
with col1:
    if st.button("💼 Maosh berilmayapti"):
        selected_sample = "Ish beruvchi 2 oydan beri maoshimni bermayapti. Qayerga murojaat qilsam bo'ladi va qanday ariza yozaman?"
with col2:
    if st.button("📜 Arenda shartnomasi buzilishi"):
        selected_sample = "Ijarada turgan joyimdan uy egasi shartnoma muddatidan oldin sababsiz chiqarib yubormoqchi. Huquqlarim qanday?"

# Matn kiritish maydoni
prompt_input = st.text_area(
    "Huquqiy muammoingizni yozing:",
    value=selected_sample if selected_sample else "",
    placeholder="Masalan: Ish beruvchi mehnat ta'tiliga chiqarishni rad etyapti...",
    height=140
)

# Asosiy tugma
if st.button("🔍 Maslahat va Hujjat Olish", type="primary"):
    if not prompt_input.strip():
        st.error("Iltimos, avval muammoingizni yozing!")
    else:
        with st.spinner("Qonunchilik bazasi tahlil qilinmoqda va hujjat tayyorlanmoqda..."):
            try:
                system_instruction = f"""
                Siz O'zbekiston Respublikasi qonunchiligi bo'yicha tajribali yurist va advokatsiz.
                Soha: {category}.
                Foydalanuvchi murojaati: {prompt_input}
                
                Iltimos, quyidagi tuzilishda javob bering:
                1. **Huquqiy Maslahat**: O'zR kodekslari va moddalariga havola bergan holda muammoni tushuntiring.
                2. **Amaliy Qadamlar**: Fuqaro tartib bilan nima qilishi kerakligi.
                3. **Rasmiy Ariza/Murojaat Namunasi**: Tegishli tashkilotga (Sud, Prokuratura, Mehnat inspeksiyasi va h.k.) topshiriladigan tayyor ariza matni.
                """
                
                response = model.generate_content(system_instruction)
                result_text = response.text
                
                st.success("Maslahat va ariza tayyorlandi!")
                st.markdown(result_text)
                
                st.markdown("---")
                st.subheader("📥 Hujjatni yuklab olish")
                
                # Funksiya 4: Word va TXT shaklida yuklab olish
                c1, c2 = st.columns(2)
                
                docx_bytes = create_docx(result_text)
                with c1:
                    st.download_button(
                        label="📄 Word (.docx) yuklash",
                        data=docx_bytes,
                        file_name="Yuridik_Maslahat.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                with c2:
                    st.download_button(
                        label="📝 Matn (.txt) yuklash",
                        data=result_text,
                        file_name="Yuridik_Maslahat.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")


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
