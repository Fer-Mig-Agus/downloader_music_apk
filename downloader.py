import time

import yt_dlp
import os
import re
import requests
import validators
import argparse
import zipfile
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from config import (FFMPEG_INSTALL_PATH, FFMPEG_BIN_PATH, FFMPEG_ZIP_PATH,
                    FFMPEG_DOWNLOAD_URL, HTTP_HEADERS, DEFAULT_DOWNLOAD_FOLDER, YTDLP_OPTIONS)


class MusicDownloader:
    def __init__(self):
        """Inicializa las variables de la clase."""
        self.ffmpeg_verificado = False
        self.list_music=[]
        self.progress=False

    def instalar_ffmpeg(self,screen):
        """Verifica si FFmpeg está instalado y, si no, lo descarga e instala.

            Esta función realiza los siguientes pasos:
            1. Verifica si FFmpeg ya está instalado en el sistema.
            2. Si está instalado, muestra un mensaje y termina.
            3. Si no está instalado:
               - Crea la carpeta de instalación.
               - Descarga el archivo ZIP de FFmpeg.
               - Extrae y configura FFmpeg.
               - Agrega FFmpeg al PATH del sistema.

            Al finalizar, se actualiza la variable `self.ffmpeg_verificado` a `True` si la instalación es exitosa.

            Retorna:
                None
            """

        if self.ffmpeg_verificado or self.ffmpeg_esta_instalado():
            screen.show_popup_notification(f"✅ FFmpeg ya está instalado en '{FFMPEG_BIN_PATH}'.",'Notification')
            return

        screen.show_popup_notification(f"⚠️ FFmpeg no está instalado en '{FFMPEG_INSTALL_PATH}'. Descargando...",'Error')
        os.makedirs(FFMPEG_INSTALL_PATH, exist_ok=True)

        if self.descargar_ffmpeg():
            self.extraer_ffmpeg()
            os.environ["PATH"] += os.pathsep + FFMPEG_BIN_PATH
            self.ffmpeg_verificado = True
            screen.show_popup_notification("✅ FFmpeg instalado correctamente.",'Notification')
            self.progress=True
        else:
            screen.show_popup_notification("❌ No se pudo instalar FFmpeg.",'Error')

    def ffmpeg_esta_instalado(self):
        """Verifica si FFmpeg ya está instalado en el sistema.

            La función comprueba la existencia de los archivos ejecutables de FFmpeg (`ffmpeg.exe`) y `ffprobe.exe`
            en la ruta de instalación especificada (`FFMPEG_BIN_PATH`).

            Retorna:
                bool: `True` si ambos archivos existen, indicando que FFmpeg está instalado.
                      `False` si alguno de los archivos no está presente.
            """
        ffmpeg_executable = os.path.join(FFMPEG_BIN_PATH, "ffmpeg.exe")
        ffprobe_executable = os.path.join(FFMPEG_BIN_PATH, "ffprobe.exe")
        return os.path.exists(ffmpeg_executable) and os.path.exists(ffprobe_executable)

    def descargar_ffmpeg(self):
        """Descarga el archivo ZIP de FFmpeg desde la URL oficial.

           La función realiza los siguientes pasos:
           1. Envía una solicitud HTTP GET a `FFMPEG_DOWNLOAD_URL` para descargar el archivo ZIP.
           2. Guarda el contenido en la ruta `FFMPEG_ZIP_PATH`, escribiendo en bloques de 1024 bytes.
           3. Si la descarga es exitosa, imprime un mensaje de confirmación y retorna `True`.
           4. Si ocurre un error durante la descarga, captura la excepción, muestra un mensaje de error y retorna `False`.

           Retorna:
               bool: `True` si la descarga fue exitosa.
                     `False` si ocurrió un error.
           """
        try:
            response = requests.get(FFMPEG_DOWNLOAD_URL, stream=True)
            with open(FFMPEG_ZIP_PATH, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print("✅ FFmpeg descargado con éxito.")
            return True
        except Exception as e:
            print(f"❌ Error al descargar FFmpeg: {e}")
            return False

    def extraer_ffmpeg(self):
        """Extrae el archivo ZIP de FFmpeg y configura su instalación.

            La función realiza los siguientes pasos:
            1. Abre el archivo ZIP de FFmpeg ubicado en `FFMPEG_ZIP_PATH`.
            2. Extrae su contenido en la ruta de instalación `FFMPEG_INSTALL_PATH`.
            3. Busca la carpeta extraída dentro de `FFMPEG_INSTALL_PATH`.
            4. Si se encuentra la carpeta extraída, mueve el subdirectorio `bin` a `FFMPEG_INSTALL_PATH`.
            5. Si la extracción es exitosa, muestra un mensaje de confirmación.
            6. Si ocurre un error durante la extracción o configuración, captura la excepción y muestra un mensaje de error.

            Retorna:
                None
            """
        try:
            with zipfile.ZipFile(FFMPEG_ZIP_PATH, 'r') as zip_ref:
                zip_ref.extractall(FFMPEG_INSTALL_PATH)

            extracted_folders = [f for f in os.listdir(FFMPEG_INSTALL_PATH) if
                                 os.path.isdir(os.path.join(FFMPEG_INSTALL_PATH, f))]
            if extracted_folders:
                extracted_folder = os.path.join(FFMPEG_INSTALL_PATH, extracted_folders[0])
                shutil.move(os.path.join(extracted_folder, "bin"), FFMPEG_INSTALL_PATH)

            print("✅ FFmpeg descomprimido y configurado.")
        except Exception as e:
            print(f"❌ Error al extraer FFmpeg: {e}")


    @staticmethod
    def obtener_carpeta_descargas():
        """Obtiene la ruta de la carpeta 'Descargas' del usuario.

            La función devuelve la ruta absoluta de la carpeta de descargas del usuario
            en función del sistema operativo.

            Retorna:
                str: Ruta absoluta de la carpeta 'Descargas' del usuario.
            """
        return os.path.join(os.path.expanduser("~"), "Downloads")


    def obtener_nombre_carpeta(self,screen):
        """Obtiene la carpeta de descargas que el usuario desea utilizar.

         La función realiza los siguientes pasos:
         1. Obtiene la ruta de la carpeta de descargas del usuario.
         2. Solicita al usuario un nombre para la carpeta de descargas.
         3. Si el usuario presiona Enter, se usa la carpeta predeterminada (`DEFAULT_DOWNLOAD_FOLDER`).
         4. Si la carpeta predeterminada no existe, la crea y la devuelve.
         5. Si el usuario ingresa otro nombre y la carpeta ya existe, le pregunta si desea usarla.
         6. Si la carpeta no existe, la crea y la devuelve.

         Retorna:
             str: Ruta absoluta de la carpeta seleccionada o creada.
         """
        carpeta_descargas = self.obtener_carpeta_descargas()
        print('va a pedir el nombre')

        nombre_carpeta = self.solicitar_nombre_carpeta(screen)

        # Si el usuario presionó Enter, usar directamente la carpeta por defecto
        if nombre_carpeta == DEFAULT_DOWNLOAD_FOLDER:
            carpeta_destino = os.path.join(carpeta_descargas, nombre_carpeta)
            os.makedirs(carpeta_destino, exist_ok=True)  # Crear si no existe
            return carpeta_destino

        while True:
            carpeta_destino = os.path.join(carpeta_descargas, nombre_carpeta)

            if os.path.exists(carpeta_destino):
                nombre_carpeta = self.verificar_carpeta_existente(nombre_carpeta, carpeta_descargas)
                if nombre_carpeta is None:  # El usuario decidió usar la carpeta existente
                    return carpeta_destino
            else:
                return self.crear_carpeta(carpeta_destino,screen)

    def solicitar_nombre_carpeta(self,screen):
        """Solicita al usuario el nombre de la carpeta de descargas.

            Muestra un mensaje solicitando al usuario que ingrese un nombre de carpeta.
            Si el usuario presiona Enter sin ingresar nada, devuelve la carpeta predeterminada.

            Retorna:
                str: Nombre de la carpeta ingresada por el usuario o `DEFAULT_DOWNLOAD_FOLDER` si se presiona Enter.
            """
        print('Aqui deberia de pedir')
        input_file=screen.input_name_directory()
        print(f'Nombre recibido: {input_file}')

        # nombre_carpeta = input(
        #     f"Ingrese el nombre de la carpeta de descargas (Enter para usar '{DEFAULT_DOWNLOAD_FOLDER}'): ").strip()

        nombre_carpeta=input_file.strip()

        return nombre_carpeta if nombre_carpeta else DEFAULT_DOWNLOAD_FOLDER

    def verificar_carpeta_existente(self, nombre_carpeta, carpeta_descargas,screen):
        """Verifica si la carpeta ya existe y pregunta al usuario si desea usarla o ingresar un nuevo nombre.

            La función muestra un mensaje informando que la carpeta ya existe y le pide al usuario que elija una opción:
            1. Si el usuario responde "s", la función retorna `None`, indicando que se usará la carpeta existente.
            2. Si el usuario responde "n" o presiona Enter, se solicita un nuevo nombre de carpeta.
            3. Si el usuario ingresa una opción no válida, se muestra un mensaje de error y se vuelve a preguntar.

            Parámetros:
                nombre_carpeta (str): Nombre de la carpeta ingresada por el usuario.
                carpeta_descargas (str): Ruta de la carpeta de descargas.

            Retorna:
                str | None: `None` si el usuario decide usar la carpeta existente.
                            Un nuevo nombre de carpeta si el usuario elige cambiarla.
            """

        # screen.show_popup_notification(f"⚠️ La carpeta '{nombre_carpeta}' ya existe en {carpeta_descargas}.",'Notification')
        # opcion = input("¿Desea usarla? (s/n) o presione Enter para ingresar un nuevo nombre: ").strip().lower()

        option=screen.choose_election(f"⚠️ La carpeta '{nombre_carpeta}' ya existe en {carpeta_descargas}.¿Desea usarla?")

        if option:
            return None  # Indica que se usará la carpeta existente
        else:
            return self.solicitar_nombre_carpeta()  # Pedir otro nombre
        # else:
        #     print("❌ Opción no válida. Intente de nuevo.")
        #     return self.verificar_carpeta_existente(nombre_carpeta, carpeta_descargas)  # Volver a preguntar

    def crear_carpeta(self, carpeta_destino,screen):
        """Crea la carpeta de descargas si no existe y la devuelve.

           Si la carpeta especificada en `carpeta_destino` no existe, la función la crea y muestra un mensaje de confirmación.

           Parámetros:
               carpeta_destino (str): Ruta absoluta de la carpeta a crear.

           Retorna:
               str: Ruta de la carpeta recién creada.
           """
        os.makedirs(carpeta_destino)
        screen.show_popup_notification(f"✅ Carpeta '{os.path.basename(carpeta_destino)}' creada en {os.path.dirname(carpeta_destino)}.",'Notification')
        return carpeta_destino


    @staticmethod
    def obtener_info_playlist(url):
        """Obtiene la lista de videos de una playlist de YouTube.

            La función intenta extraer la información de la playlist utilizando `yt_dlp`,
            devolviendo una lista de URLs de los videos contenidos en la playlist.

            Pasos:
            1. Configura `yt_dlp` para extraer solo la lista de videos sin descargarlos.
            2. Intenta obtener la información de la playlist usando `yt_dlp.YoutubeDL()`.
            3. Si la extracción es exitosa, devuelve una lista de URLs de los videos de la playlist.
            4. Si ocurre un error, imprime un mensaje de advertencia y devuelve una lista vacía.

            Parámetros:
                url (str): URL de la playlist de YouTube.

            Retorna:
                list: Lista de URLs de los videos en la playlist. Devuelve una lista vacía si ocurre un error.
            """
        opciones = {'quiet': True, 'extract_flat': True}
        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    return [entry['url'] for entry in info['entries']]
        except Exception as e:
            print(f'⚠️ Error al obtener información de la playlist: {e}')
        return []

    def descargar_audio(self, url, carpeta):
        """Descarga el audio de un solo video de YouTube y lo guarda como archivo MP3.

            La función utiliza `yt_dlp` para extraer el audio del video en la mejor calidad disponible y lo convierte a formato MP3.

            Pasos:
            1. Copia la configuración de `YTDLP_OPTIONS`.
            2. Configura la salida del archivo de audio en la carpeta de destino.
            3. Especifica la ubicación de FFmpeg para la conversión.
            4. Intenta descargar y convertir el audio del video.
            5. Si la descarga es exitosa, muestra un mensaje de confirmación.
            6. Si ocurre un error, lo captura y muestra un mensaje de error.

            Parámetros:
                url (str): URL del video de YouTube.
                carpeta (str): Ruta absoluta donde se guardará el archivo MP3.

            Retorna:
                None
            """
        opciones = YTDLP_OPTIONS.copy()
        opciones['outtmpl'] = os.path.join(carpeta, '%(title)s.%(ext)s')
        opciones['ffmpeg_location'] = FFMPEG_BIN_PATH

        try:
            print('🎵 Descargando audio...')
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
            print('✅ Descarga completa.')
        except yt_dlp.utils.DownloadError as e:
            print(f"❌ Error al descargar el video: {e}")
            print("Finalizando la ejecución debido al error.")
            return

    def descargar_playlist(self, url, carpeta):
        """Descarga todos los videos de una playlist de YouTube en formato MP3.

           La función extrae la lista de videos de la playlist y los descarga uno por uno en la mejor calidad de audio disponible.

           Pasos:
           1. Obtiene la lista de videos de la playlist mediante `obtener_info_playlist()`.
           2. Si la playlist está vacía o no se pudo extraer, muestra un mensaje de error.
           3. Recorre la lista de videos y los descarga individualmente con `descargar_audio()`.
           4. Maneja errores individuales para que la descarga continúe si algún video falla.

           Parámetros:
               url (str): URL de la playlist de YouTube.
               carpeta (str): Ruta donde se guardarán los archivos MP3.

           Retorna:
               None
           """
        videos = self.obtener_info_playlist(url)

        if not videos:
            print("❌ No se pudo obtener la lista de videos. Intenta más tarde.")
            return

        print(f'📜 Descargando {len(videos)} videos de la playlist...')

        for index, video_url in enumerate(videos, start=1):
            print(f"🎵 Descargando {index}/{len(videos)}: {video_url}")

            try:
                self.descargar_audio(video_url, carpeta)
            except yt_dlp.utils.DownloadError as e:
                print(f"⚠️ Error al descargar el video {index}: {e}. Pasando al siguiente.")

        print("✅ Descarga de playlist finalizada.")

    def descargar_musica(self, url,screen):
        """Descarga un video o una playlist de YouTube en formato MP3.

            La función determina si la URL proporcionada corresponde a un solo video o a una playlist
            y ejecuta la descarga correspondiente.

            Pasos:
            1. Verifica si la URL es válida.
            2. Instala FFmpeg si aún no está instalado.
            3. Obtiene la carpeta de destino donde se guardarán los archivos.
            4. Limpia la URL para evitar parámetros innecesarios.
            5. Determina si la URL es de un video individual o de una playlist.
            6. Si es una playlist, llama a `descargar_playlist()`.
            7. Si es un solo video, llama a `descargar_audio()`.

            Parámetros:
                url (str): URL del video o playlist de YouTube.

            Retorna:
                None
            """

        if not validators.url(url):
            screen.show_popup_notification('La URL proporcionada no es válida.','Error')
            return

        screen.show_popup_notification('Link aceptado','Accept',self.instalar_ffmpeg(screen))
        # self.instalar_ffmpeg(screen)



        #
        #     # Ejecuta la instalación en un hilo separado y espera a que termine
        # thread = threading.Thread(target=self.instalar_ffmpeg, args=(screen,))
        # thread.start()
        # thread.join()  # Espera a que termine antes de continuar


        print('Salio del instalador')
        while not  self.progress:
            break
        carpeta = self.obtener_nombre_carpeta(screen)

        url_limpia = re.sub(r'&(?:start_radio=1|rv=[^&]*)', '', url)

        videos = self.obtener_info_playlist(url_limpia)

        if videos:
            print(f"📜 Se detectó una playlist con {len(videos)} videos.")
            self.descargar_playlist(url_limpia, carpeta)
        else:
            print("🎵 Descargando un solo video.")
            self.descargar_audio(url_limpia, carpeta)


    def run(self, url_input:str, screen):
        parser = argparse.ArgumentParser(description="Descargar música de YouTube en formato MP3.")
        parser.add_argument("url", nargs="?", help="URL del video o playlist de YouTube.")

        args = parser.parse_args()

        if not args.url:
            args.url = url_input

        # downloader = MusicDownloader()
        self.descargar_musica(args.url,screen)


