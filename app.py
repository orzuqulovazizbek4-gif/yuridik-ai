import streamlit as st
import google.generativeai as genai
from docx import Document
import io
from datetime import datetime

# ==============================================================================
# 1. SAHIFA SOZLAMALARI (ENG BOSHIDA TURISHI SHART)
# ==============================================================================
st.set_page_config(
    page_title="LexiDraft AI — Intellektual Yuridik Tizim",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DIZAYN VA CSS USLUBI
# ==============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .info-box {
        background-color: #F0F9FF;
        border-left: 5px solid #0284C7;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. GOOGLE SEARCH CONSOLE VA SEO META-TEGLARI
# ==============================================================================
GOOGLE_VERIFICATION_CODE = "BU_YERGA_GOOGLE_KODINI_JOYLANG"

if GOOGLE_VERIFICATION_CODE != "BU_YERGA_GOOGLE_KODINI_JOYLANG":
    st.markdown(f'<meta name="google-site-verification" content="{GOOGLE_VERIFICATION_CODE}" />', unsafe_allow_html=True)

st.markdown("""
    <meta name="description" content="O'zbekiston Respublikasi qonunchiligi bo'yicha sun'iy intellektga asoslangan professional yuridik konsultatsiya va rasmiy hujjatlar generatsiyasi platformasi.">
    <meta name="keywords" content="yuridik maslahat, ariza namuna, O'zbekiston kodekslari, advokat AI, LexiDraft, BHM kalkulyator">
""", unsafe_allow_html=True)

# ==============================================================================
# 4. GEMINI API VA MODELLAR TIZIMI (ROBUST FALLBACK)
# ==============================================================================
api_key = st.secrets.get("GEMINI_API_KEY", None)

def get_working_model():
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    
    # Modellarni birma-bir tekshirib, ishlaydiganini tanlash
    candidate_models = ['gemini-3.6-pro', 'gemini-3.6-flash-extended', 'gemini-3.6-flash', 'gemini-pro']
    for model_name in candidate_models:
        try:
            m = genai.GenerativeModel(model_name)
            return m
        except Exception:
            continue
    return genai.GenerativeModel('gemini-1.5-pro')

model = get_working_model()

# ==============================================================================
# 5. WORD (.DOCX) HUJJAT SHAKLLANTIRISH
# ==============================================================================
def create_docx(content, category_name):
    doc = Document()
    
    # Hujjat sarlavhasi va vaqti
    title_p = doc.add_paragraph()
    title_run = title_p.add_run('LexiDraft AI — RASMIY YURIDIK HUJJAT VA MASLAHAT')
    title_run.bold = True
    title_p.alignment = 1  # Center
    
    doc.add_paragraph(f"Soha: {category_name}")
    doc.add_paragraph(f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    doc.add_paragraph("-" * 50)
    
    for line in content.split('\n'):
        if line.strip():
            doc.add_paragraph(line.strip())
            
    doc.add_paragraph("-" * 50)
    doc.add_paragraph("Diqqat: Ushbu hujjat AI tomonidan shakllantirilgan. Huquqiy harakatlardan oldin mutaxassis bilan maslahatlashing.")
    
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# ==============================================================================
# 6. FOYDALANUVCHI INTERFEYSI (UI)
# ==============================================================================
st.markdown('<div class="main-header">⚖️ LexiDraft AI — Intellektual Yuridik Tizim</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">O\'zbekiston Respublikasi Amaldagi Qonunchiligi Asosida Professional Yordamchi</div>', unsafe_allow_html=True)

# Yon Panel (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/scale.png", width=70)
    st.title("⚙️ Boshqaruv Paneli")
    
    category = st.selectbox(
        "📌 Huquqiy Sohani Tanlang:",
        [
            "Umumiy Maslahat",
            "Mehnat Huquqi va Ish Nizo",
            "Fuqarolik va Mulk Huquqi",
            "Oila Huquqi va Aliment",
            "Tadbirkorlik va Shartnomalar",
            "Ma'muriy Huquq va Jarimalar",
            "Jinoyat va Prosessual Huquq"
        ]
    )
    
    st.markdown("---")
    
    # FUNKSIYA: BHM Kalkulyatori
    st.markdown("### 🧮 BHM Kalkulyatori")
    st.caption("O'zbekiston Respublikasidagi Bazaviy Hisoblash Miqdori bo'yicha hisob-kitob:")
    bhm_rate = st.number_input("1 BHM miqdori (so'mda):", value=375000, step=5000)
    bhm_count = st.number_input("BHM baravari kiritish:", value=1.0, step=0.5)
    total_bhm = bhm_rate * bhm_count
    st.info(f"**Jami summa:** {total_bhm:,.0f} so'm")
    
    st.markdown("---")
    st.markdown("### 📞 Ishonch Telefonlari")
    st.write("• **Adliya vazirligi:** 1008")
    st.write("• **Inson huquqlari (Ombudsman):** 1148")
    st.write("• **Mehnat inspeksiyasi:** 1282")

# Asosiy Kontent
st.warning("⚠️ **Rasmiy Ogohlantirish:** Tizim taqdim etadigan maslahat va namunalar axborot xarakterida bo'lib, sud yoki advokatlik xizmatlarining o'rnini to'liq bosmaydi.")

# Session state xotirasi
if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

def set_query(text):
    st.session_state["user_query"] = text

st.markdown("### 📋 Tezkor Shablonlar:")
c1, c2, c3 = st.columns(3)

with c1:
    st.button("💼 Ish haqim berilmayapti", on_click=set_query, args=("Ish beruvchi 2 oydan beri maoshimni bermayapti. Mehnat kodeksi bo'yicha qayerga murojaat qilaman va ariza namunasini tuzib bering.",))
with c2:
    st.button("📜 Ijarachi uyimdan chiqmayapti", on_click=set_query, args=("Ijarachi bilan shartnoma muddati tugadi, lekin u uydan chiqishni rad etyapti. Fuqarolik kodeksiga ko'ra nima qilishim kerak?",))
with c3:
    st.button("👶 Aliment undirish tartibi", on_click=set_query, args=("Nikohdan ajrashgandan so'ng aliment undirish tartibi va Sudga ariza namunasini tayyorlab bering.",))

# Matn kiritish oynasi
user_prompt = st.text_area(
    "Huquqiy muammo yoki savolingizni batafsil yozing:",
    key="user_query",
    placeholder="Masalan: Tadbirkorlik subyekti sifatida shartnoma majburiyatlari bajarilmaganda qaysi sudga murojaat qilinadi?...",
    height=150
)

col_action, col_clear = st.columns([4, 1])

with col_action:
    generate_btn = st.button("🔍 Tahlil Qilish va Hujjat Yaratish", type="primary", use_container_width=True)

with col_clear:
    if st.button("🗑️ Tozalash", use_container_width=True):
        st.session_state["user_query"] = ""
        st.rerun()

# Natijani generatsiya qilish
if generate_btn:
    if not user_prompt.strip():
        st.error("Iltimos, avval muammoingizni kiriting!")
    elif not api_key:
        st.error("API Kalit sozlanmagan! Streamlit Cloud -> Settings -> Secrets bo'limiga GEMINI_API_KEY joylang.")
    else:
        with st.spinner("O'zbekiston Respublikasi Kodekslari va qonunchiligi tahlil qilinmoqda..."):
            try:
                system_prompt = f"""
                Siz O'zbekiston Respublikasi amaldagi qonunchiligi bo'yicha oliy toifali advokat va yuridik konsultantsiz.
                Soha: {category}.
                Foydalanuvchi Murojaati: {user_prompt}

                Iltimos, javobni quyidagi aniq struktura va sarlavhalar bilan tayyorlang:

                ### 1. 📖 HUQUQIY TAHLIL VA MODDALAR
                - O'zbekiston Respublikasi tegishli Kodekslari va qonunlaridagi aniq moddalarga havolalar.
                - Fuqaroning yoki tashkilotning qonuniy huquqlari tushuntirishi.

                ### 2. 📝 AMALIY QADAMLAR
                - Bosqichma-bosqich qilinishi kerak bo'lgan harakatlar ketma-ketligi.
                - Qaysi idoraga (Sud, Prokuratura, Ichki Ishlar, Mehnat Inspeksiyasi) murojaat qilish kerakligi.

                ### 3. 📄 RASMIY ARIZA / MUROJAAT SHABLONI
                - Tegishli idoraga topshirish uchun to'liq va professional rasmiy ariza matni.
                """
                
                response = model.generate_content(system_prompt)
                res_text = response.text
                
                st.success("Tahlil va hujjat yaratish muvaffaqiyatli yakunlandi!")
                
                # Tablar ko'rinishida natijani ko'rsatish
                tab1, tab2 = st.tabs(["📄 Yuridik Tahlil va Maslahat", "📥 Hujjatni Yuklab Olish"])
                
                with tab1:
                    st.markdown(res_text)
                
                with tab2:
                    st.markdown("### Hujjatni qulay formatda yuklab oling:")
                    c_word, c_txt = st.columns(2)
                    
                    docx_data = create_docx(res_text, category)
                    
                    with c_word:
                        st.download_button(
                            label="📄 Word (.docx) formatida yuklash",
                            data=docx_data,
                            file_name=f"LexiDraft_Hujjat_{datetime.now().strftime('%Y%m%d_%H%M')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    
                    with c_txt:
                        st.download_button(
                            label="📝 Matn (.txt) formatida yuklash",
                            data=res_text,
                            file_name=f"LexiDraft_Hujjat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
