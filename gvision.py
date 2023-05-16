from google.cloud import vision
from google.cloud.vision_v1 import types
import cv2
import numpy as np
import kyc_config as cfg

client = vision.ImageAnnotatorClient.from_service_account_file(cfg.gcv_api_key_path)
imgDelimiter = cv2.imread("delimiter3.png")


def get_text_response_from_path(BytesImage):
    output = None
    try:
        #if BytesImage.startswith('http') or BytesImage.startswith('gs:'):
        #    image = types.Image()
        #    image.source.image_uri = BytesImage
        #else:
        image = types.Image(content=BytesImage)

    except ValueError:
        output = "Cannot Read Input File"
        return output
    image_context = vision.ImageContext(language_hints = "id") 
    text_response = client.document_text_detection(image=image)
    document = text_response.full_text_annotation
    text = text_response.text_annotations
    


    return document


