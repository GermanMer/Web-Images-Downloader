#Este script de Python descarga imágenes desde una página web especificada por el usuario. Utiliza las bibliotecas requests y BeautifulSoup para obtener el contenido HTML de la página y encontrar las etiquetas de imagen. Luego, descarga cada imagen encontrada y las guarda en un directorio específico en el sistema de archivos local

import requests #para realizar solicitudes HTTP
from bs4 import BeautifulSoup #para analizar el contenido HTML de la página web
import os #para trabajar con directorios y rutas de archivo
from urllib.parse import urljoin, urlparse #para manipular y analizar URLs
import re #para trabajar con expresiones regulares

#FUNCIONES AUXILIARES:
def limpiar_nombre_archivo(nombre_archivo):
    '''Esta función toma un nombre de archivo y utiliza una expresión regular para eliminar cualquier carácter que no sea alfanumérico, punto, guión bajo o guión. Retorna el nombre de archivo limpio.'''
    nombre_archivo = re.sub(r'[^a-zA-Z0-9_.-]', '_', nombre_archivo)
    return nombre_archivo

def obtener_extension(url):
    '''Esta función toma una URL y devuelve la extensión del archivo en la URL. Utiliza la función os.path.basename para obtener el nombre de archivo de la URL y luego os.path.splitext para obtener la extensión. Si la extensión es válida (en este caso, .jpg, .jpeg, .png o .gif), se devuelve esa extensión. De lo contrario, se devuelve ".jpg" como extensión predeterminada.'''
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif']
    nombre_archivo = os.path.basename(urlparse(url).path)
    extension = os.path.splitext(nombre_archivo)[1].lower()
    if extension in extensiones_validas:
        return extension
    return '.jpg'  # Extensión predeterminada si no es reconocida

def descargar_imagenes(url):
    '''Esta función realiza la descarga de las imágenes desde la página web especificada'''
    try:
        # Realizar solicitud HTTP a la página web
        response = requests.get(url)
        response.raise_for_status()

        # Obtener el directorio base de la URL
        base_dir = urlparse(url).netloc

        # Crear el directorio para almacenar las imágenes
        directorio = os.path.join(os.getcwd(), 'Imagenes Descargadas', base_dir)
        os.makedirs(directorio, exist_ok=True)

        # Analizar el contenido HTML de la página web
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas las etiquetas de imagen (<img>)
        imagenes = soup.find_all('img')

        if not imagenes:
            print("No se encontraron imágenes en la página web.")
            return

        # Descargar cada imagen
        for imagen in imagenes:
            if 'src' in imagen.attrs:
                imagen_url = imagen['src']

                # Obtener la URL completa de la imagen
                imagen_url = urljoin(url, imagen_url)

                # Obtener el nombre de archivo de la URL
                nombre_archivo = os.path.basename(imagen_url)

                # Limpiar el nombre del archivo
                nombre_archivo = limpiar_nombre_archivo(nombre_archivo)

                # Obtener la extensión del archivo
                extension = obtener_extension(imagen_url)

                # Generar la ruta de archivo completa
                ruta_archivo = os.path.join(directorio, nombre_archivo + extension)

                # Descargar la imagen y guardarla en el directorio
                imagen_response = requests.get(imagen_url)
                imagen_response.raise_for_status()
                with open(ruta_archivo, 'wb') as archivo:
                    archivo.write(imagen_response.content)

        print("Todas las imágenes han sido descargadas satisfactoriamente.")

    except requests.exceptions.RequestException as e:
        print("Ocurrió un error al descargar las imágenes:", str(e))

#FUNCION PRINCIPAL
def main():
    url = input("Ingresa la dirección de la página web: ")
    descargar_imagenes(url)

if __name__ == '__main__': #Este bloque asegura que el código dentro de él solo se ejecute si el script se ejecuta directamente y no se importa como un módulo. Esto permite que el código dentro de la función main() se ejecute cuando el script se ejecuta desde la línea de comandos. En este caso, el usuario es solicitado a ingresar la dirección de la página web y luego se llama a la función descargar_imagenes(url) para iniciar la descarga de imágenes.
    main()
