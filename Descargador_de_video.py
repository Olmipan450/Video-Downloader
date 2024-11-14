import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import tkinter
from prueba import on_nombreCaja_click, on_focusout, on_mouse_wheel
from PIL import Image, ImageTk 
import youtube,instalador,CustomLogger
import re,os
import threading 


#Devolver de decimal a hexadecimal el espectro RGB
def RGB_Hexadecimal (rojo:int, verde:int, azul:int): 
    colorRGB="#%02x%02x%02x" % (rojo, verde, azul)
    return colorRGB




Debug = True
#Cuadros de video
def video_download(ventana, video, ruta_img_video, calidad,peso):
    cont_elemDescargados = tkinter.Frame(ventana)
    cont_elemDescargados.pack(pady=5, fill=tkinter.X, padx=10)
    
    # Configuramos la fila y columnas del contenedor para que tengan tamaños consistentes
    cont_elemDescargados.grid_rowconfigure(0, minsize=130)  # Ajuste para que las filas sean del mismo tamaño
    cont_elemDescargados.grid_columnconfigure(0, minsize=260)  # Ajuste para que la columna de la imagen tenga un tamaño consistente
    cont_elemDescargados.grid_columnconfigure(1, minsize=350)  # Ajuste para que la columna del título tenga un tamaño consistente
    cont_elemDescargados.grid_columnconfigure(2, minsize=60)   # Ajuste para que la columna del botón de borrar tenga un tamaño consistente
    
    # Elemento descargado
    img_video = ImageTk.PhotoImage(Image.open(ruta_img_video).resize((250, 120)))
    img_video_label = tkinter.Button(cont_elemDescargados, image=img_video,border=0, 
                                    command= lambda:[noAbrirCarpetas(video.path_video)])
    img_video_label.image = img_video
    
    duracion = tkinter.Label(cont_elemDescargados, text=video.duracion, font=("Arial", 10), bg="white")
    titulo = tkinter.Label(cont_elemDescargados, text=f"{video.titulo}\n{calidad} {peso} MB\n{video.path_descarga}", 
                        font=("Arial", 10, "bold"), justify="center", wraplength=300)
    borrar_video = tkinter.Button(command=lambda:[cont_elemDescargados.destroy(),contenedor_videos.update_idletasks(),
                                                contenedor_canva.config(scrollregion=contenedor_canva.bbox("all")),contenedor_canva.yview_moveto(0)],
                                                master=cont_elemDescargados, 
                                                image=basurero, width=50, height=50, border=0)
    #Barra de progreso e informacion de descarga
    barra_De_Progreso = tkinter.ttk.Progressbar(cont_elemDescargados,length=300,orient="horizontal")
    info_download = tkinter.Label(cont_elemDescargados,text="Iniciando",font=("Arial",9,"bold"))



    # Posicionamiento de los widgets en la cuadrícula
    img_video_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    duracion.grid(row=1, column=0, sticky="nsew")
    titulo.grid(row=0, column=1, rowspan=2, sticky="w", padx=5,pady=10)
    borrar_video.grid(row=0, column=2, rowspan=2, sticky="e", padx=10)
    barra_De_Progreso.grid(row=1,column=1,sticky="w",padx=20)
    info_download.grid(row=1,column=2,sticky="w",padx=1,pady=5)
    
    # Actualización del contenedor y el lienzo (canvas)
    contenedor_videos.update_idletasks()
    contenedor_canva.config(scrollregion=contenedor_canva.bbox("all"))
    #Inicializacion del logger
    logger = CustomLogger.CustomLogger(barra=barra_De_Progreso,contenedor=contenedor_videos)


    def monitorizacion(d):
        global Debug
        if Debug: 
            for datos in d: 
                print (datos)
            Debug=False

        if d["status"]=="downloading": 
            #Expresiones regulares para los valores de descarga
            clean_percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str'])
            clean_bytes = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', d["_downloaded_bytes_str"])
            clean_bytes_totales = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', d["_total_bytes_str"])
            porcentaje = float(clean_percent_str.replace("%",""))
            barra_De_Progreso["value"]= porcentaje
            info_download.config(text=f'{clean_bytes}/{clean_bytes_totales}')
            print(f"Descargando... {d['_percent_str']} completado a {porcentaje} (ETA: {d['eta']}s) bytes: {d["_downloaded_bytes_str"]} bytesTotales: {d["_total_bytes_str"]}")
            cont_elemDescargados.update_idletasks()


        #Funcion para no abrir carpetas si aun no se a acabado la descarga del video
    def noAbrirCarpetas(pathVideo):
        if barra_De_Progreso["value"] == 100:
            os.system(f'explorer /select,"{pathVideo.replace("/", "\\")}"')
            print(pathVideo)
    
    
    # Descarga en segundo plano si la calidad es "Audio" o video en caso contrario
    def descargar():

        if calidad == "Audio":
            video.descargaVideo(calidad="",audio=True,hook=monitorizacion,customlogger=logger)

        else: 
            print(calidad.replace("p",""))
            video.descargaVideo(calidad=calidad.replace("p",""),hook=monitorizacion,customlogger=logger)

            print("Mensajes de log:")

            if logger.messages: 
                barra_De_Progreso["value"]= 100
                cont_elemDescargados.update_idletasks()

    
    #Lanzar la descarga en segundo plano 
    hilo_descarga = threading.Thread(target=descargar)
    hilo_descarga.start()


    



