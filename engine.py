# ============ FILE 2: engine.py ============
# Mesin utama untuk data dan logika aplikasi

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DisasterDataEngine:
    """Engine untuk mengelola data bencana"""
    
    def __init__(self):
        self.last_update = datetime.now()
        
        # Data statistik utama
        self.main_stats = [
            {"title": "TOTAL KEJADIAN", "value": "3,247", "sub": "+12% dari 2025 | 34 provinsi", 
             "detail": "📊 TOTAL BENCANA 2026: 3.247 kejadian\n\n📋 BANJIR: 1.204 (37.1%)\n🌍 GEMPA: 712 (21.9%)\n⛰️ LONGSOR: 589 (18.1%)\n🔥 KARHUTLA: 312 (9.6%)\n⛈️ CUACA EKSTREM: 430 (13.3%)\n\n📍 Provinsi tertinggi: Jawa Barat (589), Jawa Timur (534), Jawa Tengah (456)"},
            {"title": "PERINGATAN AKTIF", "value": "34", "sub": "🔴 14 Darurat | 🟡 20 Waspada",
             "detail": "⚠️ 34 PERINGATAN AKTIF\n\n🔴 STATUS DARURAT (14 provinsi):\nJawa Barat, Jawa Timur, Jawa Tengah, Banten, Sulawesi Tengah, Sumatera Barat, Kalimantan Selatan, Papua, Aceh, Sumatera Utara, Riau, Lampung, DKI Jakarta, Bali\n\n🟡 STATUS WASPADA (20 provinsi):\nNTB, NTT, Sulsel, Kaltim, Kalteng, dan lainnya"},
            {"title": "TITIK EVAKUASI", "value": "7,245", "sub": "Kapasitas 850k jiwa",
             "detail": "🏢 7.245 TITIK EVAKUASI\n\nKapasitas total: 850.000 jiwa\n\n📍 Top 3 titik evakuasi:\n1. Jawa Barat (1.250 titik)\n2. Jawa Timur (1.120 titik)\n3. Jawa Tengah (987 titik)\n\nTersebar di 514 kabupaten/kota seluruh Indonesia"},
            {"title": "PROVINSI TERDAMPAK", "value": "33/34", "sub": "97% wilayah",
             "detail": "🗺️ 33 dari 34 provinsi terdampak bencana\n\n📊 TINGKAT KERUSAKAN:\n- Berat: 8 provinsi\n- Sedang: 15 provinsi\n- Ringan: 10 provinsi\n\n✅ Provinsi dengan kejadian terendah: Kepulauan Riau (38 kejadian)"},
            {"title": "PENGUNGSI", "value": "412.7k", "sub": "+52k dalam 7 hari",
             "detail": "👥 412.750 JIWA MENGUNGSI\n\nTersebar di 1.247 titik pengungsian\n\n📍 Rincian per provinsi:\n- Jawa Barat: 65.430 jiwa\n- Jawa Timur: 58.760 jiwa\n- Jawa Tengah: 49.870 jiwa\n- Banten: 32.450 jiwa\n- Sulawesi Tengah: 29.870 jiwa\n\nKorban meninggal: 687 jiwa\nKorban luka: 5.234 jiwa"},
            {"title": "PERSONEL SIAGA", "value": "78.2k", "sub": "TNI/Polri + Relawan",
             "detail": "🛡️ 78.200 PERSONEL SIAGA\n\n🔹 TNI: 32.500 personel\n🔹 POLRI: 28.700 personel\n🔹 Relawan Terlatih: 17.000 orang\n\n🚁 45 helikopter siaga\n🚛 1.200 kendaraan taktis\n🚑 800 ambulans tersebar\n📡 1.500 radio komunikasi"}
        ]
        
        # Data breakdown bencana
        self.disaster_breakdown = [
            {"name": "BANJIR", "icon": "🌊", "count": 1204, "percent": 37.1, "color": "#2b6e4e",
             "desc": "💧 BANJIR: 1.204 kejadian\n\n📍 Tertinggi: Jawa Barat (312), Jawa Timur (278), Kalimantan Selatan (189)\n⚠️ Kerugian: Rp2.4 Triliun\n🏠 Rumah terendam: 34.500 unit\n👥 Pengungsi: 189.430 jiwa"},
            {"name": "GEMPA", "icon": "🌋", "count": 712, "percent": 21.9, "color": "#c25d45",
             "desc": "🌍 GEMPA: 712 kejadian\n\n📍 Tertinggi: Jawa Barat (189), Sumatera Barat (145), Papua (98)\n📊 Magnitudo tertinggi: M 6,2\n⚠️ Kerusakan: 12.400 bangunan rusak\n💀 Korban meninggal: 187 jiwa"},
            {"name": "LONGSOR", "icon": "⛰️", "count": 589, "percent": 18.1, "color": "#e0a343",
             "desc": "⛰️ LONGSOR: 589 kejadian\n\n📍 Tertinggi: Jawa Tengah (178), Jawa Barat (156), Jawa Timur (98)\n⚠️ 235 jiwa meninggal dunia\n🏠 8.900 rumah tertimbun\n🚧 245 ruas jalan tertutup"},
            {"name": "KARHUTLA", "icon": "🔥", "count": 312, "percent": 9.6, "color": "#e07a5f",
             "desc": "🔥 KARHUTLA: 312 kejadian\n\n📍 Tertinggi: Riau (98), Kalimantan Selatan (67), Jambi (45)\n🌫️ Kabut asap: 8 provinsi terdampak\n👥 ISPA: 45.000 kasus\n🌳 Luas lahan terbakar: 45.000 hektar"},
            {"name": "CUACA EKSTREM", "icon": "🌪️", "count": 430, "percent": 13.3, "color": "#5f9b8a",
             "desc": "⛈️ CUACA EKSTREM: 430 kejadian\n\n📍 Tertinggi: Aceh (78), Sumatera Utara (67), NTB (56)\n💨 Puting beliung: 89 kejadian\n⚠️ 12.400 rumah rusak\n🌊 Puting beliung di Jawa Timur: 34 kejadian"}
        ]
        
        # Data provinsi lengkap
        self.provinces = [
            {"name": "Aceh", "status": "waspada", "totalEvents": 187, "evacPoints": 412, "refugees": 12450, "deaths": 23, "injured": 156, "predRisk": 79, 
             "cities": ["Banda Aceh", "Sabang", "Lhokseumawe", "Langsa", "Subulussalam", "Jantho", "Kutacane", "Meulaboh", "Takengon", "Sigli", "Tapaktuan", "Blangpidie", "Bireuen", "Samalanga", "Sinabang", "Calang"]},
            {"name": "Sumatera Utara", "status": "waspada", "totalEvents": 245, "evacPoints": 589, "refugees": 18720, "deaths": 31, "injured": 198, "predRisk": 73,
             "cities": ["Medan", "Binjai", "Pematangsiantar", "Tebing Tinggi", "Tanjungbalai", "Sibolga", "Padang Sidempuan", "Gunungsitoli", "Kisaran", "Rantauprapat", "Parapat", "Berastagi", "Kabanjahe", "Stabat", "Lubuk Pakam"]},
            {"name": "Sumatera Barat", "status": "darurat", "totalEvents": 312, "evacPoints": 721, "refugees": 25430, "deaths": 41, "injured": 298, "predRisk": 87,
             "cities": ["Padang", "Bukittinggi", "Payakumbuh", "Solok", "Padang Panjang", "Pariaman", "Sawahlunto", "Lubuk Basung", "Batusangkar", "Painan", "Balai Selasa", "Koto Baru", "Sijunjung"]},
            {"name": "Riau", "status": "waspada", "totalEvents": 198, "evacPoints": 543, "refugees": 15670, "deaths": 19, "injured": 134, "predRisk": 78,
             "cities": ["Pekanbaru", "Dumai", "Bengkalis", "Siak", "Rengat", "Bangkinang", "Tembilahan", "Selat Panjang", "Ujung Tanjung", "Bagan Batu", "Pasir Pengaraian"]},
            {"name": "Jambi", "status": "waspada", "totalEvents": 145, "evacPoints": 389, "refugees": 9870, "deaths": 12, "injured": 89, "predRisk": 68,
             "cities": ["Jambi", "Sungai Penuh", "Muara Bungo", "Bangko", "Kuala Tungkal", "Sengeti", "Muara Tebo", "Sarolangun", "Sungai Manas"]},
            {"name": "Sumatera Selatan", "status": "waspada", "totalEvents": 178, "evacPoints": 456, "refugees": 12340, "deaths": 21, "injured": 112, "predRisk": 71,
             "cities": ["Palembang", "Prabumulih", "Lubuklinggau", "Pagar Alam", "Baturaja", "Kayuagung", "Sekayu", "Muara Enim", "Lahat", "Martapura"]},
            {"name": "Bengkulu", "status": "waspada", "totalEvents": 98, "evacPoints": 278, "refugees": 6540, "deaths": 11, "injured": 67, "predRisk": 62,
             "cities": ["Bengkulu", "Manna", "Arga Makmur", "Curup", "Kepahiang", "Muara Aman", "Tais", "Bintuhan", "Kota Padang"]},
            {"name": "Lampung", "status": "waspada", "totalEvents": 189, "evacPoints": 456, "refugees": 13450, "deaths": 22, "injured": 145, "predRisk": 76,
             "cities": ["Bandar Lampung", "Metro", "Kotabumi", "Liwa", "Kalianda", "Pringsewu", "Gunungsugih", "Blambangan Umpu", "Menggala", "Sukadana"]},
            {"name": "Kep. Bangka Belitung", "status": "waspada", "totalEvents": 45, "evacPoints": 156, "refugees": 3210, "deaths": 5, "injured": 34, "predRisk": 52,
             "cities": ["Pangkalpinang", "Sungailiat", "Mentok", "Tanjung Pandan", "Manggar", "Toboali", "Koba"]},
            {"name": "Kepulauan Riau", "status": "waspada", "totalEvents": 38, "evacPoints": 134, "refugees": 2870, "deaths": 3, "injured": 28, "predRisk": 50,
             "cities": ["Tanjungpinang", "Batam", "Karimun", "Bintan", "Natuna", "Anambas", "Lingga"]},
            {"name": "DKI Jakarta", "status": "waspada", "totalEvents": 276, "evacPoints": 634, "refugees": 28760, "deaths": 28, "injured": 234, "predRisk": 75,
             "cities": ["Jakarta Pusat", "Jakarta Barat", "Jakarta Selatan", "Jakarta Timur", "Jakarta Utara", "Kepulauan Seribu", "Gambir", "Menteng", "Cengkareng", "Cilincing"]},
            {"name": "Jawa Barat", "status": "darurat", "totalEvents": 589, "evacPoints": 1250, "refugees": 65430, "deaths": 87, "injured": 543, "predRisk": 92,
             "cities": ["Bandung", "Bekasi", "Bogor", "Depok", "Cimahi", "Sukabumi", "Cianjur", "Garut", "Tasikmalaya", "Cirebon", "Purwakarta", "Karawang", "Subang", "Sumedang", "Indramayu", "Majalengka", "Kuningan", "Banjar", "Ciamis", "Pangandaran"]},
            {"name": "Jawa Tengah", "status": "darurat", "totalEvents": 456, "evacPoints": 987, "refugees": 49870, "deaths": 63, "injured": 398, "predRisk": 85,
             "cities": ["Semarang", "Surakarta", "Magelang", "Purwokerto", "Pekalongan", "Tegal", "Salatiga", "Kudus", "Cilacap", "Purbalingga", "Banjarnegara", "Wonosobo", "Kebumen", "Purworejo", "Klaten", "Sukoharjo", "Boyolali", "Temanggung", "Wonogiri", "Rembang", "Blora", "Grobogan", "Demak", "Jepara", "Pati", "Kendal"]},
            {"name": "DI Yogyakarta", "status": "waspada", "totalEvents": 156, "evacPoints": 398, "refugees": 12340, "deaths": 18, "injured": 112, "predRisk": 72,
             "cities": ["Yogyakarta", "Sleman", "Bantul", "Kulon Progo", "Gunungkidul", "Wates", "Godean", "Depok", "Kalasan", "Ngemplak"]},
            {"name": "Jawa Timur", "status": "darurat", "totalEvents": 534, "evacPoints": 1120, "refugees": 58760, "deaths": 72, "injured": 487, "predRisk": 88,
             "cities": ["Surabaya", "Malang", "Kediri", "Blitar", "Madiun", "Probolinggo", "Lumajang", "Sidoarjo", "Jember", "Banyuwangi", "Mojokerto", "Pasuruan", "Pacitan", "Ponorogo", "Tuban", "Bojonegoro", "Ngawi", "Magetan", "Nganjuk", "Jombang", "Lamongan", "Gresik", "Bangkalan", "Sampang", "Pamekasan", "Sumenep"]},
            {"name": "Banten", "status": "darurat", "totalEvents": 289, "evacPoints": 678, "refugees": 32450, "deaths": 34, "injured": 267, "predRisk": 90,
             "cities": ["Serang", "Cilegon", "Tangerang", "Tangerang Selatan", "Pandeglang", "Lebak", "Rangkasbitung", "Balaraja", "Malingping", "Cikupa", "Curug", "Teluknaga", "Sepatan", "Mauk", "Kresek"]},
            {"name": "Bali", "status": "waspada", "totalEvents": 134, "evacPoints": 298, "refugees": 8970, "deaths": 12, "injured": 98, "predRisk": 65,
             "cities": ["Denpasar", "Badung", "Gianyar", "Karangasem", "Buleleng", "Tabanan", "Bangli", "Klungkung", "Jembrana", "Singaraja", "Kuta", "Seminyak", "Ubud"]},
            {"name": "Nusa Tenggara Barat", "status": "waspada", "totalEvents": 156, "evacPoints": 367, "refugees": 11230, "deaths": 18, "injured": 112, "predRisk": 70,
             "cities": ["Mataram", "Bima", "Sumbawa Besar", "Praya", "Selong", "Dompu", "Taliwang", "Raba", "Gerung", "Lombok Barat", "Lombok Tengah", "Lombok Timur"]},
            {"name": "Nusa Tenggara Timur", "status": "waspada", "totalEvents": 178, "evacPoints": 412, "refugees": 14320, "deaths": 21, "injured": 134, "predRisk": 72,
             "cities": ["Kupang", "Ende", "Maumere", "Labuan Bajo", "Ruteng", "Waingapu", "Soe", "Atambua", "Kefamenanu", "Kalabahi", "Bajawa", "Borong", "Lewoleba"]},
            {"name": "Kalimantan Barat", "status": "waspada", "totalEvents": 112, "evacPoints": 423, "refugees": 14320, "deaths": 14, "injured": 98, "predRisk": 63,
             "cities": ["Pontianak", "Singkawang", "Sambas", "Mempawah", "Bengkayang", "Landak", "Sanggau", "Sekadau", "Sintang", "Melawi", "Kapuas Hulu", "Ketapang", "Kayong Utara", "Kubu Raya"]},
            {"name": "Kalimantan Tengah", "status": "waspada", "totalEvents": 108, "evacPoints": 398, "refugees": 13450, "deaths": 13, "injured": 87, "predRisk": 64,
             "cities": ["Palangka Raya", "Kasongan", "Kuala Kapuas", "Buntok", "Tamiang Layang", "Muara Teweh", "Puruk Cahu", "Sampit", "Pangkalan Bun", "Sukamara", "Lamandau"]},
            {"name": "Kalimantan Selatan", "status": "darurat", "totalEvents": 289, "evacPoints": 567, "refugees": 27650, "deaths": 38, "injured": 276, "predRisk": 86,
             "cities": ["Banjarmasin", "Banjarbaru", "Kotabaru", "Martapura", "Pelaihari", "Barabai", "Kandangan", "Rantau", "Amuntai", "Tanjung", "Marabahan", "Paringin", "Batu Licin"]},
            {"name": "Kalimantan Timur", "status": "waspada", "totalEvents": 98, "evacPoints": 367, "refugees": 11230, "deaths": 11, "injured": 76, "predRisk": 61,
             "cities": ["Samarinda", "Balikpapan", "Bontang", "Tenggarong", "Sangatta", "Berau", "Penajam", "Paser", "Kutai Barat", "Mahakam Ulu"]},
            {"name": "Kalimantan Utara", "status": "waspada", "totalEvents": 56, "evacPoints": 189, "refugees": 4320, "deaths": 6, "injured": 41, "predRisk": 55,
             "cities": ["Tanjung Selor", "Tarakan", "Malinau", "Nunukan", "Bulungan", "Krayan", "Sebatik", "Sesayap"]},
            {"name": "Sulawesi Utara", "status": "waspada", "totalEvents": 145, "evacPoints": 389, "refugees": 12450, "deaths": 17, "injured": 98, "predRisk": 68,
             "cities": ["Manado", "Bitung", "Tomohon", "Kotamobagu", "Minahasa", "Kawangkoan", "Airmadidi", "Tondano", "Amurang", "Tahuna", "Melonguane", "Sangihe", "Talaud"]},
            {"name": "Sulawesi Tengah", "status": "darurat", "totalEvents": 278, "evacPoints": 621, "refugees": 29870, "deaths": 56, "injured": 412, "predRisk": 89,
             "cities": ["Palu", "Poso", "Donggala", "Sigi", "Banggai", "Morowali", "Tojo Una-Una", "Buol", "Tolitoli", "Ampana", "Luwuk", "Bunta", "Batui", "Bungku", "Kolonedale"]},
            {"name": "Sulawesi Selatan", "status": "waspada", "totalEvents": 198, "evacPoints": 456, "refugees": 15670, "deaths": 24, "injured": 167, "predRisk": 71,
             "cities": ["Makassar", "Parepare", "Palopo", "Bulukumba", "Bantaeng", "Jeneponto", "Takalar", "Gowa", "Maros", "Pangkajene", "Barru", "Bone", "Soppeng", "Wajo", "Sidenreng", "Pinrang", "Enrekang", "Tana Toraja"]},
            {"name": "Sulawesi Tenggara", "status": "waspada", "totalEvents": 123, "evacPoints": 345, "refugees": 9870, "deaths": 15, "injured": 89, "predRisk": 65,
             "cities": ["Kendari", "Baubau", "Kolaka", "Raha", "Unaaha", "Andoolo", "Lasusua", "Rumbia", "Wangi-Wangi", "Pasarwajo"]},
            {"name": "Sulawesi Barat", "status": "waspada", "totalEvents": 98, "evacPoints": 298, "refugees": 7650, "deaths": 12, "injured": 67, "predRisk": 62,
             "cities": ["Mamuju", "Polewali", "Majene", "Mamasa", "Pasangkayu", "Baras", "Tikke Raya", "Bambalamotu", "Topoyo", "Budong-Budong"]},
            {"name": "Gorontalo", "status": "waspada", "totalEvents": 76, "evacPoints": 234, "refugees": 5430, "deaths": 8, "injured": 54, "predRisk": 58,
             "cities": ["Gorontalo", "Limboto", "Marisa", "Suwawa", "Tilamuta", "Kwandang", "Bone Bolango", "Pohuwato", "Paguyaman", "Telaga"]},
            {"name": "Maluku", "status": "waspada", "totalEvents": 89, "evacPoints": 278, "refugees": 6540, "deaths": 11, "injured": 76, "predRisk": 60,
             "cities": ["Ambon", "Tual", "Masohi", "Saumlaki", "Namlea", "Bula", "Langgur", "Dobo", "Piru", "Liang"]},
            {"name": "Maluku Utara", "status": "waspada", "totalEvents": 78, "evacPoints": 256, "refugees": 5980, "deaths": 9, "injured": 63, "predRisk": 59,
             "cities": ["Sofifi", "Ternate", "Tidore", "Tobelo", "Bacan", "Labuha", "Sanana", "Galela", "Jailolo", "Maba"]},
            {"name": "Papua", "status": "darurat", "totalEvents": 245, "evacPoints": 489, "refugees": 21450, "deaths": 52, "injured": 187, "predRisk": 84,
             "cities": ["Jayapura", "Merauke", "Biak", "Nabire", "Wamena", "Timika", "Serui", "Enarotali", "Sentani", "Abepura", "Waena", "Depapre", "Skouw", "Holtekamp"]},
            {"name": "Papua Barat", "status": "waspada", "totalEvents": 87, "evacPoints": 267, "refugees": 6540, "deaths": 11, "injured": 76, "predRisk": 60,
             "cities": ["Manokwari", "Sorong", "Fakfak", "Bintuni", "Teminabuan", "Ransiki", "Waisai", "Kaimana", "Ayamaru"]}
        ]
        
        # Data berita
        self.news = [
            {"title": "🔴 BANJIR BANDANG GARUT - 1.800 Jiwa Mengungsi", "location": "Garut, Jawa Barat", "date": "07 Juni 2026 | 14:30 WIB", "severity": "darurat", "icon": "🌊", "short": "Banjir setinggi 2.5 meter, 500 rumah terendam", 
             "full": "BANJIR BANDANG melanda 12 desa di Kecamatan Banyuresmi. Ketinggian air 2.5-3 meter. 500 rumah terendam. Akses Garut-Tasikmalaya lumpuh total.", "action": "🔴 EVAKUASI SEGERA ke tempat tinggi! Matikan listrik! Bawa dokumen penting!"},
            {"title": "🔴 GEMPA M 5,7 SUKABUMI", "location": "Sukabumi, Jawa Barat", "date": "07 Juni 2026 | 08:45 WIB", "severity": "darurat", "icon": "🌋", "short": "200 rumah rusak, getaran hingga Jakarta", 
             "full": "Gempa dangkal magnitudo 5,7. Pusat di darat 25 km Tenggara Sukabumi. 200 rumah rusak ringan, 45 rusak berat.", "action": "DROP, COVER, HOLD ON! Lindungi kepala! Waspada gempa susulan!"},
            {"title": "🔴 TSUNAMI MEGATHRUST - Evakuasi Massal", "location": "Banten & Lampung", "date": "06 Juni 2026 | 22:15 WIB", "severity": "darurat", "icon": "🌊", "short": "50.000+ jiwa dievakuasi", 
             "full": "BMKG peringatan dini tsunami pasca aktivitas Gunung Anak Krakatau. Evakuasi massal Anyer, Carita, Lampung Selatan.", "action": "🔴 LARI KE TEMPAT TINGGI minimal 30 meter! Jauhi pantai!"},
            {"title": "🔴 GUNUNG SEMERU ERUPSI", "location": "Lumajang, Jawa Timur", "date": "06 Juni 2026 | 07:30 WIB", "severity": "darurat", "icon": "🌋", "short": "Awan panas 5km, 2.000 mengungsi", 
             "full": "Awan panas guguran sejauh 5 km ke Besuk Kobokan. Radius bahaya 8 km. Hujan abu tipis di Lumajang.", "action": "Gunakan masker N95! Jauhi radius 8km! Waspada lahar dingin!"},
            {"title": "🟡 KARHUTLA RIAU - 8.000 ISPA", "location": "Riau", "date": "05 Juni 2026", "severity": "waspada", "icon": "🔥", "short": "Kualitas Udara Tidak Sehat", 
             "full": "Kebakaran hutan di Bengkalis, Dumai, Rokan Hilir. 60 hotspot. PM2.5: 120-150.", "action": "Gunakan masker N95! Tutup ventilasi! Kurangi aktivitas luar!"},
            {"title": "🟡 LONGSOR TUTUP JALUR PUNCAK", "location": "Puncak, Bogor", "date": "05 Juni 2026", "severity": "waspada", "icon": "⛰️", "short": "800 kendaraan terjebak", 
             "full": "Material longsor setinggi 4 meter menutup total jalur Puncak KM 41+200.", "action": "Cari jalur alternatif Ciawi-Sukabumi! Waspada longsor susulan!"}
        ]
        
        # Data kontak darurat
        self.emergency_contacts = [
            {"name": "PUSAT DARURAT 112", "number": "112", "desc": "Polisi, Ambulans, Pemadam, SAR - GRATIS 24 Jam", "icon": "📞"},
            {"name": "BNPB PUSAT", "number": "(021) 3522911", "desc": "Badan Nasional Penanggulangan Bencana", "icon": "🏢"},
            {"name": "AMBULANS & MEDIS", "number": "118 / 119", "desc": "Gawat Darurat Medis 24 Jam", "icon": "🚑"},
            {"name": "PEMADAM KEBAKARAN", "number": "113", "desc": "Kebakaran & Penyelamatan", "icon": "🔥"},
            {"name": "BPBD DAERAH", "number": "112", "desc": "Bencana Daerah - Terintegrasi", "icon": "🏛️"}
        ]
        
        # Data prediksi mingguan
        self.weekly_predictions = [
            {"day": "Selasa", "date": "10 Juni", "risk": 72, "level": "medium", "status": "WASPADA", 
             "desc": "Potensi hujan lebat di Jabar, Jateng, Jatim dengan intensitas 50-100mm/hari"},
            {"day": "Rabu", "date": "11 Juni", "risk": 78, "level": "medium", "status": "SIAGA", 
             "desc": "Intensitas hujan meningkat signifikan mencapai 120mm/hari"},
            {"day": "Kamis", "date": "12 Juni", "risk": 86, "level": "high", "status": "DARURAT", 
             "desc": "Puncak musim hujan! Curah hujan ekstrem 160mm/hari"},
            {"day": "Jumat", "date": "13 Juni", "risk": 83, "level": "high", "status": "SIAGA", 
             "desc": "Hujan masih tinggi 130mm/hari. Waspada banjir rob"},
            {"day": "Sabtu", "date": "14 Juni", "risk": 76, "level": "medium", "status": "WASPADA", 
             "desc": "Intensitas mulai menurun menjadi 80mm/hari"},
            {"day": "Minggu", "date": "15 Juni", "risk": 68, "level": "medium", "status": "WASPADA", 
             "desc": "Cuaca mulai stabil, hujan 50mm/hari"},
            {"day": "Senin", "date": "16 Juni", "risk": 55, "level": "low", "status": "NORMAL", 
             "desc": "Kondisi mulai normal dengan hujan ringan 20mm/hari"}
        ]
        
        # Data panduan
        self.guide_steps = [
            {"num": 1, "title": "PERSIAPAN SEBELUM BENCANA", 
             "short": "Siapkan tas darurat, kenali jalur evakuasi, buat rencana komunikasi keluarga.",
             "long": "📋 PERSIAPAN SEBELUM BENCANA - LANGKAH DETAIL\n\n✅ PERSIAPAN TAS DARURAT:\n• Siapkan tas ransel yang kuat dan kedap air\n• Isi dengan air minum (minimal 3 liter per orang)\n• Sertakan makanan tahan lama (kaleng, biskuit)\n• Masukkan P3K lengkap dan obat-obatan pribadi\n• Siapkan senter, baterai, power bank, dan radio\n• Dokumen penting dalam plastik kedap air\n• Uang tunai minimal Rp500.000\n\n✅ KENALI LINGKUNGAN DAN RISIKO:\n• Pelajari peta rawan bencana di daerah Anda\n• Identifikasi minimal 3 jalur evakuasi berbeda\n• Tentukan titik kumpul keluarga di tempat aman\n• Catat lokasi posko bencana dan BPBD terdekat"},
            {"num": 2, "title": "KETIKA PERINGATAN DINI", 
             "short": "Pantau info resmi BMKG/BNPB, amankan barang, bersiap evakuasi.",
             "long": "📋 KETIKA PERINGATAN DINI DITERIMA\n\n✅ HAL YANG HARUS SEGERA DILAKUKAN:\n• Tetap tenang dan jangan panik\n• Pantau informasi dari sumber resmi (BMKG, BNPB)\n• Jangan percaya pada hoaks di media sosial\n• Matikan aliran listrik, gas, dan air di rumah\n• Amankan barang-barang berharga ke tempat tinggi\n• Bawa tas darurat dan berkas penting\n• Bersiap untuk evakuasi jika diperintahkan\n\n✅ JANGAN LAKUKAN:\n✖️ Jangan menyebarkan informasi belum terverifikasi\n✖️ Jangan menggunakan lift saat evakuasi\n✖️ Jangan berhenti di bawah jembatan/ pohon besar"},
            {"num": 3, "title": "SAAT BENCANA TERJADI", 
             "short": "Tetap tenang, lindungi kepala, cari tempat aman, ikuti instruksi.",
             "long": "📋 SAAT BENCANA TERJADI\n\n✅ SAAT GEMPA BUMI:\n• DROP: Jatuhkan tubuh ke lantai\n• COVER: Lindungi kepala di bawah meja\n• HOLD ON: Pegang kaki meja sampai gempa berhenti\n• Jauhi jendela, cermin, rak buku\n\n✅ SAAT BANJIR:\n• Segera pindah ke tempat yang lebih tinggi\n• Jangan berjalan di air banjir - arus bisa menyapu\n• Matikan aliran listrik sebelum meninggalkan rumah\n\n✅ SAAT TANAH LONGSOR:\n• Perhatikan tanda-tanda: retakan tanah, suara gemuruh\n• Segera tinggalkan area\n• Berlari ke arah samping (menjauhi jalur longsor)"},
            {"num": 4, "title": "SETELAH BENCANA", 
             "short": "Cek kondisi sekitar, hindari area berbahaya, dengarkan info resmi.",
             "long": "📋 SETELAH BENCANA\n\n✅ HAL YANG HARUS DILAKUKAN:\n• Periksa apakah ada anggota keluarga yang terluka\n• Jauhi area yang rusak dan kabel listrik putus\n• Dengarkan radio/TV untuk informasi resmi\n• Jangan menyebarkan rumor atau hoaks\n• Gunakan pesan teks daripada telepon\n• Cek kondisi tetangga dan bantu yang membutuhkan\n\n✅ KEMBALI KE RUMAH:\n• Jangan masuk ke rumah yang rusak parah\n• Periksa kebocoran gas - jangan gunakan korek api\n• Dokumentasikan kerusakan dengan foto\n• Buang semua makanan yang terkontaminasi"},
            {"num": 5, "title": "DI TEMPAT PENGUNGSIAN", 
             "short": "Laporkan diri ke posko, jaga kebersihan, ikuti arahan petugas.",
             "long": "📋 DI TEMPAT PENGUNGSIAN\n\n✅ YANG HARUS DILAKUKAN:\n• Laporkan diri dan keluarga ke petugas posko\n• Isi data pengungsi dengan lengkap\n• Dapatkan nomor identitas pengungsi\n• Cari tempat aman untuk beristirahat\n• Jaga kebersihan diri dan lingkungan\n\n✅ KESEHATAN DI PENGUNGSIAN:\n• Gunakan air bersih untuk minum dan masak\n• Konsumsi makanan bergizi yang disediakan\n• Segera laporkan jika ada yang sakit\n• Minum obat rutin tepat waktu"},
            {"num": 6, "title": "PEMULIHAN PASCA BENCANA", 
             "short": "Ikuti program pemulihan pemerintah, bangun kembali rumah lebih aman.",
             "long": "📋 PEMULIHAN PASCA BENCANA\n\n✅ PROGRAM PEMULIHAN:\n• Ikuti program pemulihan dari pemerintah\n• Daftarkan diri untuk bantuan rehabilitasi rumah\n• Dapatkan layanan konseling jika mengalami trauma\n• Ikuti program pelatihan keterampilan\n\n✅ MEMBANGUN KEMBALI:\n• Bangun dengan konstruksi tahan bencana\n• Konsultasikan dengan ahli konstruksi\n• Gunakan material berkualitas\n• Bangun di lokasi yang aman dari ancaman bencana"}
        ]
        
        # Data tips
        self.tips = [
            {"title": "Jalur Evakuasi", "desc": "Kenali minimal 3 jalur evakuasi berbeda dari rumah ke titik kumpul", "icon": "🚶"},
            {"title": "Power Bank", "desc": "Siapkan power bank kapasitas besar (10.000mAh+) yang selalu terisi penuh", "icon": "🔋"},
            {"title": "Titik Kumpul Keluarga", "desc": "Tentukan 2 titik kumpul: di dalam lingkungan dan di luar kota", "icon": "🏠"},
            {"title": "Jangan Panik", "desc": "Panik adalah musuh utama. Ambil napas dalam, pikirkan langkah yang direncanakan", "icon": "😌"},
            {"title": "Tempat Berteduh", "desc": "Kenali bangunan kokoh terdekat: masjid, gereja, sekolah, gedung pemerintah", "icon": "🏛️"},
            {"title": "Sirine Peringatan Dini", "desc": "Sirine panjang 3 menit = peringatan darurat/evakuasi", "icon": "🔔"}
        ]
        
        # Data tas darurat
        self.emergency_kit = [
            {"name": "Air Minum", "desc": "Minimal 3 liter per orang untuk 3 hari", "icon": "💧"},
            {"name": "Makanan Darurat", "desc": "Makanan kaleng, biskuit, mi instan, energy bar", "icon": "🍝"},
            {"name": "P3K & Obat-obatan", "desc": "Perban, plester, antiseptik, obat rutin, oralit", "icon": "🏥"},
            {"name": "Senter & Baterai", "desc": "Senter LED terang, baterai cadangan minimal 2 set", "icon": "🔦"},
            {"name": "Radio Portabel", "desc": "Radio baterai atau dynamo untuk update info resmi", "icon": "📻"},
            {"name": "Pakaian & Selimut", "desc": "Pakaian ganti 3 set per orang, jaket tebal, selimut", "icon": "👕"},
            {"name": "Masker & Sanitizer", "desc": "Masker N95 (minimal 5 per orang), handsanitizer", "icon": "😷"},
            {"name": "Dokumen Penting", "desc": "KK, KTP, akta kelahiran, sertifikat tanah", "icon": "📄"},
            {"name": "Peralatan", "desc": "Pisau lipat, tali nilon, plester lakban, peluit", "icon": "🔧"},
            {"name": "Uang Tunai", "desc": "Uang pecahan kecil dan besar. Minimal Rp500.000 per orang", "icon": "💰"}
        ]
        
        # Data peringatan cuaca
        self.weather_warnings = [
            {"type": "🌊 BANJIR BANDANG", "locations": "Garut, Sukabumi, Cianjur, Bandung", "time": "10-12 Juni", "severity": "high", 
             "desc": "Potensi banjir bandang dengan ketinggian mencapai 2-3 meter"},
            {"type": "⛰️ TANAH LONGSOR", "locations": "Puncak, Banjarnegara, Sumedang", "time": "11-14 Juni", "severity": "high", 
             "desc": "Lereng curam rawan longsor. Hindari perjalanan malam hari"},
            {"type": "🌋 GUNUNG SEMERU", "locations": "Lumajang, Malang", "time": "Aktif - AWAS", "severity": "high", 
             "desc": "Status AWAS (Level IV). Radius 8 km dari puncak dilarang beraktivitas"},
            {"type": "🔥 KARHUTLA", "locations": "Riau, Kalimantan Selatan, Sumsel", "time": "12-16 Juni", "severity": "medium", 
             "desc": "Titik api meningkat 45% dibanding kemarin"},
            {"type": "🌪️ ANGIN PUTING BELIUNG", "locations": "Indramayu, Cirebon, Brebes", "time": "11 Juni", "severity": "medium", 
             "desc": "Potensi angin kencang >60 km/jam"},
            {"type": "🌊 GELOMBANG TINGGI", "locations": "Selat Sunda, Samudra Hindia", "time": "10-13 Juni", "severity": "high", 
             "desc": "Tinggi gelombang 4-6 meter. Nelayan dilarang melaut"}
        ]
    
    def get_top_provinces(self, limit=12):
        """Mendapatkan provinsi dengan kejadian tertinggi"""
        sorted_provinces = sorted(self.provinces, key=lambda x: x["totalEvents"], reverse=True)
        return sorted_provinces[:limit]
    
    def get_province_by_name(self, name):
        """Mendapatkan data provinsi berdasarkan nama"""
        for p in self.provinces:
            if p["name"].lower() == name.lower():
                return p
        return None
    
    def get_cities_by_province(self, province_name):
        """Mendapatkan daftar kota berdasarkan provinsi"""
        prov = self.get_province_by_name(province_name)
        return prov["cities"] if prov else []
    
    def search_provinces(self, keyword):
        """Mencari provinsi berdasarkan keyword"""
        keyword = keyword.lower()
        return [p for p in self.provinces if keyword in p["name"].lower()]
    
    def get_news_by_severity(self, severity=None):
        """Mendapatkan berita berdasarkan tingkat keparahan"""
        if severity:
            return [n for n in self.news if n["severity"] == severity]
        return self.news
    
    def get_statistics_summary(self):
        """Mendapatkan ringkasan statistik"""
        total_events = sum(p["totalEvents"] for p in self.provinces)
        total_refugees = sum(p["refugees"] for p in self.provinces)
        total_deaths = sum(p["deaths"] for p in self.provinces)
        total_injured = sum(p["injured"] for p in self.provinces)
        
        darurat_count = len([p for p in self.provinces if p["status"] == "darurat"])
        waspada_count = len([p for p in self.provinces if p["status"] == "waspada"])
        
        return {
            "total_events": total_events,
            "total_refugees": total_refugees,
            "total_deaths": total_deaths,
            "total_injured": total_injured,
            "darurat_count": darurat_count,
            "waspada_count": waspada_count,
            "total_provinces": len(self.provinces)
        }
    
    def get_risk_level_color(self, risk):
        """Mendapatkan warna berdasarkan tingkat risiko"""
        if risk >= 75:
            return "#e07a5f"
        elif risk >= 50:
            return "#e0a343"
        else:
            return "#3d9b6d"
    
    def get_risk_level_text(self, risk):
        """Mendapatkan teks tingkat risiko"""
        if risk >= 75:
            return "TINGGI"
        elif risk >= 50:
            return "SEDANG"
        else:
            return "RENDAH"
    
    def update_timestamp(self):
        """Update timestamp terakhir"""
        self.last_update = datetime.now()
    
    def get_last_update_str(self):
        """Mendapatkan string timestamp terakhir"""
        return self.last_update.strftime("%d/%m/%Y %H:%M:%S")