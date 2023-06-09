import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import re

def limpiar_nombre_archivo(nombre_archivo):
    nombre_archivo = re.sub(r'[^a-zA-Z0-9_.-]', '_', nombre_archivo)
    return nombre_archivo

def obtener_extension(url):
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif']
    nombre_archivo = os.path.basename(urlparse(url).path)
    extension = os.path.splitext(nombre_archivo)[1].lower()
    if extension in extensiones_validas:
        return extension
    return '.jpg'  # Extensión predeterminada si no es reconocida

def descargar_imagenes(url):
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

def main():
    url = input("Ingresa la dirección de la página web: ")
    descargar_imagenes(url)

if __name__ == '__main__':
    main()
