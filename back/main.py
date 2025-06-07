from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, Any
from label_map import label_map
import tensorflow as tf 
import numpy as np
import cv2 
import os


app = FastAPI()

os .environ["TF_ENABLE_ONEDNN_OPTS"]=0
MODEL_DIR = 'ssd_mobilenet_v2_coco/saved_model'

model = tf.saved_model.load(str(MODEL_DIR))

infer = model.signatures ['serving_default']

def run_inference (image:np.ndarray)->Dict[str,any]:
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis,...]

    detections = infer (input_tensor)
    return detections


@app.get("/")

@app.post("/predict")
async def predict(file:UploadFile =File(...))->JSONResponse:
    contents = await file.read()
    image = np.array(cv2.imdecode(np.frombuffer(contents,np.
                                                uint8),cv2.IMREAD_COLOR))
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detections = run_inference(image_rgb)
    num_detections = int (detections.pop('num_detections'))
    detections = {
        key: value[0, :num_detections].numpy() for key, value()in detections.items()
    }
    for key in detections:
        detections[key] = detections[key].tolist()
        results=[]


async def root():
    return {"message":"hello world"}

items = {
    1:{"name":"jose", "description":"Instructor"},
      2:{"name":"jose", "description":"Estudent"},
        3:{"name":"jose", "description":"Estudent"},
}

@app.get ("/items/{item_id}")
def get_item(item_id:int):
    item = items.get(item_id)
    if item is None:
        return{"error":"item not found"},404
    return item