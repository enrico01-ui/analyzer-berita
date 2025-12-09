import streamlit as st
from openai import OpenAI
from typing import Dict
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="News Bias Analyzer",
    page_icon="📰",
    layout="wide"
)

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ API Key belum disetting di Streamlit Secrets!")
    st.stop()

# Inisialisasi OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_bias(text: str) -> Dict:
    """
    Analisis bias menggunakan OpenAI API
    """
    try:
        prompt = f"""Analisis teks berita berikut untuk mendeteksi bias:

"{text}"

Berikan analisis dalam format berikut:
1. Klasifikasi Bias: [Positif/Negatif/Netral/Berimbang]
2. Alasan: [Penjelasan detail mengapa teks memiliki bias tersebut]
3. Loaded Words: [Daftar kata-kata bermuatan yang ditemukan]
4. Framing: [Bagaimana berita di-frame]
5. Skor Bias: [0-100, dimana 0=sangat negatif, 50=netral, 100=sangat positif]

Fokus pada:
- Pemilihan kata yang menunjukkan bias
- Framing dan sudut pandang
- Keseimbangan perspektif
- Objektivitas penyajian"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Anda adalah ahli analisis bias media yang objektif dan teliti."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return {
            "status": "success",
            "result": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Header
st.title("📰 Analyzer Teks Berita untuk Deteksi Bias")
st.markdown("**Menggunakan OpenAI API**")
st.markdown("*Emanuel Enrico Anindya Wibawa (220711890) & Davin Gilbert Natanael (220711841)*")
st.divider()

# Sidebar untuk informasi
with st.sidebar:
    st.header("ℹ️ Informasi Proyek")
    st.markdown("""
    ### Tentang Sistem
    Sistem ini menganalisis teks berita untuk mendeteksi bias menggunakan AI.
    
    ### Fitur:
    - ✅ Klasifikasi Bias
    - ✅ Analisis Alasan
    - ✅ Deteksi Loaded Words
    - ✅ Analisis Framing
    - ✅ Scoring (0-100)
    
    ### Cara Penggunaan:
    1. Masukkan teks berita
    2. Klik "Analisis Bias"
    3. Lihat hasil analisis
    """)
    
    st.divider()
    
   

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Analisis", "📚 Dokumentasi", "💻 Source Code"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Teks Berita")
        
        # Contoh teks
        examples = {
            "Pilih contoh...": "",
            "Berita Positif": "Ekonom memuji langkah pemerintah yang dianggap mampu menstabilkan harga pangan dan meningkatkan kesejahteraan petani.",
            "Berita Negatif": "Pemerintah kembali menuai kritik setelah mengumumkan kebijakan baru yang dianggap kontroversial oleh berbagai kalangan.",
            "Berita Netral": "Pemerintah mengumumkan kebijakan baru terkait tata kelola ekonomi digital yang akan berlaku mulai tahun depan."
        }
        
        selected_example = st.selectbox("Atau gunakan contoh:", list(examples.keys()))
        
        news_text = st.text_area(
            "Masukkan teks berita:",
            value=examples[selected_example],
            height=200,
            placeholder="Ketik atau paste teks berita di sini..."
        )
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            analyze_button = st.button("🔍 Analisis Bias", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.rerun()
    
    with col2:
        st.subheader("Hasil Analisis")
        
        if analyze_button:
            if not news_text.strip():
                st.error("❌ Mohon masukkan teks berita terlebih dahulu!")
            elif not openai.api_key:
                st.error("❌ Mohon masukkan OpenAI API Key di sidebar!")
            else:
                with st.spinner("🔄 Menganalisis teks..."):
                    result = analyze_bias(news_text)
                    
                    if result["status"] == "success":
                        st.success("✅ Analisis selesai!")
                        
                        # Parse hasil (simplified)
                        analysis_text = result["result"]
                        
                        # Tampilkan hasil
                        st.markdown("### 📊 Hasil Lengkap:")
                        st.info(analysis_text)
                        
                        # Metrics
                        st.divider()
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("Jumlah Kata", len(news_text.split()))
                        with col_m2:
                            st.metric("Token Terpakai", result["tokens_used"])
                        
                    else:
                        st.error(f"❌ Error: {result['message']}")
        else:
            st.info("👈 Masukkan teks berita dan klik 'Analisis Bias' untuk memulai")

with tab2:
    st.header("📚 Dokumentasi Proyek")
    
    st.markdown("""
    ## 1. Deskripsi Proyek
    Proyek ini mengembangkan sistem analyzer teks berita yang mampu mendeteksi bias 
    menggunakan OpenAI API. Sistem menerima input berupa teks berita dan mengembalikan 
    klasifikasi bias beserta alasan analisisnya.
    
    ## 2. Arsitektur Sistem
    ```
    User Interface (Streamlit) → OpenAI API → Hasil Analisis
    ```
    
    ## 3. Fitur Utama
    - **Klasifikasi Bias**: Positif, Negatif, Netral, atau Berimbang
    - **Analisis Alasan**: Penjelasan detail mengapa teks memiliki bias tersebut
    - **Deteksi Loaded Words**: Identifikasi kata-kata bermuatan emosional
    - **Analisis Framing**: Bagaimana informasi disajikan
    - **Scoring**: Nilai kuantitatif tingkat bias (0-100)
    
    ## 4. Metodologi
    Sistem menggunakan GPT-4-turbo untuk:
    1. Analisis semantik mendalam
    2. Deteksi pemilihan kata yang bias
    3. Evaluasi keseimbangan perspektif
    4. Penilaian objektivitas
    
    ## 5. Teknologi
    - **Frontend**: Streamlit (Python)
    - **AI Engine**: OpenAI GPT-4-turbo
    - **Language**: Python 3.8+
    
    ## 6. Pengembangan Selanjutnya
    - Export hasil ke PDF/CSV
    - Batch processing multiple articles
    - Historical analysis
    - Advanced NLP metrics
    """)

with tab3:
    st.header("💻 Source Code")
    
    st.markdown("### requirements.txt")
    st.code("""streamlit==1.29.0
openai==1.3.0
python-dotenv==1.0.0""", language="text")
    
    st.markdown("### Cara Menjalankan")
    st.code("""# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# 3. Run aplikasi
streamlit run app.py

# 4. Buka browser di http://localhost:8501""", language="bash")
    
    st.markdown("### API Integration Code")
    st.code("""import openai

def analyze_bias(text: str):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Anda ahli analisis bias media"},
            {"role": "user", "content": f"Analisis bias: {text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content""", language="python")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Tugas Kapita Selekta B - Sistem Deteksi Bias Berita</p>
    <p>Emanuel Enrico (220711890) & Davin Gilbert (220711841)</p>
</div>
""", unsafe_allow_html=True)
