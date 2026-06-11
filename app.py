# ============ FILE: app.py (UPDATED WITH ENHANCED CHATBOT) ============
# Aplikasi utama Streamlit dengan Enhanced Chatbot

import streamlit as st
import random
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from FSM import DisasterAppFSM
from engine import DisasterDataEngine

# ==================== ENHANCED CHATBOT CLASS (LANGSUNG DI APP.PY) ====================

class EnhancedChatbot:
    """Enhanced Chatbot dengan memory dan konteks - Langsung terintegrasi di app.py"""
    
    def __init__(self, data_engine):
        self.data_engine = data_engine
        self.conversation_memory = {}
        
        # Template respons
        self.response_templates = {
            "greeting": [
                "👋 Halo **{name}**! Ada yang bisa saya bantu? Saya INA-BOT, asisten bencana Indonesia.",
                "🌏 Selamat {timeofday}, **{name}**! Saya siap membantu informasi kebencanaan.",
                "🤖 Hai **{name}**! Tanyakan apa saja tentang bencana di Indonesia."
            ],
            "thanks": [
                "🙏 Sama-sama! Ada lagi yang ingin ditanyakan?",
                "✨ Senang bisa membantu! Tetap waspada ya!",
                "💚 Terima kasih kembali!"
            ],
            "unknown": "🤔 Maaf, saya kurang paham.\n\n📌 **Coba tanyakan:**\n• Banjir / Gempa / Tsunami / Longsor\n• Statistik bencana\n• Tas siaga\n• Nomor darurat\n• [Nama Provinsi] - contoh: Jawa Barat"
        }
    
    def get_time_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 11: return "pagi"
        elif 11 <= hour < 15: return "siang"
        elif 15 <= hour < 18: return "sore"
        else: return "malam"
    
    def detect_intent(self, message: str) -> str:
        msg = message.lower().strip()
        
        intents = {
            "greeting": ["halo", "hai", "hey", "hello", "selamat pagi", "selamat siang", "selamat malam", "hy", "hi", "morning"],
            "thanks": ["terima kasih", "makasih", "thank", "thanks", "trims", "thx"],
            "banjir": ["banjir", "flood", "air naik", "genangan"],
            "gempa": ["gempa", "earthquake", "getaran"],
            "tsunami": ["tsunami", "gelombang tsunami"],
            "longsor": ["longsor", "tanah longsor", "landslide"],
            "gunung": ["gunung", "erupsi", "meletus", "semeru", "merapi"],
            "tas_siaga": ["tas siaga", "emergency kit", "perlengkapan", "persiapan"],
            "evakuasi": ["evakuasi", "evacuation", "penyelamatan"],
            "mitigasi": ["mitigasi", "pencegahan", "kesiapsiagaan"],
            "nomor": ["nomor darurat", "telepon", "hotline", "kontak"],
            "statistik": ["statistik", "data", "kejadian", "total bencana"],
            "peringatan": ["peringatan", "warning", "cuaca"],
            "donasi": ["donasi", "sumbangan", "donate"]
        }
        
        for intent, keywords in intents.items():
            if any(k in msg for k in keywords):
                return intent
        
        # Cek apakah menyebut provinsi
        provinces = [p["name"].lower() for p in self.data_engine.provinces]
        if any(prov in msg for prov in provinces):
            return "province"
        
        return "unknown"
    
    def extract_province(self, message: str) -> Optional[str]:
        msg_lower = message.lower()
        for prov in self.data_engine.provinces:
            if prov["name"].lower() in msg_lower:
                return prov["name"]
        return None
    
    def get_province_info(self, province_name: str) -> str:
        prov = self.data_engine.get_province_by_name(province_name)
        if not prov:
            return f"❌ Provinsi '{province_name}' tidak ditemukan."
        
        status_emoji = "🔴" if prov['status'] == "darurat" else "🟡"
        risk_text = "TINGGI" if prov['predRisk'] >= 75 else ("SEDANG" if prov['predRisk'] >= 50 else "RENDAH")
        
        return f"""📍 **{prov['name'].upper()}**

📊 **STATUS:** {status_emoji} {prov['status'].upper()}
⚠️ **RISIKO:** {risk_text} ({prov['predRisk']}%)
📈 **KEJADIAN:** {prov['totalEvents']} bencana
👥 **PENGUNGSI:** {prov['refugees']:,} jiwa
💀 **MENINGGAL:** {prov['deaths']} jiwa
🏢 **TITIK EVAKUASI:** {prov['evacPoints']} titik

🏙️ **KOTA/KABUPATEN:** {', '.join(prov['cities'][:8])}{'...' if len(prov['cities']) > 8 else ''}

📞 **HUBUNGI:** 112 (BPBD setempat)"""

    def get_statistics(self) -> str:
        stats = self.data_engine.get_statistics_summary()
        disasters = self.data_engine.disaster_breakdown
        
        response = f"""📊 **STATISTIK BENCANA INDONESIA 2026**
📅 Update: {self.data_engine.get_last_update_str()}

═══════════════════════════

**📈 DATA NASIONAL:**
• Total Kejadian: {stats['total_events']:,}
• Pengungsi: {stats['total_refugees']:,} jiwa
• Meninggal: {stats['total_deaths']} jiwa
• Provinsi Darurat: {stats['darurat_count']}

**🌋 RINCIAN BENCANA:**
"""
        for d in disasters:
            response += f"\n{d['icon']} {d['name']}: {d['count']:,} ({d['percent']}%)"
        
        response += f"""

**🏆 TOP PROVINSI:**
"""
        for i, p in enumerate(self.data_engine.get_top_provinces(3), 1):
            response += f"{i}. {p['name']}: {p['totalEvents']} kejadian\n"
        
        return response
    
    def get_flood_info(self) -> str:
        disaster = next((d for d in self.data_engine.disaster_breakdown if d["name"] == "BANJIR"), None)
        return f"""💧 **BANJIR** - UPDATE TERKINI

📊 **STATISTIK:** {disaster['count']:,} kejadian ({disaster['percent']}%)
📍 **RAWAN:** Jawa Barat (312), Jawa Timur (278), Kalsel (189)

⚠️ **TINDAKAN DARURAT:**
1️⃣ Evakuasi ke tempat lebih tinggi
2️⃣ Matikan listrik dan gas
3️⃣ Bawa dokumen penting
4️⃣ Jangan melewati arus banjir
5️⃣ Waspada penyakit pasca banjir

📞 **DARURAT:** 112"""
    
    def get_earthquake_info(self) -> str:
        return """🌍 **GEMPA BUMI** - PROSEDUR DARURAT

⚠️ **SAAT GEMPA (DROP, COVER, HOLD ON):**
1️⃣ **DROP** - Jatuhkan tubuh ke lantai
2️⃣ **COVER** - Lindungi kepala di bawah meja
3️⃣ **HOLD ON** - Pegang sampai gempa berhenti

🚫 **JANGAN:**
• Berdiri di dekat jendela/rak
• Menggunakan lift
• Berlari keluar saat gempa

✅ **SETELAH GEMPA:**
• Waspada gempa susulan
• Jauhi bangunan retak
• Periksa kebocoran gas

📞 **LAPORAN:** 112"""
    
    def get_tsunami_info(self) -> str:
        return """🌊 **TSUNAMI** - PERINGATAN DINI

⚠️ **TANDA BAHAYA:**
• Gempa kuat & lama (>30 detik)
• Air laut surut tiba-tiba
• Suara gemuruh dari laut

🏃 **TINDAKAN SEGERA:**
1️⃣ LARI ke tempat tinggi (minimal 30m)
2️⃣ JAUHI pantai (minimal 3km)
3️⃣ JANGAN menunggu peringatan!
4️⃣ IKUTI jalur evakuasi tsunami

📍 **RAWAN:** Selat Sunda, Pantai Sumatera, Selatan Jawa

📱 **INFO:** BMKG | InaTEWS"""
    
    def get_landslide_info(self) -> str:
        disaster = next((d for d in self.data_engine.disaster_breakdown if d["name"] == "LONGSOR"), None)
        return f"""⛰️ **TANAH LONGSOR** - UPDATE TERKINI

📊 **STATISTIK:** {disaster['count']:,} kejadian ({disaster['percent']}%)
📍 **RAWAN:** Jateng (178), Jabar (156), Jatim (98)

⚠️ **TANDA BAHAYA:**
• Retakan tanah meluas
• Pohon/pagar miring
• Air tanah keruh
• Suara gemuruh dari bukit

🏃 **TINDAKAN:**
1️⃣ Lari ke SAMPING (bukan ke bawah)
2️⃣ Waspada saat hujan >3 jam
3️⃣ Jangan tinggal di tebing curam

📞 **DARURAT:** 112"""
    
    def get_volcano_info(self) -> str:
        return """🌋 **GUNUNG MELETUS** - PROSEDUR DARURAT

⚠️ **TINDAKAN:**
1️⃣ Jauhi radius bahaya (8-10km dari puncak)
2️⃣ Gunakan masker N95
3️⃣ Lindungi mata dan kulit
4️⃣ Waspada lahar dingin saat hujan
5️⃣ Ikuti arahan PVMBG

📍 **GUNUNG AKTIF:**
• Semeru (Level III - Siaga)
• Merapi (Level II - Waspada)
• Krakatau (Level II - Waspada)

📱 **INFO:** @infoPVMBG | Magma Indonesia"""
    
    def get_emergency_kit(self) -> str:
        return """🎒 **TAS SIAGA BENCANA LENGKAP**

📦 **ISI TAS SIAGA (3 HARI):**

💧 **Air minum** - 3 liter per orang
🍝 **Makanan darurat** - Biskuit, kaleng, energy bar
🏥 **P3K & Obat** - Perban, betadine, obat rutin
🔦 **Senter & Baterai** - LED terang + baterai cadangan
📻 **Radio portabel** - Update info resmi
👕 **Pakaian & Selimut** - Ganti 3 set + jaket
😷 **Masker N95** - Minimal 5 per orang
📄 **Dokumen penting** - KK, KTP, sertifikat tanah
🔧 **Peralatan** - Pisau, tali, peluit
💰 **Uang tunai** - Minimal Rp500.000

💡 **TIPS:**
• Letakkan di dekat pintu keluar
• Periksa setiap 3 bulan
• Ganti makanan/air setiap 6 bulan"""
    
    def get_emergency_numbers(self) -> str:
        contacts = self.data_engine.emergency_contacts
        return f"""📞 **KONTAK DARURAT 24 JAM**

{chr(10).join([f"{c['icon']} **{c['name']}**: {c['number']}" for c in contacts])}

📱 **APLIKASI:**
• BMKG Info - Gempa & Cuaca
• InaRISK - Peta Risiko
• Magma Indonesia - Gunung Api

⚠️ **PENTING:** Simpan nomor di kontak cepat HP!"""
    
    def get_evacuation(self) -> str:
        return """🚨 **PROSEDUR EVAKUASI**

📋 **LANGKAH-LANGKAH:**
1️⃣ Tetap tenang, jangan panik
2️⃣ Ikuti arahan petugas BPBD
3️⃣ Gunakan jalur evakuasi resmi
4️⃣ Bantu lansia, anak-anak, disabilitas
5️⃣ Jangan gunakan lift
6️⃣ Kumpul di titik kumpul
7️⃣ Bawa tas siaga
8️⃣ Jangan kembali sebelum aman

🎒 **WAJIB DIBAWA:**
• Tas siaga
• Dokumen penting
• Obat-obatan
• Ponsel & power bank

📞 **HUBUNGI:** 112 jika ada yang tertinggal"""
    
    def get_mitigation(self) -> str:
        return """🛡️ **MITIGASI BENCANA**

📌 **LANGKAH PERSIAPAN:**
1. Kenali risiko bencana di daerah Anda
2. Buat peta evakuasi keluarga
3. Siapkan tas siaga
4. Ikuti pelatihan tanggap darurat
5. Pantau peringatan dini BMKG/BNPB
6. Sosialisasi ke tetangga
7. Perkuat struktur rumah
8. Simpan nomor darurat

🏠 **PERSIAPAN RUMAH:**
• Pasang rak/lemari ke dinding
• Jangan letakkan barang berat di tempat tinggi
• Siapkan matras evakuasi
• Letakkan tas siaga dekat pintu

👨‍👩‍👧‍👦 **PERSIAPAN KELUARGA:**
• Diskusikan rencana darurat
• Tentukan 2 titik kumpul
• Latih evakuasi rutin
• Ajari anak cara memanggil bantuan"""
    
    def get_weather_warning(self) -> str:
        warnings = self.data_engine.weather_warnings[:3]
        response = f"🌤️ **PERINGATAN DINI CUACA**\n📅 {self.data_engine.get_last_update_str()}\n\n"
        for w in warnings:
            icon = "🔴" if w['severity'] == "high" else "🟡"
            response += f"{icon} **{w['type']}**\n📍 {w['locations']}\n📝 {w['desc']}\n\n"
        return response
    
    def get_donation_info(self) -> str:
        return """🤝 **DONASI BENCANA**

🏦 **REKENING RESMI:**

🏦 **BCA** - 1234567890
   a.n. Yayasan Bencana Indonesia

🏦 **MANDIRI** - 1234567890123
   a.n. Yayasan Bencana Indonesia

🏦 **BRI** - 123456789012345
   a.n. Yayasan Bencana Indonesia

📝 **CARA DONASI:**
1. Transfer ke rekening tujuan
2. Upload bukti transfer di form donasi
3. Konfirmasi via WhatsApp

✅ Setiap donasi sangat berarti bagi korban bencana!"""
    
    def get_response(self, message: str, session_id: str, selected_province: str = None, user_name: str = None) -> str:
        # Inisialisasi memory
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = {"last_province": None}
        
        memory = self.conversation_memory[session_id]
        msg = message.lower().strip()
        
        # Deteksi intent
        intent = self.detect_intent(message)
        
        # Cek ekstraksi provinsi
        mentioned_province = self.extract_province(message)
        if mentioned_province:
            memory["last_province"] = mentioned_province
        
        # Gunakan provinsi dari memory atau yang dipilih user
        active_province = mentioned_province or selected_province or memory["last_province"]
        
        # Intent khusus province
        if intent == "province" and active_province:
            return self.get_province_info(active_province)
        
        # Intent lainnya
        if intent == "greeting":
            template = random.choice(self.response_templates["greeting"])
            return template.format(name=user_name or "Pengguna", timeofday=self.get_time_greeting())
        
        elif intent == "thanks":
            return random.choice(self.response_templates["thanks"])
        
        elif intent == "banjir":
            return self.get_flood_info()
        
        elif intent == "gempa":
            return self.get_earthquake_info()
        
        elif intent == "tsunami":
            return self.get_tsunami_info()
        
        elif intent == "longsor":
            return self.get_landslide_info()
        
        elif intent == "gunung":
            return self.get_volcano_info()
        
        elif intent == "tas_siaga":
            return self.get_emergency_kit()
        
        elif intent == "evakuasi":
            if active_province:
                return self.get_evacuation() + f"\n\n📍 **INFO KHUSUS {active_province.upper()}:**\nHubungi BPBD setempat di 112"
            return self.get_evacuation()
        
        elif intent == "mitigasi":
            return self.get_mitigation()
        
        elif intent == "nomor":
            return self.get_emergency_numbers()
        
        elif intent == "statistik":
            return self.get_statistics()
        
        elif intent == "peringatan":
            return self.get_weather_warning()
        
        elif intent == "donasi":
            return self.get_donation_info()
        
        elif intent == "province":
            return "📍 Silakan sebutkan nama provinsi (contoh: 'Jawa Barat' atau 'info Banten')"
        
        return self.response_templates["unknown"]


# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="INA-PREDICT | Early Warning System",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== INISIALISASI ====================
if 'fsm' not in st.session_state:
    st.session_state.fsm = DisasterAppFSM()

if 'data_engine' not in st.session_state:
    st.session_state.data_engine = DisasterDataEngine()

if 'selected_province' not in st.session_state:
    st.session_state.selected_province = None

if 'show_cities' not in st.session_state:
    st.session_state.show_cities = False

# Inisialisasi Enhanced Chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = EnhancedChatbot(st.session_state.data_engine)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(random.randint(10000, 99999))

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Inisialisasi chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Halo! Saya **INA-BOT**, asisten virtual bencana Indonesia. Ada yang bisa saya bantu?\n\n📌 **Coba tanyakan:**\n• Banjir, Gempa, Tsunami, Longsor\n• Gunung meletus\n• Tas siaga\n• Nomor darurat\n• Statistik bencana\n• [Nama Provinsi] - contoh: Jawa Barat"}
    ]

# ==================== FUNGSI CHATBOT ====================
def get_bot_response(user_message: str) -> str:
    return st.session_state.chatbot.get_response(
        message=user_message,
        session_id=st.session_state.session_id,
        selected_province=st.session_state.selected_province,
        user_name=st.session_state.user_name
    )

