import os
from os.path import abspath
from modules.detector import Detector
from modules.searcher import ImageSearch
from utils.split_and_merge_file import merge_files


def initAllCacheFolder():
	if not os.path.exists(abspath(os.getenv('INPUT_IMG_FOLDER'))):
		os.makedirs(abspath(os.getenv('INPUT_IMG_FOLDER')))
	if not os.path.exists(abspath(os.getenv('OUTPUT_IMG_FOLDER'))):
		os.makedirs(abspath(os.getenv('OUTPUT_IMG_FOLDER')))

def initModel():
	detector = Detector()
	return detector