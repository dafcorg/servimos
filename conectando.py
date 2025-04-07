#Código para Google Colab cada -------- es una celda nueva
#-----------
!pip install -q fastapi uvicorn pyngrok nest-asyncio pillow torchvision torch python-multipart
#----------

#Crea una cuenta en:  
# https://dashboard.ngrok.com/signup
# Creación de un túnel seguro.

#---------
!ngrok config add-authtoken ************************************* #Remplaza *** por tu token
#____

from fastapi import FastAPI, UploadFile, File
import nest_asyncio
import uvicorn
from PIL import Image
import io
import requests
import time


# Parche para permitir async en Colab
nest_asyncio.apply()

# Crear app de FastAPI
app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contenido = await file.read()
    print(f"📂 Archivo recibido: {file.filename}")
    print(f"🧾 Tamaño: {len(contenido)} bytes")
    
    return {
        "filename": file.filename,
        "size_bytes": len(contenido)
    }

#------------------
from pyngrok import ngrok
import nest_asyncio
import uvicorn

nest_asyncio.apply()
public_url = ngrok.connect(8000)
print(f"🚀 Tu API está en: {public_url}/predict")
uvicorn.run(app, host="0.0.0.0", port=8000)

#------------------------
#################################
#CLIENTE
#################################
# Otra ventana

import requests

url = "URL/predict" 

img_url = "https://raw.githubusercontent.com/dafcorg/servimos/refs/heads/main/img/YellowLabradorLooking_new.jpg"
img_bytes = requests.get(img_url).content

response = requests.post(
    url,
    files={"file": ("dog.jpg", img_bytes, "image/jpeg")}
)

print(response.status_code)
print(response.json())

