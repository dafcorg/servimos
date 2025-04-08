#Código colab
#--------CELDA 3-------------

from fastapi import UploadFile, File, FastAPI
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
from torchvision import models, transforms
import time
import urllib.request


model = models.resnet18(pretrained=True)
model.eval()
device = torch.device("cpu")  
model.to(device)


transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  
        std=[0.229, 0.224, 0.225]
    )
])


labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
labels = urllib.request.urlopen(labels_url).read().decode("utf-8").splitlines()

app = FastAPI()

@app.post("/predict")
def predict(file: UploadFile = File(...)):
    try:
        start = time.time()
        contents = file.file.read()
        
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

        
        with torch.no_grad():
            output = model(input_tensor)
            pred_idx = output.argmax().item()
        

        label = labels[pred_idx]

        end = time.time()
        infer_time = round(end - start, 4)

        return JSONResponse(content={
            "prediction": label,
            "inference_time_sec": infer_time,
            "filename": file.filename
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