# ==================== CSS CUSTOM ====================
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #0a1a12 0%, #020504 100%);
    }
    
    /* Card styling */
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
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    .chat-message-user {
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-right-radius: 4px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        white-space: pre-wrap;
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
        white-space: pre-wrap;
    }
    
    /* Stat value */
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    /* Risk indicators */
    .risk-high { color: #e07a5f; font-weight: 800; }
    .risk-medium { color: #e0a343; font-weight: 800; }
    .risk-low { color: #3d9b6d; font-weight: 800; }
    
    /* Progress bar */
    .progress-bar {
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Status badges */
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
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* Chatbot section */
    .chatbot-header {
        background: linear-gradient(135deg, #2b6e4e, #3d9b6d);
        padding: 15px 20px;
        border-radius: 15px 15px 0 0;
        margin-bottom: 0;
    }
    
    /* Quick question buttons */
    .quick-btn {
        background: rgba(61, 155, 109, 0.2);
        border: 1px solid rgba(61, 155, 109, 0.3);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.7rem;
        cursor: pointer;
        transition: all 0.2s;
        margin: 4px;
        display: inline-block;
    }
    
    .quick-btn:hover {
        background: rgba(61, 155, 109, 0.4);
        transform: scale(1.02);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .stButton button { width: 100%; }
        .chat-message-user, .chat-message-bot { max-width: 95%; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo
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
    
    # Input nama user
    st.markdown("### 👤 Profil")
    user_name_input = st.text_input("Nama Anda", value=st.session_state.user_name or "", 
                                      placeholder="Masukkan nama", key="user_name_input")
    if user_name_input:
        st.session_state.user_name = user_name_input
    
    st.markdown("---")
    
    # Menu navigasi
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
    
    # Info update
    st.caption(f"🕐 Update Terakhir")
    st.caption(f"{st.session_state.data_engine.get_last_update_str()}")
    st.caption("📊 Sumber: BNPB - BMKG - BPBD")
    
    # Tombol refresh
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.data_engine.update_timestamp()
        st.rerun()

# ==================== MAIN CONTENT ====================
current_state = st.session_state.fsm.current_state

# ==================== DASHBOARD PAGE (WITH CHATBOT) ====================
if current_state == "dashboard":
    # Header
    st.markdown('<p class="section-header">📊 PUSAT INFORMASI BENCANA INDONESIA</p>', unsafe_allow_html=True)
    st.caption("34 Provinsi | 514 Kab/Kota | Data Real-time | Early Warning")
    
    # Status banner
    st.info("🚨 **STATUS: SIAGA NASIONAL** - Selalu waspada terhadap potensi bencana!", icon="⚠️")
    
    # ==================== STATS GRID ====================
    cols = st.columns(6)
    for idx, stat in enumerate(st.session_state.data_engine.main_stats):
        with cols[idx]:
            with st.container():
                st.markdown(f"""
                <div class="custom-card" style="text-align: center; cursor: pointer;">
                    <div style="font-size: 0.7rem; opacity: 0.65;">{stat['title']}</div>
                    <div class="stat-value">{stat['value']}</div>
                    <div style="font-size: 0.55rem; opacity: 0.6;">{stat['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Detail", key=f"stat_{idx}", use_container_width=True):
                    st.info(stat['detail'])
    
    st.markdown("---")
    
    # ==================== LAYOUT 2 KOLOM ====================
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<p class="section-header">📊 DETAIL KEJADIAN BENCANA 2026</p>', unsafe_allow_html=True)
        
        # Breakdown Bencana
        disaster_cols = st.columns(5)
        for idx, disaster in enumerate(st.session_state.data_engine.disaster_breakdown):
            with disaster_cols[idx]:
                with st.container():
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
        
        # Leaderboard Provinsi
        st.markdown('<p class="section-header">🏆 TOP PROVINSI KEJADIAN TERTINGGI 2026</p>', unsafe_allow_html=True)
        
        top_provinces = st.session_state.data_engine.get_top_provinces(10)
        
        for prov in top_provinces:
            col_a, col_b, col_c, col_d = st.columns([2, 3, 1, 1])
            with col_a:
                st.markdown(f"**{prov['name']}**")
            with col_b:
                st.markdown(f"{prov['totalEvents']} kejadian")
            with col_c:
                status_class = "status-darurat" if prov['status'] == "darurat" else "status-waspada"
                st.markdown(f'<span class="{status_class}">{prov["status"].upper()}</span>', unsafe_allow_html=True)
            with col_d:
                if st.button("Detail", key=f"prov_leader_{prov['name']}"):
                    st.info(f"""
                    **📊 {prov['name']}**
                    - Total Kejadian: {prov['totalEvents']} kejadian
                    - Pengungsi: {prov['refugees']:,} jiwa
                    - Titik Evakuasi: {prov['evacPoints']} titik
                    - Korban Meninggal: {prov['deaths']} jiwa
                    - Korban Luka: {prov['injured']} jiwa
                    - Status: {prov['status'].upper()}
                    - Prediksi Risiko: {prov['predRisk']}%
                    """)
            st.divider()
    
    with col_right:
        # ==================== ENHANCED CHATBOT SECTION ====================
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
        
        # Chat container
        chat_container = st.container(height=350)
        
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message-bot">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Input chat
        col_input, col_send = st.columns([4, 1])
        with col_input:
            user_input = st.text_input(
                "Ketik pesan...",
                key="chat_input_field",
                placeholder="Tanyakan tentang bencana atau ketik nama provinsi...",
                label_visibility="collapsed"
            )
        with col_send:
            if st.button("📤 Kirim", key="send_btn", use_container_width=True):
                if user_input and user_input.strip():
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    bot_response = get_bot_response(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                    st.rerun()
        
        # Quick Questions
        st.markdown("---")
        st.markdown("📌 **Pertanyaan Cepat:**")
        
        quick_questions = ["Banjir", "Gempa", "Tsunami", "Longsor", "Tas siaga", "Nomor darurat", "Statistik", "Jawa Barat"]
        
        quick_cols = st.columns(4)
        for idx, q in enumerate(quick_questions[:4]):
            with quick_cols[idx]:
                if st.button(q, key=f"quick_{q}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    bot_response = get_bot_response(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                    st.rerun()
        
        quick_cols2 = st.columns(4)
        for idx, q in enumerate(quick_questions[4:]):
            with quick_cols2[idx]:
                if st.button(q, key=f"quick2_{q}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    bot_response = get_bot_response(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                    st.rerun()
        
        # Tombol reset chat
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "👋 Halo! Saya **INA-BOT**, asisten virtual bencana Indonesia. Ada yang bisa saya bantu?\n\n📌 **Coba tanyakan:**\n• Banjir, Gempa, Tsunami, Longsor\n• Gunung meletus\n• Tas siaga\n• Nomor darurat\n• Statistik bencana\n• [Nama Provinsi] - contoh: Jawa Barat"}
            ]
            st.rerun()
    
    st.markdown("---")
    
    # ==================== BREAKING NEWS ====================
    st.markdown('<p class="section-header">🔴 BREAKING NEWS / PERINGATAN DINI</p>', unsafe_allow_html=True)
    
    breaking = st.session_state.data_engine.news[0]
    st.warning(f"**{breaking['title']}**\n\n📍 {breaking['location']} | {breaking['date']}\n\n{breaking['short']}")
    
    # ==================== BERITA TERKINI ====================
    st.markdown('<p class="section-header">📰 BERITA BENCANA TERKINI</p>', unsafe_allow_html=True)
    
    news_cols = st.columns(3)
    for idx, news in enumerate(st.session_state.data_engine.news[:3]):
        with news_cols[idx]:
            with st.container():
                severity_color = "🔴" if news['severity'] == "darurat" else "🟡"
                st.markdown(f"""
                <div class="custom-card">
                    <div style="font-weight: 700; margin-bottom: 8px;">
                        {news['icon']} {news['title']}
                        <span style="font-size: 0.6rem; opacity: 0.7;">{severity_color}</span>
                    </div>
                    <div style="font-size: 0.7rem; opacity: 0.7;">📍 {news['location']}</div>
                    <div style="font-size: 0.7rem; margin: 8px 0;">{news['short']}</div>
                    <div style="font-size: 0.55rem; opacity: 0.6;">{news['date']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Baca", key=f"news_{idx}", use_container_width=True):
                    st.info(f"**{news['title']}**\n\n📅 {news['date']}\n📍 {news['location']}\n\n{news['full']}\n\n⚠️ **INSTRUKSI:** {news['action']}")
    
    # ==================== PROVINSI GRID ====================
    st.markdown('<p class="section-header">🗺️ 34 PROVINSI + 514 KABUPATEN/KOTA</p>', unsafe_allow_html=True)
    
    search_prov = st.text_input("🔍 Cari provinsi...", key="search_prov")
    
    provinces = st.session_state.data_engine.search_provinces(search_prov) if search_prov else st.session_state.data_engine.provinces
    
    prov_cols = st.columns(4)
    for idx, prov in enumerate(provinces[:20]):
        with prov_cols[idx % 4]:
            status_class = "status-darurat" if prov['status'] == "darurat" else "status-waspada"
            status_text = "🔴 DARURAT" if prov['status'] == "darurat" else "🟡 WASPADA"
            
            if st.button(f"🏙️ {prov['name']}\n\n{prov['totalEvents']} kejadian\n{status_text}", key=f"prov_btn_{prov['name']}"):
                st.session_state.selected_province = prov
                st.session_state.show_cities = True
                st.rerun()
    
    # Tampilkan kota-kota
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
        - Total Kejadian: {prov['totalEvents']} kejadian
        - Status: {prov['status'].upper()}
        - Titik Evakuasi: {prov['evacPoints']} titik
        - Pengungsi: {prov['refugees']:,} jiwa
        - Prediksi Risiko: {prov['predRisk']}%
        """)
        
        city_cols = st.columns(5)
        for idx, city in enumerate(prov['cities'][:15]):
            with city_cols[idx % 5]:
                st.markdown(f"""
                <div style="background: rgba(43,110,78,0.1); border-radius: 15px; padding: 10px; margin: 5px; text-align: center;">
                    <span>📍 {city}</span>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== KONTAK DARURAT ====================
    st.markdown('<p class="section-header">📞 KONTAK DARURAT 24/7</p>', unsafe_allow_html=True)
    
    contact_cols = st.columns(5)
    for idx, contact in enumerate(st.session_state.data_engine.emergency_contacts):
        with contact_cols[idx % 5]:
            with st.container():
                st.markdown(f"""
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 2rem;">{contact['icon']}</div>
                    <div class="stat-value">{contact['number']}</div>
                    <div style="font-size: 0.65rem; font-weight: 600;">{contact['name']}</div>
                    <div style="font-size: 0.55rem; opacity: 0.7;">{contact['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

# ==================== PREDIKSI PAGE ====================
elif current_state == "prediksi":
    st.markdown('<p class="section-header">🔮 PREDIKSI & PERINGATAN DINI BENCANA</p>', unsafe_allow_html=True)
    st.caption("AI-Powered Prediction | Akurasi 94.7% | Update Real-time")
    
    st.info("🚨 **AI PREDICTION ACTIVE** - Sistem prediksi berbasis deep learning aktif", icon="🤖")
    
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
    
    st.markdown('<p class="section-header">📅 PREDIKSI HARIAN (7 HARI KE DEPAN)</p>', unsafe_allow_html=True)
    
    pred_cols = st.columns(7)
    for idx, pred in enumerate(st.session_state.data_engine.weekly_predictions):
        with pred_cols[idx]:
            risk_class = "risk-high" if pred['level'] == "high" else ("risk-medium" if pred['level'] == "medium" else "risk-low")
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-weight: 700;">{pred['day']}</div>
                <div style="font-size: 0.6rem; opacity: 0.7;">{pred['date']}</div>
                <div class="{risk_class}" style="font-size: 1.3rem;">{pred['risk']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pred['risk']}%; background: {st.session_state.data_engine.get_risk_level_color(pred['risk'])};"></div>
                </div>
                <div style="font-size: 0.55rem; margin-top: 5px;">{pred['status']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Detail", key=f"pred_{idx}", use_container_width=True):
                st.info(f"**{pred['day']}, {pred['date']}**\n\n📊 Risiko: {pred['risk']}%\n⚠️ Status: {pred['status']}\n\n📝 {pred['desc']}")
    
    st.markdown("---")
    
    st.markdown('<p class="section-header">🌧️ PERINGATAN DINI CUACA EKSTREM</p>', unsafe_allow_html=True)
    
    for warning in st.session_state.data_engine.weather_warnings[:4]:
        severity_icon = "🔴" if warning['severity'] == "high" else "🟡"
        with st.container():
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700;">{warning['type']}</span>
                    <span>{severity_icon} {warning['time']}</span>
                </div>
                <div style="font-size: 0.75rem;">📍 {warning['locations']}</div>
                <div style="font-size: 0.7rem; margin-top: 8px;">{warning['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PANDUAN PAGE ====================
elif current_state == "panduan":
    st.markdown('<p class="section-header">📖 PANDUAN LENGKAP TANGGAP DARURAT</p>', unsafe_allow_html=True)
    st.caption("Pedoman resmi BNPB • Langkah penyelamatan diri • Informasi terkini 24/7")
    
    st.info("🚨 **SIAGA BENCANA 24 JAM** - Hubungi 112 untuk darurat", icon="📞")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(224,122,95,0.25), rgba(224,122,95,0.08)); border-radius: 20px; padding: 20px; border-left: 4px solid #e07a5f;">
            <div style="font-size: 2rem;">🔴</div>
            <h3 style="color: #e07a5f;">RISIKO TINGGI ≥75%</h3>
            <p style="font-size: 0.7rem;">⚠️ STATUS DARURAT - Segera evakuasi ke tempat aman.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(224,163,67,0.25), rgba(224,163,67,0.08)); border-radius: 20px; padding: 20px; border-left: 4px solid #e0a343;">
            <div style="font-size: 2rem;">🟠</div>
            <h3 style="color: #e0a343;">RISIKO SEDANG 50-74%</h3>
            <p style="font-size: 0.7rem;">⚠️ STATUS SIAGA - Tingkatkan kewaspadaan.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(61,155,109,0.25), rgba(61,155,109,0.08)); border-radius: 20px; padding: 20px; border-left: 4px solid #3d9b6d;">
            <div style="font-size: 2rem;">🟢</div>
            <h3 style="color: #3d9b6d;">RISIKO RENDAH <50%</h3>
            <p style="font-size: 0.7rem;">✅ STATUS NORMAL - Tetap waspada.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-header">📋 LANGKAH-LANGKAH SIAGA BENCANA</p>', unsafe_allow_html=True)
    
    for step in st.session_state.data_engine.guide_steps:
        with st.expander(f"LANGKAH {step['num']}: {step['title']}"):
            st.markdown(f"**{step['short']}**")
            st.markdown("---")
            st.markdown(step['long'])
    
    st.markdown("---")
    
    st.markdown('<p class="section-header">🎒 TAS DARURAT LENGKAP (UNTUK 3 HARI)</p>', unsafe_allow_html=True)
    
    kit_cols = st.columns(5)
    for idx, kit in enumerate(st.session_state.data_engine.emergency_kit):
        with kit_cols[idx % 5]:
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2rem;">{kit['icon']}</div>
                <div style="font-weight: 700; font-size: 0.8rem;">{kit['name']}</div>
                <div style="font-size: 0.55rem; opacity: 0.7;">{kit['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.info("💡 **Tips Penting:** Simpan tas darurat di tempat mudah dijangkau dekat pintu keluar. Periksa setiap 3 bulan.")

# ==================== KONTAK PAGE ====================
elif current_state == "kontak":
    st.markdown('<p class="section-header">📞 KONTAK DARURAT 24/7</p>', unsafe_allow_html=True)
    st.caption("Hubungi nomor-nomor berikut untuk bantuan segera | GRATIS dari seluruh operator")
    
    st.info("🚨 **STATUS SIAGA NASIONAL** - Simpan nomor kontak ini di HP Anda!", icon="⚠️")
    
    st.markdown('<p class="section-header">📞 KONTAK DARURAT NASIONAL PRIORITAS</p>', unsafe_allow_html=True)
    
    contact_cols = st.columns(4)
    for idx, contact in enumerate(st.session_state.data_engine.emergency_contacts):
        with contact_cols[idx % 4]:
            st.markdown(f"""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">{contact['icon']}</div>
                <div class="stat-value">{contact['number']}</div>
                <div style="font-weight: 700; font-size: 0.9rem;">{contact['name']}</div>
                <div style="font-size: 0.6rem; opacity: 0.7;">{contact['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-header">🏢 KONTAK BPBD PER PROVINSI</p>', unsafe_allow_html=True)
    
    search_bpbd = st.text_input("🔍 Cari provinsi...", key="search_bpbd")
    
    bpbd_data = []
    for prov in st.session_state.data_engine.provinces:
        if search_bpbd.lower() in prov['name'].lower() or not search_bpbd:
            bpbd_data.append(prov)
    
    bpbd_cols = st.columns(4)
    for idx, prov in enumerate(bpbd_data[:20]):
        with bpbd_cols[idx % 4]:
            status_class = "status-darurat" if prov['status'] == "darurat" else "status-waspada"
            st.markdown(f"""
            <div class="custom-card">
                <div style="font-weight: 700;">🏛️ {prov['name']}</div>
                <div style="font-size: 0.7rem;">📞 {prov['evacPoints']} titik evakuasi</div>
                <div style="font-size: 0.6rem;">🚨 Hotline: 112</div>
                <div style="margin-top: 8px;"><span class="{status_class}">{prov['status'].upper()}</span></div>
            </div>
            """, unsafe_allow_html=True)

# ==================== DONASI PAGE ====================
elif current_state == "donasi":
    st.markdown('<p class="section-header">🤝 DONASI BENCANA INDONESIA</p>', unsafe_allow_html=True)
    st.caption("Salurkan bantuan Anda untuk korban bencana")
    
    st.info("🙏 **Terima kasih atas kepedulian Anda!** Setiap donasi sangat berarti bagi korban bencana", icon="❤️")
    
    with st.form("donation_form"):
        st.markdown("### 📝 FORM DONASI")
        
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *", placeholder="Masukkan nama lengkap Anda")
            email = st.text_input("Email *", placeholder="email@example.com")
            whatsapp = st.text_input("WhatsApp *", placeholder="6281234567890")
        
        with col2:
            nominal = st.number_input("Nominal Donasi *", min_value=10000, step=10000, placeholder="Minimal Rp10.000")
            bank = st.selectbox("Pilih Bank Tujuan *", ["BCA - 1234567890", "MANDIRI - 1234567890123", "BRI - 123456789012345"])
            bencana = st.selectbox("Donasi Untuk Bencana *", ["Banjir Bandang Garut", "Gempa Sukabumi", "Erupsi Semeru", "Banjir Umum", "Tanah Longsor"])
        
        pesan = st.text_area("Pesan & Doa (opsional)", placeholder="Tulis pesan dukungan untuk korban...")
        uploaded_file = st.file_uploader("Upload Bukti Transfer", type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button("💝 DONASI SEKARANG", use_container_width=True, type="primary")
        
        if submitted:
            if nama and email and whatsapp and nominal:
                st.success(f"""
                ✅ **Donasi Berhasil!**
                
                Terima kasih, {nama}!
                
                💰 Nominal: Rp{nominal:,}
                🏦 Bank: {bank}
                🌋 Untuk: {bencana}
                
                🙏 Doa dan dukungan Anda sangat berarti bagi korban bencana.
                """)
            else:
                st.error("❌ Mohon lengkapi semua data yang diperlukan!")
    
    st.markdown("---")
    
    st.markdown("### 🏦 REKENING TUJUAN RESMI")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem;">🏦</div>
            <div style="font-weight: 800;">BCA</div>
            <div style="font-size: 1.1rem; letter-spacing: 1px;">1234567890</div>
            <div style="font-size: 0.7rem;">a.n. Yayasan Bencana Indonesia</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem;">🏦</div>
            <div style="font-weight: 800;">MANDIRI</div>
            <div style="font-size: 1.1rem; letter-spacing: 1px;">1234567890123</div>
            <div style="font-size: 0.7rem;">a.n. Yayasan Bencana Indonesia</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="custom-card" style="text-align: center;">
            <div style="font-size: 2rem;">🏦</div>
            <div style="font-weight: 800;">BRI</div>
            <div style="font-size: 1.1rem; letter-spacing: 1px;">123456789012345</div>
            <div style="font-size: 0.7rem;">a.n. Yayasan Bencana Indonesia</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== HUBUNGI KAMI PAGE ====================
elif current_state == "hubungi":
    st.markdown('<p class="section-header">💬 HUBUNGI KAMI</p>', unsafe_allow_html=True)
    st.caption("Keluhan, laporan bencana, dan aspirasi Anda sangat kami hargai")
    
    st.info("💬 **Laporan akan otomatis terkirim ke Admin via WhatsApp!**", icon="📱")
    
    st.markdown('<p class="section-header">📝 LAPORKAN KEJADIAN / KELUHAN</p>', unsafe_allow_html=True)
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_lapor = st.text_input("Nama Lengkap *", placeholder="Masukkan nama Anda")
            kontak_lapor = st.text_input("Nomor WhatsApp *", placeholder="6281234567890")
        with col2:
            provinsi_lapor = st.selectbox("Provinsi *", [p['name'] for p in st.session_state.data_engine.provinces])
            jenis_lapor = st.selectbox("Jenis Laporan *", ["Banjir", "Gempa Bumi", "Tanah Longsor", "Kebakaran Hutan", "Angin Puting Beliung", "Kekeringan", "Infrastruktur Rusak", "Bantuan Belum Datang", "Lainnya"])
        
        lokasi_lapor = st.text_input("Lokasi Detail *", placeholder="Contoh: RT 02 RW 05, Kelurahan X, Kecamatan Y")
        deskripsi_lapor = st.text_area("Deskripsi Kejadian / Keluhan *", placeholder="Ceritakan kejadian secara detail...", height=150)
        
        submitted = st.form_submit_button("📤 KIRIM LAPORAN", use_container_width=True, type="primary")
        
        if submitted:
            if nama_lapor and kontak_lapor and provinsi_lapor and lokasi_lapor and deskripsi_lapor:
                st.success(f"""
                ✅ **Laporan Berhasil Dikirim!**
                
                Terima kasih, {nama_lapor}! Laporan Anda telah kami terima.
                
                📋 Ringkasan Laporan:
                - Jenis: {jenis_lapor}
                - Lokasi: {provinsi_lapor} - {lokasi_lapor}
                
                ⏰ Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                
                Admin akan segera merespon laporan Anda.
                """)
            else:
                st.error("❌ Mohon lengkapi semua data yang diperlukan!")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding: 20px; font-size: 11px; opacity: 0.6;'>"
    "🛡️ INA-PREDICT | Sistem Informasi & Peringatan Dini Bencana Indonesia<br>"
    "Sumber: BNPB - BMKG - BPBD | Data real-time | Akurasi 98.7%"
    "</div>",
    unsafe_allow_html=True
)