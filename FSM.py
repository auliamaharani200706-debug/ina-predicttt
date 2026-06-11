# ============ FILE 1: FSM.py ============
# State Machine untuk navigasi aplikasi

class DisasterAppFSM:
    """Finite State Machine untuk mengelola state aplikasi"""
    
    def __init__(self):
        # State yang tersedia
        self.states = [
            "dashboard",
            "prediksi",
            "panduan",
            "kontak",
            "donasi",
            "hubungi"
        ]
        
        # State saat ini
        self.current_state = "dashboard"
        
        # Mapping state ke nama tampilan
        self.state_to_display = {
            "dashboard": "📊 Dashboard",
            "prediksi": "🔮 Prediksi Bencana",
            "panduan": "📖 Panduan Aksi",
            "kontak": "📞 Kontak Darurat",
            "donasi": "🤝 Donasi",
            "hubungi": "💬 Hubungi Kami"
        }
        
        # Mapping state ke icon
        self.state_to_icon = {
            "dashboard": "📊",
            "prediksi": "🔮",
            "panduan": "📖",
            "kontak": "📞",
            "donasi": "🤝",
            "hubungi": "💬"
        }
    
    def transition_to(self, new_state):
        """Pindah ke state baru jika valid"""
        if new_state in self.states:
            self.current_state = new_state
            return True
        return False
    
    def get_current_display(self):
        """Mendapatkan nama tampilan untuk state saat ini"""
        return self.state_to_display.get(self.current_state, "📊 Dashboard")
    
    def get_current_icon(self):
        """Mendapatkan icon untuk state saat ini"""
        return self.state_to_icon.get(self.current_state, "📊")
    
    def get_menu_items(self):
        """Mendapatkan semua item menu"""
        return [
            {
                "state": state,
                "display": self.state_to_display[state],
                "icon": self.state_to_icon[state],
                "is_active": state == self.current_state
            }
            for state in self.states
        ]
    
    def reset(self):
        """Reset ke state awal"""
        self.current_state = "dashboard"