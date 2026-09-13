import streamlit as st
import google.generativeai as genai
from docx import Document
import io

# ==============================================================================
# 1. SAHIFA SOZLAMALARI (DIQQAT: Ushbu buyruq doim ENG BOSHIDA turishi shart!)
# ==============================================================================
st.set_page_config(
    page_title="LexiDraft AI — Yuridik Konsultant",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. GOOGLE SEARCH CONSOLE VA SEO META-TEGLARI
# ==============================================================================
# Google Search Console taqdim etgan koddagi 'content' qiymatini pastdagi tirnoq ichiga yozing:
GOOGLE_VERIFICATION_CODE = "BU_YERGA_GOOGLE_KODINI_JOYLANG"

if GOOGLE_VERIFICATION_CODE != "BU_YERGA_GOOGLE_KODINI_JOYLANG":
    st.markdown(f'<meta name="google-site-verification" content="{GOOGLE_VERIFICATION_CODE}" />', unsafe_allow_html=True)

st.markdown("""
    <meta name="description" content="O'zbekiston qonunchiligi bo'yicha AI yuridik konsulatsiyasi va rasmiy hujjatlar yaratuvchi intellektual tizim.">
    <meta name="keywords" content="yuridik maslahat, ariza yaratish, O'zbekiston qonunlari, AI yurist, LexiDraft">
""", unsafe_allow_html=True)

# ==============================================================================
# 3. GEMINI API SOZLAMALARI
# ==============================================================================
api_key = st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.6-flash')
else:
    st.error("⚠️ GEMINI_API_KEY topilmadi! Streamlit Cloud -> Settings -> Secrets bo'limini tekshiring.")

# ==============================================================================
# 4. WORD (.DOCX) HUJJAT YARATISH FUNKSIYASI
# ==============================================================================
def create_docx(text):
    doc = Document()
    doc.add_heading('LexiDraft AI — Yuridik Hujjat va Maslahat', level=1)
    for paragraph in text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# ==============================================================================
# 5. TAYYOR SHABLONLAR UCHUN XOTIRA (SESSION STATE)
# ==============================================================================
if "prompt_text" not in st.session_state:
    st.session_state["prompt_text"] = ""

def set_sample_prompt(text):
    st.session_state["prompt_text"] = text

# ==============================================================================
# 6. FOYDALANUVCHI INTERFEYSI (UI)
# ==============================================================================
st.title("⚖️ LexiDraft AI")
st.caption("O'zbekiston Respublikasi qonunchiligiga asoslangan intellektual yuridik yordamchi")

# Rasmiy ogohlantirish
st.warning("⚠️ **Eslatma:** Tizim sun'iy intellektga asoslangan. Berilgan maslahatlar axborot xarakterida bo'lib, rasmiy advokatlik xizmati o'rnini bosmaydi.")

# Yon panel (Sidebar)
with st.sidebar:
    st.header("⚙️ Sozlamalar")
    category = st.selectbox(
        "Huquqiy sohani tanlang:",
        [
            "Umumiy maslahat", 
            "Mehnat huquqi", 
            "Fuqarolik va Mulk", 
            "Oila huquqi", 
            "Tadbirkorlik va Shartnomalar", 
            "Ma'muriy huquq"
        ]
    )
    st.markdown("---")
    st.markdown("### 💡 Ko'rsatma")
    st.write("Muammoingizni imkon qadar batafsil bayon eting. Tizim O'zbekiston kodekslariga havolalar beradi va tayyor ariza namunasini shakllantiradi.")

# Tayyor shablon tugmalari
st.subheader("📋 Tezkor shablonlar (Tanlash uchun bosing):")
col1, col2 = st.columns(2)

with col1:
    st.button(
        "💼 Maosh berilmayapti", 
        on_click=set_sample_prompt, 
        args=("Ish beruvchi 2 oydan beri maoshimni bermayapti. Qayerga murojaat qilsam bo'ladi va qanday ariza yozaman?",)
    )

with col2:
    st.button(
        "📜 Ijaradan chiqarish", 
        on_click=set_sample_prompt, 
        args=("Ijarada turgan joyimdan uy egasi shartnoma muddatidan oldin sababsiz chiqarib yubormoqchi. Huquqlarim qanday?",)
    )

# Matn kiritish oynasi
user_prompt = st.text_area(
    "Huquqiy muammoingizni yozing:",
    key="prompt_text",
    placeholder="Masalan: Ish beruvchi mehnat ta'tiliga chiqarishni rad etyapti...",
    height=140
)

# Natijani chiqarish tugmasi
if st.button("🔍 Maslahat va Hujjat Olish", type="primary"):
    if not user_prompt.strip():
        st.error("Iltimos, avval muammoingizni yozing!")
    elif not api_key:
        st.error("API kalit o'rnatilmagan. Streamlit Secrets bo'limini tekshiring.")
    else:
        with st.spinner("Qonunchilik bazasi tahlil qilinmoqda va hujjat tayyorlanmoqda..."):
            try:
                system_instruction = f"""
                Siz O'zbekiston Respublikasi qonunchiligi bo'yicha tajribali yurist va advokatsiz.
                Tanlangan soha: {category}.
                Foydalanuvchi murojaati: {user_prompt}
                
                Iltimos, quyidagi tuzilishda aniq va tushunarli javob bering:
                1. **Huquqiy Maslahat**: O'zR tegishli kodekslari va moddalariga havolalar bilan muammoni tushuntiring.
                2. **Amaliy Qadamlar**: Fuqaro tartib bilan nima qilishi kerak.
                3. **Rasmiy Ariza/Murojaat Namunasi**: Tegishli idoraga (Sud, Prokuratura, Mehnat inspeksiyasi va h.k.) topshiriladigan to'liq va rasmiy ariza matni.
                """
                
                response = model.generate_content(system_instruction)
                result_text = response.text
                
                st.success("Maslahat va ariza namunasi tayyorlandi!")
                st.markdown(result_text)
                
                st.markdown("---")
                st.subheader("📥 Hujjatni yuklab olish")
                
                c1, c2 = st.columns(2)
                
                # Word fayli
                docx_bytes = create_docx(result_text)
                with c1:
                    st.download_button(
                        label="📄 Word (.docx) yuklash",
                        data=docx_bytes,
                        file_name="Yuridik_Maslahat_LexiDraft.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                # TXT fayli
                with c2:
                    st.download_button(
                        label="📝 Matn (.txt) yuklash",
                        data=result_text,
                        file_name="Yuridik_Maslahat_LexiDraft.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"Yuzaga kelgan xatolik: {e}")
