import onnxruntime as ort
import torchvision.transforms as transforms
from PIL import Image
from fastapi import FastAPI, UploadFile
import io

app = FastAPI(title="Resnet18 ONNX Live")

try:
    sess = ort.InferenceSession("resnet18.onnx", providers=["CPUExecutionProvider"])
    print("ONNX Loaded")
except:
    sess = ort.InferenceSession("03-advanced/app/resnet18.onnx", providers=["CPUExecutionProvider"])
    print("ONNX Loaded")

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

import json, urllib.request
CLASSES = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json").read())

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile):
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).numpy()
    outputs = sess.run(None, {"input": tensor})
    pred_id = int(outputs[0].argmax())
    return {"prediction": CLASSES[pred_id] if pred_id < len(CLASSES) else f"class_{pred_id}", "class_id": pred_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)