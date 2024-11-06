import io
import sys
import json
import base64
import requests
import pygame

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QFileDialog,
)
from PyQt5.QtGui import QPalette, QColor

API_BASE_URL = f"https://api16-normal-v6.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"

VOICE_OPTIONS = {
    "id": ["id_001"],
    "disney": ["en_us_ghostface", "en_us_chewbacca", "en_us_c3po", "en_us_stitch", "en_us_stormtrooper", "en_us_rocket"],
    "english": ["en_au_001", "en_au_002", "en_uk_001", "en_uk_003", "en_us_001", "en_us_002", "en_us_006", "en_us_007", "en_us_009", "en_us_010"],
    "europe": ["fr_001", "fr_002", "de_001", "de_002", "es_002"],
    "america": ["es_mx_002", "br_001", "br_003", "br_004", "br_005"],
    "asia": ["jp_001", "jp_003", "jp_005", "jp_006", "kr_002", "kr_003", "kr_004"],
    "singing": ["en_female_f08_salut_damour", "en_male_m03_lobby", "en_female_f08_warmy_breeze", "en_male_m03_sunshine_soon"],
    "other": ["en_male_narration", "en_male_funny", "en_female_emotional"]
}

def tiktok_tts(session_id, text, voice_category="id", voice_index=0):
    """
    Mengubah teks menjadi suara menggunakan API TikTok.

    Args:
        session_id: Session ID TikTok yang valid.
        text: Teks yang akan diubah menjadi suara.
        voice_category: Kategori suara (default: "id").
            Pilihan: "id", "disney", "english", "europe", "america", 
                    "asia", "singing", "other".
        voice_index: Indeks suara dalam kategori (default: 0).

    Returns:
        bytes: Data audio dalam bentuk bytes.
    """
    try:
        # Mendapatkan daftar suara untuk kategori yang dipilih
        voices = VOICE_OPTIONS.get(voice_category)
        if not voices:
            raise ValueError(f"Kategori suara '{voice_category}' tidak valid.")

        # Memeriksa apakah indeks suara valid
        if voice_index < 0 or voice_index >= len(voices):
            raise ValueError(
                f"Indeks suara tidak valid untuk kategori '{voice_category}'."
            )

        # Memilih suara berdasarkan kategori dan indeks
        text_speaker = voices[voice_index]

        # Melakukan request ke API
        response = requests.post(
            f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={text}&speaker_map_type=0&aid=1233",
            headers={"User-Agent": USER_AGENT, "Cookie": f"sessionid={session_id}"},
        )

        # Memeriksa response
        response.raise_for_status()  # Raise HTTPError untuk bad responses (4xx or 5xx)
        data = response.json()

        if data["message"] == "Couldn't load speech. Try again.":
            raise ValueError(
                "Error: Session ID tidak valid atau masalah dengan API TikTok."
            )

        # Mengembalikan data audio sebagai bytes
        return base64.b64decode(data["data"]["v_str"])

    except (requests.exceptions.RequestException, ValueError) as e:
        raise e

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Inisialisasi pygame mixer
        pygame.mixer.init()

        self.setWindowTitle("Aplikasi Text-to-Speech TikTok")
        self.setGeometry(100, 100, 400, 300)

        # Atur tema gelap
        self.set_dark_theme()

        # Variabel untuk menyimpan data audio
        self.audio_data = None

        # Layout utama
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # Label judul
        title_label = QLabel("Text-to-Speech TikTok")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; margin-bottom: 20px;"
        )
        main_layout.addWidget(title_label)

        # Input teks
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Masukkan teks di sini")
        self.text_input.setStyleSheet(
            "padding: 10px; border: 1px solid #ccc; border-radius: 5px;"
        )
        main_layout.addWidget(self.text_input)

        # Dropdown kategori suara
        self.voice_category_dropdown = QComboBox()
        self.voice_category_dropdown.addItems(VOICE_OPTIONS.keys())
        self.voice_category_dropdown.setStyleSheet(
            "padding: 10px; border: 1px solid #ccc; border-radius: 5px;"
        )
        main_layout.addWidget(self.voice_category_dropdown)

        # Dropdown indeks suara
        self.voice_index_dropdown = QComboBox()
        self.voice_index_dropdown.addItems(
            [str(i) for i in range(len(VOICE_OPTIONS["id"]))]
        )  # Default to "id" category
        self.voice_category_dropdown.currentIndexChanged.connect(
            self.update_voice_index_dropdown
        )
        self.voice_index_dropdown.setStyleSheet(
            "padding: 10px; border: 1px solid #ccc; border-radius: 5px;"
        )
        main_layout.addWidget(self.voice_index_dropdown)

        # Tombol generate
        generate_button = QPushButton("Generate Audio")
        generate_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            """
        )
        generate_button.clicked.connect(self.generate_audio)
        main_layout.addWidget(generate_button)

        # Layout untuk tombol Play dan Download
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Tombol play
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)  # Awalnya nonaktif karena belum adaaudio
        button_layout.addWidget(self.play_button)

        # Tombol download
        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet(
            """
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0077a3;
            }
            """
        )
        self.download_button.clicked.connect(self.download_audio)
        self.download_button.setEnabled(False)  # Awalnya nonaktif karena belum ada audio
        button_layout.addWidget(self.download_button)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)

    def update_voice_index_dropdown(self):
        selected_category = self.voice_category_dropdown.currentText()
        self.voice_index_dropdown.clear()
        self.voice_index_dropdown.addItems(
            [str(i) for i in range(len(VOICE_OPTIONS[selected_category]))]
        )

    def generate_audio(self):
        try:
            # Baca session ID dari file config.json
            with open("config.json", "r") as f:
                config = json.load(f)
            session_id = config.get("session_id")

            if not session_id:
                raise ValueError("Session ID tidak ditemukan di config.json")

            text = self.text_input.text()
            voice_category = self.voice_category_dropdown.currentText()
            voice_index = self.voice_index_dropdown.currentIndex()

            # Generate audio dan simpan ke variabel self.audio_data
            self.audio_data = tiktok_tts(session_id, text, voice_category, voice_index)

            QMessageBox.information(self, "Berhasil", "Audio berhasil digenerate!")
            self.play_button.setEnabled(True)
            self.download_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def play_audio(self):
        try:
            # Putar audio dari memori
            pygame.mixer.music.load(io.BytesIO(self.audio_data))
            pygame.mixer.music.play()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memutar audio: {e}")

    def download_audio(self):
        try:
            # Buka dialog untuk memilih lokasi penyimpanan
            filename, _ = QFileDialog.getSaveFileName(
                self, "Simpan Audio", "output.mp3", "Audio Files (*.mp3)"
            )
            if filename:
                # Simpan audio ke file
                with open(filename, "wb") as f:
                    f.write(self.audio_data)
                QMessageBox.information(self, "Berhasil", f"Audio disimpan di {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengunduh audio: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())