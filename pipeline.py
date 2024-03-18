from modules.searcher import *
from utils.helper import *

def phase_1(detector, img):
    outputImage, listYoloBoxes = detector.get_output_image_and_yolo_boxes(img)
    return outputImage, listYoloBoxes

def phase_2(listYoloBoxes, img):
    listProductBarcodes = []
    listProductNames = []
    listItems = []
    searcher = ImageSearch(k=5)
    for yolo_box in listYoloBoxes:
        xyxy = yolo_box.xyxy[0]
        xmin = int(xyxy[0])
        ymin = int(xyxy[1])
        xmax = int(xyxy[2])
        ymax = int(xyxy[3])
        cropped_product = img[ymin:ymax, xmin:xmax]
        cropped_product = cv2.cvtColor(cropped_product, cv2.COLOR_BGR2RGB)
        cropped_product = Image.fromarray(cropped_product)
        list_product_barcodes, list_product_names = searcher.search(cropped_product)
        for i in range(len(list_product_barcodes)):
            listProductBarcodes.append(list_product_barcodes[i])
            listProductNames.append(list_product_names[i])
        product_info = {
                            "Barcode": list_product_barcodes,
                            "Bbox_coor": {
                                "xmax": xmin,
                                "xmin": xmin,
                                "ymax": ymax,
                                "ymin": ymin
                            }
                        }
        listItems.append(product_info)
    listProductBarcodes = list(set(listProductBarcodes))
    listProductNames = list(set(listProductNames))
    return listProductBarcodes, listItems, listProductNames