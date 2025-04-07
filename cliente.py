#Código para Colab
img_url = "https://raw.githubusercontent.com/dafcorg/servimos/refs/heads/main/img/YellowLabradorLooking_new.jpg"
img_data = requests.get(img_url).content
print(img_data)
#------------------ NUeva Celda
from PIL import Image
import io

# Verificar si la imagen es válida ANTES de enviarla
try:
    img = Image.open(io.BytesIO(img_data))
    img.show()  # o img.save("verificacion.jpg")
    print("Imagen válida en cliente")
except Exception as e:
    print("Error al abrir la imagen en el cliente:", e)

#-----------------------
import requests

url = "URL_Servidor/predict"
# Enviar como archivo binario (bien formado)
files = {
    "file": ("dog.jpg", img_data, "image/jpeg")
}

response = requests.post(url, files=files)
print(response.status_code)
print(response.json())
