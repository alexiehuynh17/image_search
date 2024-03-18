from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask, jsonify, make_response, render_template, request
from flask_restful import Api, Resource, reqparse
from search import getImageSimilarity, getImageSimilarityBase64
from utils.init import initAllCacheFolder, initModel



initAllCacheFolder()
productDetector = initModel()
app = Flask(__name__)
api = Api(app)

class Index(Resource):
	def get(self):
		return 'Image Search'

class ImageSearchV1(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str, help="Image link to valid", required=True, location="json")
        parser.add_argument("brand", type=str, required=True, location="args", default="vota")
        self.req_parser = parser

    def post(self):
        url = self.req_parser.parse_args(strict=True).get("url", "")
        brand = self.req_parser.parse_args(strict=True).get("brand", None)
        results = getImageSimilarity(productDetector, url, brand)
        return jsonify(results)

class ImageSearchV1Base64(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("base64", type=str, help="Base64 Image data", required=True, location="json")
        parser.add_argument("brand", type=str, required=True, location="args", default="vota")
        self.req_parser = parser

    def post(self):
        base64_data = self.req_parser.parse_args(strict=True).get("base64", "")
        brand = self.req_parser.parse_args(strict=True).get("brand", None)
        results = getImageSimilarityBase64(productDetector, base64_data, brand)
        return jsonify(results)

api.add_resource(Index, '/')
api.add_resource(ImageSearchV1, '/api/V1/image-search')
api.add_resource(ImageSearchV1Base64, '/api/V1/image-search-base64')

if __name__ == '__main__':
	app.run(debug=True)