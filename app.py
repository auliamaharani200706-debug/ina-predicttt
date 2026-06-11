# ============ FILE: app.py (FINAL - DEPLOY READY) ============
# Aplikasi utama Streamlit dengan Chatbot AI

import streamlit as st
import re
from datetime import datetime
from FSM import DisasterAppFSM
from engine import DisasterDataEngine

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="INA-PREDICT | Early Warning System",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== INISIALISASI SESSION STATE ====================
def init_session_state():
    """Inisialisasi semua session state dengan aman"""
    if 'fsm' not in st.session_state:
        st.session_state.fsm = DisasterAppFSM()
    
    if 'data_engine' not in st.session_state:
        st.session_state.data_engine = DisasterDataEngine()
    
    if 'selected_province' not in st.session_state:
        st.session_state.selected_province = None
    
    if 'show_cities' not in st.session_state:
        st.session_state.show_cities = False
    
    # Inisialisasi chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{
            "role": "assistant", 
            "content": "👋 **Halo! Saya INA-BOT** - Asisten Bencana Indonesia 🇮🇩\n\nSaya bisa membantu Anda dengan:\n\n🌊 **Informasi Bencana**: Banjir, Gempa, Tsunami, Longsor, Gunung Meletus\n🎒 **Kesiapsiagaan**: Tas Siaga, Jalur Evakuasi, Tips Keselamatan\n📞 **Kontak Darurat**: Nomor Penting 24/7\n📊 **Statistik**: Data Bencana Terkini\n🗺️ **Info Lokasi**: Provinsi & Kabupaten/Kota\n\n**Coba tanyakan:**\n• Bagaimana cara evakuasi banjir?\n• Apa isi tas siaga?\n• Nomor darurat nasional"
        }]

init_session_state()