#Generar opciones de descarga
def opciones_de_descarga(img_descarga, url, contenedor_videos):
    def cargar_video():
        # Instancia el objeto de video en un hilo separado
        video = youtube.Descargador(url)
        
        # Actualiza la UI después de que el hilo termine
        if video.error is None: 
            opciones.after(0, mostrar_informacion_video, video)
        else: 
            opciones.destroy()
            tkinter.messagebox.showwarning(title="Advertencia",message=video.error)
    
    def mostrar_informacion_video(video):
        # Una vez que el objeto video está listo, actualizamos la interfaz
        ruta_a_imagen = video.descargaMiniatura()
        imagen = ImageTk.PhotoImage(Image.open(ruta_a_imagen).resize((250, 120)))
        tiempo = video.duracion
        
        # Información del video
        img_video.config(image=imagen)
        img_video.image = imagen  # Mantener referencia de la imagen
        titulo.config(text=video.titulo)
        duracion.config(text="Duración: " + tiempo)
        path_descarga.config(text=video.path_descarga)
        
        # Actualizar las opciones de descarga
        pesoAudio = str(video.audio_disponible["peso"])
        formatos_disponibles = video.calidadesDisponiblesMayorPeso()

        #Actualizacion del boton de descarga y de descargas
        boton_cambiar_path.config(command=lambda: [obtener_path_de_descarga(label=path_descarga, video=video),opciones.lift()])
        boton_descarga_Audio.config(command=lambda:[opciones.destroy(),video_download(contenedor_videos,video,ruta_a_imagen,calidad="Audio",peso=pesoAudio)])
        boton_descarga_Video1080.config(command=lambda:[opciones.destroy(),video_download(contenedor_videos,video,ruta_a_imagen,calidad="1080p",peso=pesoVideo1080)])
        boton_descarga_Video720.config(command=lambda:[opciones.destroy(),video_download(contenedor_videos,video,ruta_a_imagen,calidad="720p",peso=pesoVideo720)])
        boton_descarga_Video480.config(command=lambda:[opciones.destroy(),video_download(contenedor_videos,video,ruta_a_imagen,calidad="480p",peso=pesoVideo480)])

        pesoVideo1080 = pesoVideo720 = pesoVideo480 = ""
        for formato in formatos_disponibles: 
            if "480" in formato:
                pesoVideo480 = str(formatos_disponibles[formato][1])
            if "720" in formato: 
                pesoVideo720 = str(formatos_disponibles[formato][1])
            if "1080" in formato: 
                pesoVideo1080 = str(formatos_disponibles[formato][1])
        
        # Actualización de la información de descarga
        formato_pesoAudio.config(text="MP3: " + pesoAudio + " MB")
        
        # Mostrar los botones solo si las resoluciones están disponibles
        if pesoVideo1080:
            formato_pesoVideo1080.config(text="1080p\nMP4: " + pesoVideo1080 + " MB")
            formato_pesoVideo1080.pack(padx=5)
            boton_descarga_Video1080.pack(padx=5)
        
        if pesoVideo720:
            formato_pesoVideo720.config(text="720p\nMP4: " + pesoVideo720 + " MB")
            formato_pesoVideo720.pack(padx=5)
            boton_descarga_Video720.pack(padx=5)
        
        if pesoVideo480:
            formato_pesoVideo480.config(text="480p\nMP4: " + pesoVideo480 + " MB")
            formato_pesoVideo480.pack(padx=5)
            boton_descarga_Video480.pack(padx=5)



    # Crear la ventana principal
    opciones = tkinter.Toplevel()
    opciones.iconphoto(False, foto1)
    opciones.title("Opciones de descarga")
    
    # Frame para la información del video
    info_video = tkinter.Frame(opciones)
    info_video.pack(padx=10, pady=10, side="left")
    
    # Inicialización de los widgets
    img_video = tkinter.Label(info_video, text="Cargando imagen...")
    img_video.grid(row=0, column=0)
    
    titulo = tkinter.Label(info_video, text="Cargando título...")
    titulo.grid(row=1, column=0)
    
    duracion = tkinter.Label(info_video, text="Duración: Cargando...", background="white", font=("Arial", 10))
    duracion.grid(row=2, column=0)
    
    path_descarga = tkinter.Label(info_video, text="Cargando ruta...", font=("Consolas", 10), wraplength=200)
    path_descarga.grid(row=3, column=0)
    
    boton_cambiar_path = tkinter.Button(info_video, text="Elegir ruta", padx=5, pady=5, border=1, 
                                        background=RGB_Hexadecimal(144, 238, 144),
                                        command=lambda: obtener_path_de_descarga(label=path_descarga, video=None))
    boton_cambiar_path.grid(row=4, column=0)
    
    # Frame para las opciones de descarga
    op_download = tkinter.Frame(opciones)
    op_download.pack(padx=10, pady=10, side="right")
    
    # Etiquetas y botones de descarga de audio
    audio = tkinter.Label(op_download, text="Audio", font=("Arial", 11, "bold"))
    formato_pesoAudio = tkinter.Label(op_download, text="MP3: Cargando...", background="grey")
    boton_descarga_Audio = tkinter.Button(op_download, image=img_descarga, border=0, 
                                        command=lambda: video_download(contenedor_videos, None, None, calidad="Audio"))
    
    # Etiquetas y botones de descarga de video
    video_label = tkinter.Label(op_download, text="Video", font=("Arial", 11, "bold"))
    
    formato_pesoVideo1080 = tkinter.Label(op_download, text="Cargando 1080p...", background="grey")
    boton_descarga_Video1080 = tkinter.Button(op_download, image=img_descarga, border=0, padx=5, pady=5,
                                            command=lambda: video_download(contenedor_videos, None, None, calidad="1080p"))
    
    formato_pesoVideo720 = tkinter.Label(op_download, text="Cargando 720p...", background="grey")
    boton_descarga_Video720 = tkinter.Button(op_download, image=img_descarga, border=0, padx=5, pady=5,
                                            command=lambda: video_download(contenedor_videos, None, None, calidad="720p"))
    
    formato_pesoVideo480 = tkinter.Label(op_download, text="Cargando 480p...", background="grey")
    boton_descarga_Video480 = tkinter.Button(op_download, image=img_descarga, border=0, padx=5, pady=5,
                                            command=lambda: video_download(contenedor_videos, None, None, calidad="480p"))

    # Colocar los widgets iniciales de audio y video
    audio.pack(padx=10)
    formato_pesoAudio.pack(padx=5)
    boton_descarga_Audio.pack(padx=5)
    video_label.pack(padx=10)

    # Lanzar el hilo para cargar el video
    hilo_youtube = threading.Thread(target=cargar_video)
    hilo_youtube.start()



