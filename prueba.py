

def on_nombreCaja_click(event,ayuda,nombreCaja):
    """Función que se llama cuando el usuario hace clic en la entrada."""
    if nombreCaja.get() == ayuda:
        nombreCaja.delete(0, "end")  # Borra el contenido
        nombreCaja.config(fg='grey')  # Cambia el color del texto

def on_focusout(event,ayuda,nombreCaja):
    """Función que se llama cuando la entrada pierde el enfoque."""
    if nombreCaja.get() == '':
        nombreCaja.insert(0, ayuda)
        nombreCaja.config(fg="grey")

def on_mouse_wheel(event,canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units") 

def centrar_ventana(ventana, ancho=300, alto=200):
    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular las coordenadas para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    
    # Establecer la geometría de la ventana para centrarla
    return f'{ancho}x{alto}+{x}+{y}'