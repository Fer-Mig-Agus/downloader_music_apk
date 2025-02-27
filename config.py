import os

# 📌 Rutas de instalación de FFmpeg
FFMPEG_INSTALL_PATH = os.path.join(os.path.expanduser("~"), "ffmpeg")
FFMPEG_BIN_PATH = os.path.join(FFMPEG_INSTALL_PATH, "bin")
FFMPEG_ZIP_PATH = os.path.join(FFMPEG_INSTALL_PATH, "ffmpeg.zip")

# 📌 URL de descarga de FFmpeg
FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

# 📌 User-Agent para evitar bloqueos de YouTube
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 📌 Carpeta por defecto para descargas
DEFAULT_DOWNLOAD_FOLDER = "music_downloader"

# 📌 Opciones por defecto para yt-dlp
YTDLP_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'http_headers': HTTP_HEADERS  # Usar encabezados para evitar errores 403
}
