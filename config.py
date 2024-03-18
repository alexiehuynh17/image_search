import os
from os.path import abspath, join

GPU = False

ERROR_TABLE = [
    {
        "error_code": 0,
        "message":"<b> Unable to download image</b>"
    },
    {
        "error_code": 1,
        "message":"<b> Failed to open this image </b>"
    },
    {
        "error_code": 2,
        "message":"<b> Search unsuccessful</b>"
    },
     {
        "error_code": 3,
        "message":"<b> Base64 is empty</b>"
    },
    {
        "error_code": 4,
        "message":"<b> Failed to decode base64</b>"
    },
]
 