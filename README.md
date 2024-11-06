# Aplikasi Text-to-Speech TikTok dengan PyQt

Aplikasi sederhana ini memungkinkan Anda untuk mengubah teks menjadi suara menggunakan API Text-to-Speech TikTok, dengan antarmuka pengguna grafis (GUI) yang dibangun menggunakan PyQt.

## Fitur

*   Mengubah teks menjadi suara dengan berbagai pilihan suara dari TikTok.
*   Memutar audio yang dihasilkan.
*   Mengunduh audio yang dihasilkan dalam format MP3.
*   Antarmuka pengguna yang modern dengan tema gelap.


## Instalasi

1.  Pastikan Anda telah menginstal Python 3.7 atau yang lebih baru.
2.  Install library yang dibutuhkan:
    ```bash
    pip install PyQt5 requests pygame
    ```
3.  Buat file `config.json` di direktori yang sama dengan script Python, dan isi dengan session ID TikTok Anda:
    ```json
    {
      "session_id": "YOUR_SESSION_ID_HERE"
    }
    ```

## Penggunaan

1.  Jalankan script Python: `python main.py`
2.  Masukkan teks yang ingin diubah menjadi suara.
3.  Pilih kategori dan indeks suara.
4.  Klik tombol "Generate Audio".
5.  Klik tombol "Play" untuk memutar audio.
6.  Klik tombol "Download" untuk mengunduh audio.

## Requirements

*   Python 3.7+
*   PyQt5
*   requests
*   pygame

## Catatan

*   Anda perlu mendapatkan session ID TikTok yang valid untuk menggunakan aplikasi ini.
*   API TikTok dapat berubah sewaktu-waktu, sehingga aplikasi ini mungkin tidak selalu berfungsi.

## Lisensi

MIT License