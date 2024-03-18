import torch
from ultralytics import YOLO

if torch.cuda.is_available():
        device = 'cuda'
else:
    device = 'cpu'
    
class Detector:
    def __init__(self) -> None:
        self.model = YOLO('models/detector.pt')

    def get_output_image_and_yolo_boxes(self, img):
        result = self.model(img, device=device)
        outputImg = result[0].plot()
        bboxes = result[0].boxes
        listYoloBoxes = []
        if len(bboxes) > 0:
            for box in bboxes:
                listYoloBoxes.append(box)
        return outputImg, listYoloBoxes