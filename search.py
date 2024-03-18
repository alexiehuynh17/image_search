import os
from os.path import basename, join
from flask import request
from datetime import datetime
import cv2
import urllib
import config
import uuid
from pipeline import *

from utils.telegrambot import send_message, send_photo, send_error
from utils.helper import base64_to_image

def getImageSimilarity(detector, url, brand):
    if brand != "vota":
        return {"message": "<b> Unsupported brand! </b>"}
    filePath = None
    try:    
        fileName = basename(url)
        now = datetime.now()
        formatted_time = now.strftime("%H-%M-%S-%d-%m-%Y")
        filePath = join(os.getenv('INPUT_IMG_FOLDER'), formatted_time + '_' + fileName)
        urllib.request.urlretrieve(url, filePath)
    except Exception as e:
        # Send error message to telegram and return error if URL retrieval fails
        send_error(f"Fail to download image from url: {url}")
        return {"message":"<b> Download this file unsuccessful</b>"}
    
    # Extract file name from the URL
    fileName = basename(url)
    img = None
    raw_img_url = ''
    detected_img_url = ''
    if filePath is not None:
        try:
            img = cv2.imread(filePath)
        except:
            send_error(f"Fail to open image from url: {url}")
            return config.ERROR_TABLE[1]["message"]
    if img is not None:
        try:
            raw_img_url = str(request.host_url).replace('http','https') + filePath
            outputImage, listYoloBoxes = phase_1(detector, img)
            now = datetime.now()
            formatted_time = now.strftime("%H-%M-%S-%d-%m-%Y")
            save_path = join(os.getenv('OUTPUT_IMG_FOLDER'), formatted_time + '_' + fileName)
            cv2.imwrite(save_path, outputImage)
            detected_img_url = str(request.host_url).replace('http','https') + save_path
            listProductBarcodes, listItems, listProductNames = phase_2(listYoloBoxes, img)
            result = {
                        "Detected_image_link": detected_img_url,
                        "List_barcodes": listProductBarcodes, 
                        "List_items": listItems,
                        "Raw_image_link": raw_img_url
                    }
            message = (
                        f"<a href='{result['Raw_image_link']}'>Original Image</a>\n"
                        f"<a href='{result['Detected_image_link']}'>Output Image</a>\n"
                        f"List_barcodes: {result['List_barcodes']}\n"
                        f"List_product_names: {listProductNames}"
                    )
            send_photo(save_path)
            send_message(message)
            return result
        except Exception as e:
            print(e)
            send_photo(filePath)
            send_error(e)
            return config.ERROR_TABLE[2]["message"]
    send_photo(filePath)
    message =   (
                    f"<a href='{url}'>Original Image</a>\n"
                    "Message: Input Image is None!"
                )
    send_message(message)
    return config.ERROR_TABLE[1]["message"]

def getImageSimilarityBase64(detector, base64_data, brand):
    if brand != "vota":
        return {"message": "<b> Unsupported brand! </b>"}
    if len(base64_data) == 0:
        return config.ERROR_TABLE[3]["message"]
    
    def get_uuid_filename():
        return str(uuid.uuid4())
    
    filePath = None
    try:
        uuid_filename = get_uuid_filename()
        now = datetime.now()
        formatted_time = now.strftime("%H-%M-%S-%d-%m-%Y")
        filePath = join(os.getenv('INPUT_IMG_FOLDER'), formatted_time + "_" + uuid_filename + ".jpg")
        try:
            img = base64_to_image(base64_data)
            cv2.imwrite(filePath, img)
        except:
            img = None
    except Exception as e:
        # Send error message to telegram and return error if URL retrieval fails
        send_error(f"Fail to decode image base64: {base64_data}")
        return {"message":"<b> Fail to decode image base64</b>"}
    
    fileName = formatted_time + "_" + uuid_filename
    raw_img_url = ''
    detected_img_url = ''
    if img is not None:
        try:
            raw_img_url = str(request.host_url).replace('http','https') + filePath
            outputImage, listYoloBoxes = phase_1(detector, img)
            now = datetime.now()
            formatted_time = now.strftime("%H-%M-%S-%d-%m-%Y")
            save_path = join(os.getenv('OUTPUT_IMG_FOLDER'), formatted_time + '_' + fileName + '.jpg')
            cv2.imwrite(save_path, outputImage)
            detected_img_url = str(request.host_url).replace('http','https') + save_path
            listProductBarcodes, listItems, listProductNames = phase_2(listYoloBoxes, img)
            result = {
                        "Detected_image_link": detected_img_url,
                        "List_barcodes": listProductBarcodes, 
                        "List_items": listItems,
                        "Raw_image_link": raw_img_url
                    }
            message = (
                        f"<a href='{result['Raw_image_link']}'>Original Image</a>\n"
                        f"<a href='{result['Detected_image_link']}'>Output Image</a>\n"
                        f"List_barcodes: {result['List_barcodes']}\n"
                        f"List_product_names: {listProductNames}"
                    )
            send_photo(save_path)
            send_message(message)
            return result
        except Exception as e:
            print(e)
            send_photo(filePath)
            send_error(e)
            return config.ERROR_TABLE[2]["message"]
    return config.ERROR_TABLE[4]["message"]