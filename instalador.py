import subprocess 
import os,shutil
import winreg
class Instalador: 

    def __init__(self):

        pass
#Funcion para instalar las librerias de
    def instaladorDeLibrerias(paquete):
        subprocess.check_call([])
        pass

    def instaladorFFMPEG(self):
        try:
            destino_ffmpeg = "c:/ffmpeg"
            if os.path.exists(destino_ffmpeg):
                pass
            else: 
                shutil.copytree("ffmpeg",destino_ffmpeg )

            self.agregar_al_path(destino_ffmpeg)
        except Exception as e:
            return  "\n "+str(e) 
        
    
# Método para agregar al PATH del sistema usando winreg
    def agregar_al_path(self, nuevo_path):
        try:
            # Abre la clave de registro para las variables de entorno del sistema
            clave = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0, winreg.KEY_ALL_ACCESS
            )

            # Obtén el valor actual de la variable PATH
            valor_path, tipo = winreg.QueryValueEx(clave, "Path")

            # Si el nuevo path no está ya en el PATH, lo añade
            if nuevo_path not in valor_path:
                nuevo_valor_path = f"{valor_path};{nuevo_path}"
                winreg.SetValueEx(clave, "Path", 0, tipo, nuevo_valor_path)
                print("FFMPEG añadido al PATH del sistema.")

                # Notifica al sistema de los cambios en el entorno
                os.system(f"setx PATH \"%PATH%;{nuevo_path}\"")
            else:
                print("FFMPEG ya está en el PATH del sistema.")

            # Cierra la clave de registro
            winreg.CloseKey(clave)

        except Exception as e:
            print("Error al modificar el PATH en las variables de entorno del sistema:", str(e))