#Accion para el boton de busqueda (lupa)
def Buscar(contenedor,img_descarga,url,ventanaPrincipal):
    #video_download(contenedor) 
    #Configurar la vista de los elementos

    if "https://www.youtube.com/" not in url:
        tkinter.messagebox.showwarning(title="Advertencia",message="Por favor, ingresa una url de video válida")
    else: 
        opciones_de_descarga(img_descarga,url,contenedor)
    

def obtener_path_de_descarga(label,video): 
    path=tkinter.filedialog.askdirectory(title="Selecciona una carpeta para la descarga:")
    if path:
        video.path_descarga = path
        label.configure(text=path)



#Declaracion de la ventana
ventana = tkinter.Tk()
ventana.config(background=RGB_Hexadecimal(211, 211, 211))
tamañolupa=30

#Imagenes para la apliación
icono = Image.open("imagenes/bobCholo.jpg")
lupaimg= Image.open("imagenes/R.jpg").resize((tamañolupa,tamañolupa-1))
foto1 = ImageTk.PhotoImage(icono)
fotolupa=ImageTk.PhotoImage(lupaimg)

basurero=ImageTk.PhotoImage(Image.open("imagenes/basura.png").resize((50,50)))
descarga=ImageTk.PhotoImage(Image.open("imagenes/descarga_icono.png").resize((20,20)))
#Configuracion de la ventana principal
ventana.geometry("750x600")
ventana.title("Video Downloader")
ventana.iconphoto(False,foto1)

