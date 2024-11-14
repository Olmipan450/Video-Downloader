import yt_dlp
from colorama import init, Fore
import requests,re
import os
class Descargador:

    #Constructor de la clase para obtener la información relevante del video 
    def __init__(self, url) -> None:
        self.formatos_disponibles = []
        self.audio_disponible=None
        self.video_index =None
        self.url=self._extraer_url_video(url) 
        self.error=None

        try:
        
            with yt_dlp.YoutubeDL({"skip_download": True, "quiet": False}) as downloader: 
                informacion = downloader.extract_info(self.url, download=False)

                for formato in informacion.get("formats",[]): 
                    formato_note = formato.get("format_note", "N/A")
                    resolucion = formato.get("resolution", "N/A Resolución")
                    ext = formato.get("ext", "N/A extensión")
                    peso = formato.get("filesize", "desconocido")


                    # Convierte el tamaño de bytes a megabytes si es posible y filtra las calidades de video disponibles
                    if isinstance(peso, int) and ext=="mp4" and ("720" in resolucion or "480" in resolucion or"1080"in resolucion)  :
                        peso = round(peso / (1024 * 1024), 2)
                        self.formatos_disponibles.append({
                        "format_id": formato.get("format_id"),
                        "ext": ext,
                        "resolucion": resolucion,
                        "calidad": formato_note,
                        "peso": peso
                    })

                mejor_audio = max(
                    (f for f in informacion.get("formats", []) if f.get("vcodec") == "none" and f.get("abr") is not None),
                    key=lambda f: f.get("abr", 0),
                    default=None
                )

                if mejor_audio:
                    peso_audio = mejor_audio.get("filesize", 0)
                    if isinstance(peso_audio, int):
                        peso_audio = round(peso_audio / (1024 * 1024), 2)
                    self.audio_disponible = {
                        "format_id": mejor_audio.get("format_id"),
                        "url": mejor_audio.get("url"),
                        "ext": mejor_audio.get("ext"),
                        "abr": mejor_audio.get("abr"),
                        "peso": peso_audio
                    }

            self.titulo = re.sub(r'[\\/*?:"<>|]', "_",informacion.get('title', None))
            self.duracion = self._convertir_duracion(informacion.get('duration', None))  # Duración en formato mm:ss
            self.miniatura = informacion.get('thumbnail', None)
            self.path_descarga=os.getcwd().replace("\\","/")+"/Descargas/videos"
            self.path_video=""
        except Exception as e: 
            self.error = str(e)
        

    def _extraer_url_video(self, url):
        # Expresión regular para extraer la URL del video de una posible lista de reproducción
        match = re.match(r'(https://www\.youtube\.com/watch\?v=[\w-]+)', url)
        if match:
            return match.group(1)
        else:
            raise ValueError("La URL no es válida o no se puede extraer el ID del video.")


    #Convertir la duración en segundos al formato mm:ss
    def _convertir_duracion(self, duracion_en_segundos):
        if duracion_en_segundos is not None:
            minutos = duracion_en_segundos // 60
            segundos = duracion_en_segundos % 60
            return f"{minutos:02d}:{segundos:02d}"
        return None        

    #Descargar un video a una de las tres resoluciones más comunes
    def descargaVideo(self,calidad:str,hook=None,audio=False,customlogger=None):
        if not audio:
            dic_calidades=self.calidadesDisponiblesMayorPeso()
            for res in dic_calidades : 
                if calidad in res:
                    configuracion = {'format': f"{dic_calidades[res][0]}+bestaudio[ext=m4a]/best",  # Combina el formato de video con el mejor audio, 
            'outtmpl':f'{self.path_descarga}/{self.titulo}',
            'progress_hooks':[hook] if hook else [],
            'logger':customlogger if customlogger else None
            }  # Define el formato de salida
                    print(Fore.GREEN,dic_calidades[res][0])
                    
                    with yt_dlp.YoutubeDL(configuracion) as downloaderVideo:
                        downloaderVideo.download(self.url)
                        self.path_video=self.path_descarga+"/"+self.titulo+".mp4"
                        
                        
        else:
            if self.audio_disponible:
                configuracion = {'format':self.audio_disponible["format_id"],
                                'merge_output_format': 'mp3',
                                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        }],
                        'progress_hooks':[hook] if hook else [],
                        'outtmpl':f'{self.path_descarga}/{self.titulo}%(ext)s',
                        'logger':customlogger if customlogger else None
                        }
                    
                with yt_dlp.YoutubeDL(configuracion) as downloaderAudio: 
                    downloaderAudio.download(self.url) 
                    self.path_video=self.path_descarga+"/"+self.titulo+".mp3"
                

    #Descargar la miniatura del video y devuelve el nombre de la imagen
    def descargaMiniatura(self): 
        if self.miniatura: 
            response = requests.get(self.miniatura)
            if response.status_code == 200: 
                with open(f"{"imagenes/imagenes_videos"}/{self.titulo}.jpg","wb") as imagen: 
                    imagen.write(response.content)
                    return "imagenes/imagenes_videos/"+self.titulo+".jpg"
    
    #Obtener una lista de las calidades disponibles para descarga 
    def calidadesDisponiblesMayorPeso(self):
        calidad480=[]
        calidad720=[]
        calidad1080=[]
        for formato in self.formatos_disponibles: 
            print(Fore.BLACK,formato)
            if "480" in formato["resolucion"] : 
                calidad480.append(formato["peso"])
            if "720" in formato["resolucion"]: 
                calidad720.append(formato["peso"])
            if "1080" in formato["resolucion"]: 
                calidad1080.append(formato["peso"])
        calidades={}
        for formato in self.formatos_disponibles: 
            if max(calidad480,default=0) == formato.get("peso",-1) and "480" in formato["resolucion"]: 
                calidades[formato["resolucion"]]= [formato["format_id"],max(calidad480,default=0)]
            if max(calidad720,default=0) == formato.get("peso",-1) and "720" in formato["resolucion"]: 
                calidades[formato["resolucion"]]= [formato["format_id"],max(calidad720,default=0)]
            if max(calidad1080,default=0) == formato.get("peso",-1) and "1080" in formato["resolucion"]: 
                calidades[formato["resolucion"]]= [formato["format_id"],max(calidad1080,default=0)] 
        
        return calidades



#url = "https://www.youtube.com/watch?v=Y4nEEZwckuU&list=RDnhOhFOoURnE&index=8&ab_channel=Ayase%2FYOASOBI"
#descargador = Descargador(url)
#print(descargador.titulo)
#print(descargador.duracion)
#print(descargador.miniatura) 
#for formato in descargador.formatos_disponibles: 
#    if "480" in formato["resolucion"] or "720" in formato["resolucion"] or "1080" in formato["resolucion"]: 
#        print(formato)
#print(descargador.calidadesDisponiblesMayorPeso())
#descargador.descargaVideo("720","",audio=True)
#print(descargador.audio_disponible["peso"],"MB")
#print(descargador.calidades_disponibles) 
#print(descargador.descargaMiniatura())
#descargador.descargaVideo("1080p")
