from transformers import ViTImageProcessor, ViTModel
from transformers.utils import logging
import torch
import faiss

from utils.helper import load_array_from_file, get_embedding, get_product_barcode, get_product_name

logging.set_verbosity_error()

if torch.cuda.is_available():
    device_name = torch.device("cuda")
else:
    device_name = torch.device('cpu')

class ImageSearch:
    def __init__(self, k):
        self.image_processor = ViTImageProcessor.from_pretrained('models/VIT-Best-model')
        self.model = ViTModel.from_pretrained('models/VIT-Best-model').to(device_name)
        self.product_index = faiss.read_index('models/product_faiss_768.bin')
        self.product_codes = load_array_from_file('models/product_codes.npy')
        self.k = k

    def search(self, image):
        img_embeddings = get_embedding(self.image_processor, self.model, device_name, image)
        _, f_ids = self.product_index.search(img_embeddings, k=self.k)
        result =  [self.product_codes[id] for id in f_ids][0]
        list_product_codes = list(set(result))
        list_bar_codes = []
        list_product_names = []
        for product_code in list_product_codes:
            list_bar_codes.append(get_product_barcode(product_code))
            list_product_names.append(get_product_name(product_code))
        return list_bar_codes, list_product_names