#Confirma si ffmpeg esta insatalado, si da un error al intentar instalarlo cierra el programa
instalado =instalador.Instalador()
if  instalado.instaladorFFMPEG()!= None: 
    tkinter.messagebox.showerror("Fallo al instalar ffmpeg o al buscar el programa" ,instalado.instaladorFFMPEG())
    exit()

#Titulo de la aplicación
etiqueta = tkinter.Label(ventana, text = "Video Downloader",
        background=RGB_Hexadecimal(205,200,150),font=("Times New Roman",20))
etiqueta.pack(fill=tkinter.X) 

#Contenedor para la barra de busqueda
cont_busqueda = tkinter.Frame(ventana,background=RGB_Hexadecimal(211, 211, 211))
cont_busqueda.pack(pady=10)

#Barra de busqueda
textBox1= tkinter.Entry(master=cont_busqueda,font=("Arial",12))
textBox1.insert(0,"Escribe la URL")
textBox1.config(fg="grey",border=0,width=50)
textBox1.bind('<FocusIn>', lambda event:on_nombreCaja_click(event,"Escribe la URL",textBox1))
textBox1.bind('<FocusOut>', lambda event:on_focusout(event,"Escribe la URL",textBox1))
textBox1.pack(side="left",ipady=5) 

#Boton de busqueda
lupa = tkinter.Button(cont_busqueda,image=fotolupa,width=tamañolupa,height=tamañolupa-2)
lupa.config(border=0)
lupa.pack(side="right",pady=10)

#Crear un canva para el movimiento del raton 
contenedor_canva=tkinter.Canvas(ventana)
scrolBar_y = tkinter.Scrollbar(contenedor_canva,orient="vertical",command=contenedor_canva.yview)

#Contenedor para los elementos video (Cuadros de video)
contenedor_videos = tkinter.Frame(contenedor_canva)
contenedor_canva.create_window((0,0), window=contenedor_videos)
contenedor_canva.configure(yscrollcommand=scrolBar_y.set)
scrolBar_y.pack(side="right",fill="y")
contenedor_canva.pack(side="left", fill="both", expand=True)

lupa.config(command=lambda:Buscar(contenedor_videos,img_descarga=descarga,url=textBox1.get(),ventanaPrincipal=ventana))

#evento del raton
ventana.bind_all("<MouseWheel>", lambda event:on_mouse_wheel(event,contenedor_canva))
ventana.mainloop()