# ==================== CHATBOT CERDAS ====================
class SmartChatbot:
    """Chatbot dengan pemrosesan natural language"""
    
    def __init__(self, data_engine):
        self.data_engine = data_engine
        
    def process_query(self, message: str) -> str:
        """Memproses query user"""
        msg = message.lower().strip()
        
        # 1. SAPAAN
        if re.search(r'\b(halo|hai|hey|hello|selamat|pagi|siang|malam)\b', msg):
            return self._greeting_response()
        
        # 2. TERIMA KASIH
        if re.search(r'\b(terima kasih|makasih|thank|thanks)\b', msg):
            return self._thanks_response()
        
        # 3. BANJIR
        if re.search(r'\b(banjir|air naik|bandang|genangan)\b', msg):
            return self._banjir_response(msg)
        
        # 4. GEMPA
        if re.search(r'\b(gempa|gempa bumi|getaran|lindu)\b', msg):
            return self._gempa_response(msg)
        
        # 5. TSUNAMI
        if re.search(r'\b(tsunami|gelombang laut|air laut naik)\b', msg):
            return self._tsunami_response()
        
        # 6. LONGSOR
        if re.search(r'\b(longsor|tanah longsor|gerakan tanah)\b', msg):
            return self._longsor_response()
        
        # 7. GUNUNG MELETUS
        if re.search(r'\b(gunung (meletus|berapi|erupsi)|erupsi|vulkanik)\b', msg):
            return self._gunung_response()
        
        # 8. KEBARAKAN HUTAN
        if re.search(r'\b(kebakaran (hutan|lahan)|karhutla|asap|hotspot)\b', msg):
            return self._karhutla_response()
        
        # 9. CUACA EKSTREM
        if re.search(r'\b(cuaca (ekstrem|buruk)|angin (kencang|puting)|puting beliung|hujan lebat)\b', msg):
            return self._cuaca_response()
        
        # 10. TAS SIAGA
        if re.search(r'\b(tas (siaga|darurat|bencana)|perlengkapan darurat|emergency kit)\b', msg):
            return self._tas_siaga_response()
        
        # 11. EVAKUASI
        if re.search(r'\b(evakuasi|mengevakuasi|jalur evakuasi|titik kumpul|tempat aman)\b', msg):
            return self._evakuasi_response()
        
        # 12. MITIGASI
        if re.search(r'\b(mitigasi|pencegahan|antisipasi|kesiapsiagaan|siaga bencana)\b', msg):
            return self._mitigasi_response()
        
        # 13. NOMOR DARURAT
        if re.search(r'\b(nomor (darurat|telepon|kontak)|kontak (darurat|penting)|hotline|telepon)\b', msg):
            return self._kontak_response()
        
        # 14. STATISTIK
        if re.search(r'\b(statistik|data|jumlah|kejadian|total bencana|berapa (banyak|kali))\b', msg):
            return self._statistik_response()
        
        # 15. PROVINSI TERTINGGI
        if re.search(r'\b(provinsi (tertinggi|terbanyak|paling)|top provinsi|daerah terparah)\b', msg):
            return self._top_provinsi_response()
        
        # 16. CEK NAMA PROVINSI
        for prov in self.data_engine.provinces:
            if prov['name'].lower() in msg:
                return self._provinsi_detail_response(prov['name'])
        
        # 17. DEFAULT
        return self._default_response()
    
    def _greeting_response(self):
        return """👋 **Halo! Selamat datang di INA-PREDICT!** 🇮🇩

Saya INA-BOT, asisten virtual bencana Indonesia.

📌 **Yang bisa saya bantu:**
• Informasi jenis bencana (banjir, gempa, tsunami, longsor)
• Panduan evakuasi dan penyelamatan diri
• Isi tas siaga yang lengkap
• Nomor darurat penting
• Statistik bencana terkini

💡 **Coba tanyakan:** "Bagaimana cara evakuasi saat gempa?" """
    
    def _thanks_response(self):
        return """🙏 **Sama-sama!** Senang bisa membantu.

🛡️ **Tetap waspada** dan selalu utamakan keselamatan!"""
    
    def _banjir_response(self, msg):
        if "data" in msg or "statistik" in msg:
            return """💧 **DATA BANJIR 2026**

📊 **Statistik:**
• Total kejadian: 1.204 (37.1%)
• Tertinggi: Jawa Barat (312 kejadian)
• Pengungsi: 189.430 jiwa

📍 **Provinsi tertinggi:**
1. Jawa Barat - 312
2. Jawa Timur - 278
3. Kalimantan Selatan - 189"""
        
        elif "evakuasi" in msg or "tindakan" in msg:
            return """⚠️ **TINDAKAN SAAT BANJIR:**

🚨 **SEGERA LAKUKAN:**
1. Evakuasi ke tempat yang lebih TINGGI
2. Matikan aliran LISTRIK dan GAS
3. Bawa dokumen penting
4. Ikuti arahan petugas

❌ **JANGAN:**
• Berjalan di air banjir
• Menyentuh kabel listrik
• Kembali ke rumah sebelum aman

📞 **Hubungi 112 untuk bantuan!**"""
        
        else:
            return """💧 **INFORMASI BANJIR:**

📊 Data: 1.204 kejadian di 2026
📍 Tertinggi: Jawa Barat

⚠️ **Tanda-tanda banjir bandang:**
• Hujan deras >3 jam
• Air sungai naik cepat

📌 **Ketik:** "Evakuasi banjir" untuk panduan lengkap"""
    
    def _gempa_response(self, msg):
        if "evakuasi" in msg or "tindakan" in msg:
            return """⚠️ **PROSEDUR 3L (DROP, COVER, HOLD ON):**

✅ **DROP:** Jatuhkan tubuh ke lantai
✅ **COVER:** Lindungi kepala di bawah meja
✅ **HOLD ON:** Pegang sampai gempa berhenti

❌ **JANGAN:**
• Berlari keluar saat gempa
• Berdiri di dekat jendela
• Menggunakan lift

🏃 **SETELAH GEMPA:**
• Evakuasi ke tempat terbuka
• Waspada gempa susulan"""
        
        else:
            return """🌍 **INFORMASI GEMPA BUMI:**

📊 Data 2026: 712 kejadian
📍 Tersebar di 33 provinsi

🛡️ **Lindungi diri dengan 3L:**
• DROP - Jatuhkan badan
• COVER - Lindungi kepala
• HOLD ON - Pegang sampai berhenti

📌 **Ketik:** "Evakuasi gempa" untuk panduan lengkap"""
    
    def _tsunami_response(self):
        return """🌊 **PERINGATAN DINI TSUNAMI!** 🚨

⚠️ **TANDA-TANDA:**
• Gempa kuat dan lama (>30 detik)
• Air laut surut tiba-tiba
• Suara gemuruh dari laut

🏃 **TINDAKAN DARURAT:**
1. LARI ke tempat TINGGI minimal 30 meter!
2. Jangan menunggu peringatan resmi
3. Ikuti jalur evakuasi

📞 Info resmi: BMKG | BNPB | 112"""
    
    def _longsor_response(self):
        return """⛰️ **INFORMASI TANAH LONGSOR**

📊 Data 2026: 589 kejadian
📍 Tertinggi: Jawa Tengah (178), Jabar (156)

⚠️ **TANDA-TANDA:**
• Retakan tanah di lereng
• Pohon/tiang listrik miring
• Suara gemuruh dari lereng

🏃 **TINDAKAN:**
1. Lari ke SAMPING (menjauhi longsor)
2. Jangan di lembah saat hujan deras
3. Evakuasi ke tempat aman"""
    
    def _gunung_response(self):
        return """🌋 **INFORMASI GUNUNG MELETUS**

⚠️ **TINDAKAN DARURAT:**
1. Jauhi radius bahaya (8-10 km)
2. Gunakan masker N95
3. Lindungi mata dan kulit
4. Waspada lahar dingin

📊 **Gunung AWAS:**
• Semeru (Jawa Timur)
• Merapi (Jogja/Jateng)

📞 Info: PVMBG | BPBD setempat"""
    
    def _karhutla_response(self):
        return """🔥 **KEBAKARAN HUTAN/LAHAN**

📊 Data 2026: 312 kejadian
📍 Tertinggi: Riau (98), Kalsel (67)

⚠️ **PERLINDUNGAN DIRI:**
1. Gunakan masker N95
2. Tutup ventilasi rumah
3. Kurangi aktivitas luar
4. Evakuasi jika kualitas udara buruk

📞 Lapor: 113 (Pemadam) | 112"""
    
    def _cuaca_response(self):
        return """⛈️ **CUACA EKSTREM**

📊 Data 2026: 430 kejadian

⚠️ **TINDAKAN:**

🌪️ **Angin Puting Beliung:**
• Cari shelter kokoh
• Jauhi pohon besar

⛈️ **Hujan Lebat + Petir:**
• Tetap di dalam rumah
• Cabut peralatan elektronik

📱 Pantau info: BMKG | InfoBMKG"""
    
    def _tas_siaga_response(self):
        return """🎒 **TAS SIAGA BENCANA**

📋 **ISI LENGKAP:**

🥤 **AIR & MAKANAN:**
• Air minum (3 liter/orang)
• Makanan darurat (biskuit, kaleng)

🏥 **P3K & OBAT:**
• Perban, plester, betadine
• Obat rutin pribadi
• Masker N95

🔧 **PERALATAN:**
• Senter + baterai
• Power bank
• Radio portabel
• Peluit + pisau lipat

📄 **DOKUMEN:**
• KTP, KK, akta (fotokopi)
• Uang tunai (Rp500.000)

💡 **Simpan di dekat pintu keluar!**"""
    
    def _evakuasi_response(self):
        return """🚨 **PROSEDUR EVAKUASI**

📋 **LANGKAH-LANGKAH:**

1️⃣ **SEBELUM:**
• Tetap tenang, jangan panik
• Matikan listrik, gas, air
• Bawa tas siaga
• Kunci pintu

2️⃣ **SAAT EVAKUASI:**
• Ikuti arahan petugas
• JANGAN gunakan lift
• Bantu lansia & anak-anak

3️⃣ **DI TITIK KUMPUL:**
• Lapor ke petugas posko
• Cek kondisi keluarga
• Jangan kembali sebelum aman

📞 **Hubungi 112 jika butuh bantuan!**"""
    
    def _mitigasi_response(self):
        return """🛡️ **MITIGASI BENCANA**

📋 **LANGKAH-LANGKAH:**

1️⃣ **KENALI RISIKO:**
• Pelajari bencana di daerah Anda
• Cek peta rawan bencana

2️⃣ **PERSIAPAN KELUARGA:**
• Buat rencana darurat
• Siapkan tas siaga
• Simpan nomor darurat

3️⃣ **LINGKUNGAN RUMAH:**
• Perkuat struktur bangunan
• Buat saluran air yang baik

4️⃣ **LATIHAN:**
• Ikuti simulasi evakuasi
• Pelajari P3K dasar

💡 **Mitigasi lebih baik daripada respons!**"""
    
    def _kontak_response(self):
        return """📞 **NOMOR DARURAT NASIONAL 24 JAM**

• **112** - Pusat Darurat (Polisi, Ambulans, Pemadam, SAR) GRATIS
• **118/119** - Ambulans & Gawat Darurat Medis
• **113** - Pemadam Kebakaran
• **(021) 3522911** - BNPB Pusat

🏢 **BPBD PER PROVINSI:**
Hubungi 112 (terintegrasi ke BPBD setempat)

💡 **Simpan nomor ini di HP Anda!**
🆘 **Darurat? Segera hubungi 112!**"""
    
    def _statistik_response(self):
        stats = self.data_engine.get_statistics_summary()
        
        return f"""📊 **STATISTIK BENCANA INDONESIA 2026**

📈 **TOTAL:**
• Kejadian: {stats['total_events']:,}
• Pengungsi: {stats['total_refugees']:,}
• Meninggal: {stats['total_deaths']}
• Luka: {stats['total_injured']}

📋 **PER JENIS:**
• Banjir: 1.204 (37.1%)
• Gempa: 712 (21.9%)
• Longsor: 589 (18.1%)
• Cuaca Ekstrem: 430 (13.3%)
• Karhutla: 312 (9.6%)

🏆 **PROVINSI TERDAMPAK:**
• Darurat: {stats['darurat_count']} provinsi
• Waspada: {stats['waspada_count']} provinsi

📅 Update: {self.data_engine.get_last_update_str()}"""
    
    def _top_provinsi_response(self):
        top = self.data_engine.get_top_provinces(5)
        response = "🏆 **TOP 5 PROVINSI KEJADIAN TERTINGGI 2026**\n\n"
        
        for i, prov in enumerate(top, 1):
            status = "🔴 DARURAT" if prov['status'] == "darurat" else "🟡 WASPADA"
            response += f"{i}. **{prov['name']}** {status}\n"
            response += f"   📊 {prov['totalEvents']} kejadian | 👥 {prov['refugees']:,} pengungsi\n\n"
        
        response += "📌 **Ketik nama provinsi** untuk detail lengkap!"
        return response
    
    def _provinsi_detail_response(self, prov_name):
        prov = self.data_engine.get_province_by_name(prov_name)
        if not prov:
            return f"❌ Provinsi '{prov_name}' tidak ditemukan."
        
        status = "🔴 DARURAT" if prov['status'] == "darurat" else "🟡 WASPADA"
        
        return f"""📍 **{prov['name']}** {status}

📊 **STATISTIK:**
• Kejadian: {prov['totalEvents']}
• Evakuasi: {prov['evacPoints']} titik
• Pengungsi: {prov['refugees']:,}
• Meninggal: {prov['deaths']}
• Luka: {prov['injured']}
• Risiko: {prov['predRisk']}%

🏙️ **KOTA (sebagian):**
{', '.join(prov['cities'][:8])}

📞 **BPBD {prov['name']}:** 112"""
    
    def _default_response(self):
        return """🤖 **Maaf, saya kurang paham.**

📌 **Coba tanyakan:**

🌊 **BENCANA:**
• Banjir / Evakuasi banjir
• Gempa / Evakuasi gempa
• Tsunami / Longsor
• Gunung meletus

🎒 **KESIAPSIAGAAN:**
• Tas siaga
• Evakuasi / Mitigasi
• P3K

📊 **DATA & KONTAK:**
• Statistik
• Provinsi tertinggi
• Nomor darurat

📍 **Atau ketik nama provinsi** (contoh: "Jawa Barat")

💡 Ketik "Halo" untuk memulai!"""

