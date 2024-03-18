import glob
import json
import os


class BrandInfo:
    def __init__(self) -> None:
        # jsonFilePath = glob.glob(os.path.join(os.getenv('JSON_BRAND'), '*.json'))
        jsonFilePath = glob.glob(os.path.join("brands", '*.json'))
        
        self.list_loaded = []
        for jsonFile in jsonFilePath:
            with open(jsonFile, 'r', encoding='utf-8') as f:
                self.list_loaded.append(json.load(f))

    def __getitem__(self, key):
        for idx, brand in enumerate(self.list_loaded):
            for product_code in brand:
                if key == product_code:
                    return self.list_loaded[idx][key]
        return None