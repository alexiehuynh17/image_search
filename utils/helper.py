import numpy as np
import torch
from PIL import Image
from transformers.utils import logging
import base64

# from modules.vit import VITModel
from utils.load_brand import *
import cv2 

logging.set_verbosity_error()

def base64_to_image(base64_data):
    img = None
    encoded_data = base64_data#.split(',')[1]
    np_img = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)
    return img

def load_array_from_file(file_name):
    # Load array from a file
    array = np.load(file_name)
    return array

def get_embedding(image_processor, model, device_name, img):
    inputs = image_processor(img, return_tensors="pt").to(device_name)
    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state
        embeddings = last_hidden_states[:, 0, :]
        np_embeddings = embeddings.cpu().numpy()
    return np_embeddings

def get_product_barcode(productCode):
    brandInfo = BrandInfo()
    return brandInfo[productCode]['Barcode']

def get_product_name(productCode):
    brandInfo = BrandInfo()
    return brandInfo[productCode]['Product name']

def get_boxes_coordinates(listYoloBoxes):
    listBboxes = []
    for yolo_box in listYoloBoxes:
        xyxy = yolo_box.xyxy[0]
        xmin = int(xyxy[0])
        ymin = int(xyxy[1])
        xmax = int(xyxy[2])
        ymax = int(xyxy[3])
        listBboxes.append([xmin, ymin, xmax, ymax])
    return listBboxes

def get_cropped_product(listBboxes, img):
    listCroppedProduct = []
    for bbox in listBboxes:
        cropped_product = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        cropped_product = cv2.cvtColor(cropped_product, cv2.COLOR_BGR2RGB)
        listCroppedProduct.append(Image.fromarray(cropped_product))
    return listCroppedProduct