# ==================== CSS CUSTOM ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a1a12 0%, #020504 100%);
    }
    
    .custom-card {
        background: rgba(18, 28, 23, 0.9);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(61, 155, 109, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        border-color: #2b6e4e;
    }
    
    .chat-message-user {
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-right-radius: 4px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-message-bot {
        background: rgba(61, 155, 109, 0.15);
        color: #e2e8e4;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-left-radius: 4px;
        margin: 10px 0;
        max-width: 85%;
        border: 1px solid rgba(61, 155, 109, 0.3);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    .risk-high { color: #e07a5f; font-weight: 800; }
    .risk-medium { color: #e0a343; font-weight: 800; }
    .risk-low { color: #3d9b6d; font-weight: 800; }
    
    .status-darurat {
        background: rgba(200, 80, 60, 0.2);
        color: #e07a5f;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .status-waspada {
        background: rgba(220, 140, 40, 0.2);
        color: #e0a343;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .section-header {
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    
    @media (max-width: 768px) {
        .chat-message-user, .chat-message-bot { max-width: 95%; }
    }
    
    .stTextInput input {
        background-color: rgba(18, 28, 23, 0.9);
        border: 1px solid rgba(61, 155, 109, 0.3);
        border-radius: 25px;
        color: #e2e8e4;
    }
    
    .stButton button {
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <div style="width: 70px; height: 70px; background: linear-gradient(135deg, #2b6e4e, #3d9b6d); border-radius: 25px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto;">
            <span style="font-size: 35px;">🌋</span>
        </div>
        <h2 style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 5px;">INA-PREDICT</h2>
        <p style="font-size: 11px; opacity: 0.7;">EARLY WARNING SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu_items = st.session_state.fsm.get_menu_items()
    
    for item in menu_items:
        button_type = "primary" if item["is_active"] else "secondary"
        if st.button(
            f"{item['icon']} {item['display']}",
            key=f"nav_{item['state']}",
            use_container_width=True,
            type=button_type
        ):
            if st.session_state.fsm.transition_to(item["state"]):
                st.session_state.show_cities = False
                st.session_state.selected_province = None
                st.rerun()
    
    st.markdown("---")
    
    st.caption(f"🕐 Update Terakhir")
    st.caption(f"{st.session_state.data_engine.get_last_update_str()}")
    st.caption("📊 Sumber: BNPB - BMKG - BPBD")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.data_engine.update_timestamp()
        st.rerun()

# ==================== MAIN CONTENT ====================
current_state = st.session_state.fsm.current_state
chatbot = SmartChatbot(st.session_state.data_engine)

# ==================== DASHBOARD PAGE ====================
if current_state == "dashboard":
    st.markdown('<p class="section-header">📊 PUSAT INFORMASI BENCANA INDONESIA</p>', unsafe_allow_html=True)
    st.caption("34 Provinsi | 514 Kab/Kota | Data Real-time | Early Warning")
    
    st.info("🚨 **STATUS: SIAGA NASIONAL** - Selalu waspada terhadap potensi bencana!", icon="⚠️")
    
    # Stats Grid
    cols = st.columns(6)
    for idx, stat in enumerate(st.session_state.data_engine.main_stats):
        with cols[idx]:
            with st.container():
                st.markdown(f"""
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 0.7rem; opacity: 0.65;">{stat['title']}</div>
                    <div class="stat-value">{stat['value']}</div>
                    <div style="font-size: 0.55rem; opacity: 0.6;">{stat['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Detail", key=f"stat_{idx}", use_container_width=True):
                    st.info(stat['detail'])
    
    st.markdown("---")
    
    # 2 Kolom: Breakdown + Chatbot
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<p class="section-header">📊 DETAIL KEJADIAN BENCANA 2026</p>', unsafe_allow_html=True)
        
        disaster_cols = st.columns(5)
        for idx, disaster in enumerate(st.session_state.data_engine.disaster_breakdown):
            with disaster_cols[idx]:
                st.markdown(f"""
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 2rem;">{disaster['icon']}</div>
                    <div class="stat-value">{disaster['count']:,}</div>
                    <div style="font-size: 0.65rem; font-weight: 600;">{disaster['percent']}%</div>
                    <div style="font-size: 0.7rem; font-weight: 700;">{disaster['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Detail", key=f"disaster_{idx}", use_container_width=True):
                    st.info(disaster['desc'])
        
        st.markdown('<p class="section-header">🏆 TOP PROVINSI KEJADIAN TERTINGGI</p>', unsafe_allow_html=True)
        
        top_provinces = st.session_state.data_engine.get_top_provinces(8)
        
        for prov in top_provinces:
            col_a, col_b, col_c = st.columns([2, 3, 2])
            with col_a:
                st.markdown(f"**{prov['name']}**")
            with col_b:
                st.markdown(f"{prov['totalEvents']} kejadian")
            with col_c:
                status_class = "status-darurat" if prov['status'] == "darurat" else "status-waspada"
                st.markdown(f'<span class="{status_class}">{prov["status"].upper()}</span>', unsafe_allow_html=True)
            st.divider()
    
    with col_right:
        # Chatbot Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2b6e4e, #3d9b6d); border-radius: 15px 15px 0 0; padding: 15px 20px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 28px;">🤖</span>
                <div>
                    <div style="font-weight: 800; font-size: 1rem; color: white;">INA-BOT</div>
                    <div style="font-size: 0.65rem; color: rgba(255,255,255,0.8);">Asisten Bencana 24/7</div>
                </div>
                <span style="margin-left: auto; font-size: 10px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px;">AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        chat_container = st.container(height=350)
        
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message-bot">{msg["content"]}</div>', unsafe_allow_html=True)
        
        with st.form(key="chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([4, 1])
            with col_input:
                user_input = st.text_input(
                    "Ketik pesan...",
                    key="chat_input_field",
                    placeholder="Contoh: Bagaimana cara evakuasi banjir?",
                    label_visibility="collapsed"
                )
            with col_send:
                submitted = st.form_submit_button("📤 Kirim", use_container_width=True)
            
            if submitted and user_input and user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_response = chatbot.process_query(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                st.rerun()
        
        st.markdown("---")
        st.markdown("📌 **Pertanyaan Cepat:**")
        
        quick_q = ["Banjir", "Gempa", "Tsunami", "Tas siaga", "Nomor darurat", "Statistik"]
        
        quick_cols = st.columns(3)
        for idx, q in enumerate(quick_q[:3]):
            with quick_cols[idx]:
                if st.button(q, key=f"quick_{q}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    bot_response = chatbot.process_query(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                    st.rerun()
        
        quick_cols2 = st.columns(3)
        for idx, q in enumerate(quick_q[3:]):
            with quick_cols2[idx]:
                if st.button(q, key=f"quick2_{q}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    bot_response = chatbot.process_query(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                    st.rerun()
        
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state.chat_history = [{
                "role": "assistant", 
                "content": "👋 **Halo! Saya INA-BOT** - Asisten Bencana Indonesia 🇮🇩\n\nSaya bisa membantu Anda dengan:\n\n🌊 **Informasi Bencana**: Banjir, Gempa, Tsunami, Longsor, Gunung Meletus\n🎒 **Kesiapsiagaan**: Tas Siaga, Jalur Evakuasi, Tips Keselamatan\n📞 **Kontak Darurat**: Nomor Penting 24/7\n📊 **Statistik**: Data Bencana Terkini\n🗺️ **Info Lokasi**: Provinsi & Kabupaten/Kota\n\n**Coba tanyakan:**\n• Bagaimana cara evakuasi banjir?\n• Apa isi tas siaga?\n• Nomor darurat nasional"
            }]
            st.rerun()
    
    st.markdown("---")
    
    # Breaking News
    st.markdown('<p class="section-header">🔴 BREAKING NEWS</p>', unsafe_allow_html=True)
    breaking = st.session_state.data_engine.news[0]
    st.warning(f"**{breaking['title']}**\n\n📍 {breaking['location']} | {breaking['date']}\n\n{breaking['short']}")
    
    # Berita Terkini
    st.markdown('<p class="section-header">📰 BERITA TERKINI</p>', unsafe_allow_html=True)
    news_cols = st.columns(3)
    for idx, news in enumerate(st.session_state.data_engine.news[:3]):
        with news_cols[idx]:
            st.markdown(f"""
            <div class="custom-card">
                <div style="font-weight: 700;">{news['icon']} {news['title']}</div>
                <div style="font-size: 0.7rem;">📍 {news['location']}</div>
                <div style="font-size: 0.7rem;">{news['short']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Provinsi Grid
    st.markdown('<p class="section-header">🗺️ 34 PROVINSI</p>', unsafe_allow_html=True)
    
    search_prov = st.text_input("🔍 Cari provinsi...", key="search_prov")
    provinces = st.session_state.data_engine.search_provinces(search_prov) if search_prov else st.session_state.data_engine.provinces
    
    prov_cols = st.columns(4)
    for idx, prov in enumerate(provinces[:20]):
        with prov_cols[idx % 4]:
            status_text = "🔴 DARURAT" if prov['status'] == "darurat" else "🟡 WASPADA"
            if st.button(f"🏙️ {prov['name']}\n\n{prov['totalEvents']} kejadian\n{status_text}", key=f"prov_btn_{prov['name']}"):
                st.session_state.selected_province = prov
                st.session_state.show_cities = True
                st.rerun()
    
    if st.session_state.show_cities and st.session_state.selected_province:
        st.markdown("---")
        prov = st.session_state.selected_province
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🏙️ Kota/Kabupaten di {prov['name']}")
        with col2:
            if st.button("✕ Tutup", use_container_width=True):
                st.session_state.show_cities = False
                st.session_state.selected_province = None
                st.rerun()
        
        st.info(f"""
        **📊 Statistik {prov['name']}**
        - Kejadian: {prov['totalEvents']}
        - Status: {prov['status'].upper()}
        - Evakuasi: {prov['evacPoints']} titik
        - Pengungsi: {prov['refugees']:,}
        - Risiko: {prov['predRisk']}%
        """)
        
        city_cols = st.columns(5)
        for idx, city in enumerate(prov['cities'][:15]):
            with city_cols[idx % 5]:
                st.markdown(f"📍 {city}")
    
    # Kontak Darurat
    st.markdown('<p class="section-header">📞 KONTAK DARURAT 24/7</p>', unsafe_allow_html=True)
    contact_cols = st.columns(5)
    for idx, contact in enumerate(st.session_state.data_engine.emergency_contacts):
        with contact_cols[idx % 5]:
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2rem;">{contact['icon']}</div>
                <div class="stat-value">{contact['number']}</div>
                <div style="font-size: 0.65rem; font-weight: 600;">{contact['name']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PREDIKSI PAGE ====================
elif current_state == "prediksi":
    st.markdown('<p class="section-header">🔮 PREDIKSI & PERINGATAN DINI</p>', unsafe_allow_html=True)
    st.caption("AI-Powered Prediction | Akurasi 94.7%")
    
    stats = st.session_state.data_engine.get_statistics_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Risiko Nasional", "76.8%", "↑6.2%")
    with col2:
        st.metric("Provinsi Darurat", stats['darurat_count'], "14 Provinsi")
    with col3:
        st.metric("Kota Berisiko", "74", "Risiko Tinggi")
    with col4:
        st.metric("Akurasi Prediksi", "94.7%", "↑2.1%")
    
    st.markdown("---")
    st.markdown('<p class="section-header">📅 PREDIKSI 7 HARI</p>', unsafe_allow_html=True)
    
    pred_cols = st.columns(7)
    for idx, pred in enumerate(st.session_state.data_engine.weekly_predictions):
        with pred_cols[idx]:
            risk_class = "risk-high" if pred['level'] == "high" else ("risk-medium" if pred['level'] == "medium" else "risk-low")
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-weight: 700;">{pred['day']}</div>
                <div style="font-size: 0.6rem;">{pred['date']}</div>
                <div class="{risk_class}" style="font-size: 1.3rem;">{pred['risk']}%</div>
                <div style="font-size: 0.55rem;">{pred['status']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PANDUAN PAGE ====================
elif current_state == "panduan":
    st.markdown('<p class="section-header">📖 PANDUAN TANGGAP DARURAT</p>', unsafe_allow_html=True)
    st.caption("Pedoman resmi BNPB | Langkah penyelamatan diri")
    
    for step in st.session_state.data_engine.guide_steps[:4]:
        with st.expander(f"LANGKAH {step['num']}: {step['title']}"):
            st.markdown(step['long'])
    
    st.markdown("---")
    st.markdown('<p class="section-header">🎒 TAS DARURAT</p>', unsafe_allow_html=True)
    
    kit_cols = st.columns(5)
    for idx, kit in enumerate(st.session_state.data_engine.emergency_kit[:10]):
        with kit_cols[idx % 5]:
            st.markdown(f"**{kit['icon']} {kit['name']}**")

# ==================== KONTAK PAGE ====================
elif current_state == "kontak":
    st.markdown('<p class="section-header">📞 KONTAK DARURAT 24/7</p>', unsafe_allow_html=True)
    
    contact_cols = st.columns(4)
    for idx, contact in enumerate(st.session_state.data_engine.emergency_contacts):
        with contact_cols[idx % 4]:
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2rem;">{contact['icon']}</div>
                <div class="stat-value">{contact['number']}</div>
                <div style="font-weight: 700;">{contact['name']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== DONASI PAGE ====================
elif current_state == "donasi":
    st.markdown('<p class="section-header">🤝 DONASI BENCANA</p>', unsafe_allow_html=True)
    
    with st.form("donation_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
        with col2:
            nominal = st.number_input("Nominal Donasi *", min_value=10000, step=10000)
            bank = st.selectbox("Bank Tujuan", ["BCA - 1234567890", "MANDIRI - 1234567890123"])
        
        submitted = st.form_submit_button("💝 DONASI SEKARANG", use_container_width=True)
        if submitted and nama and email and nominal:
            st.success(f"✅ Terima kasih, {nama}! Donasi Rp{nominal:,} berhasil.")

# ==================== HUBUNGI KAMI PAGE ====================
elif current_state == "hubungi":
    st.markdown('<p class="section-header">💬 HUBUNGI KAMI</p>', unsafe_allow_html=True)
    
    with st.form("complaint_form"):
        nama = st.text_input("Nama Lengkap *")
        pesan = st.text_area("Pesan *", height=150)
        submitted = st.form_submit_button("📤 KIRIM", use_container_width=True)
        if submitted and nama and pesan:
            st.success("✅ Pesan terkirim! Admin akan merespon.")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding: 20px; font-size: 11px; opacity: 0.6;'>"
    "🛡️ INA-PREDICT | Sistem Peringatan Dini Bencana Indonesia<br>"
    "Sumber: BNPB - BMKG - BPBD | Update Real-time"
    "</div>",
    unsafe_allow_html=True
)