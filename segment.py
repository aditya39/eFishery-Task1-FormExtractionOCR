from ultralytics import YOLO
import cv2
import numpy as np
import yaml
from gvision import get_text_response_from_path
import boto3
import pandas as pd
from io import BytesIO
from PIL import Image

# Open config.yaml File
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

frame_size = 640*640 # image input size

# Block type Textract
def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']

# Object detection function, input is image & model
def segment(file, model):
    
    # Convert File byte to array for OpenCV 
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image_copy = image.copy()
    print(image)

    # Inference YOLOv8
    result = model.predict(
        source=image, # image input
        conf=cfg["yolov8"]["conf"], # confidence threshold
        device='cpu',
        save_crop=True) # device (defualt 0 (gpu), change to "cpu" to use cpu)
    
    # Plot detection result image
    try:
        img_yolo = result[0].plot()
        # Retrive result information
        prob = result[0].boxes.cls
        problist = prob.tolist() # change type from tensor to list
        countListDetected = [len(problist)] # count total detected for each class
    except:
        pass

    try:
        # Retrive boundingbox information
        boxes = result[0].boxes.xyxy # get list xywh for each detected object
        boxes_list = boxes.tolist() # change type from tensor to list
        x1 = int(boxes_list[0][0])
        y1 = int(boxes_list[0][1])
        x2 = int(boxes_list[0][2])
        y2 = int(boxes_list[0][3])

        roi = image_copy[y1:y2, x1:x2]
        dfs = []
        tableImage = Image.fromarray(roi)
        buffered = BytesIO()
        tableImage.save(buffered, format='PNG')
    except:
        pass

    # Connect with AWS Textract
    client = boto3.client("textract", aws_access_key_id = "AKIAREXGVRHDK2LNPNHC",
                        aws_secret_access_key= "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", region_name = "us-east-2")
    response = client.analyze_document( Document={'Bytes': buffered.getvalue()}, FeatureTypes=['TABLES'])

    blocks = response['Blocks']
    tables = map_blocks(blocks, 'TABLE')
    cells = map_blocks(blocks, 'CELL')
    words = map_blocks(blocks, 'WORD')
    selections = map_blocks(blocks, 'SELECTION_ELEMENT')

    """for result1 in result:
        mask = result1.masks.cpu().numpy()
        masks = mask.masks.astype(bool)
        print("mask", masks)
        ori_img = result1.orig_img
        for m in masks:
            new = np.zeros_like(ori_img, dtype=np.uint8)
            new[m] = ori_img[m]
            cv2.imshow('p', new)"""
   
    """for i in range(len(result)):
        for j in range(len(result[i].masks)):
            segmenPoly = result[i].masks[j].xy
            
            x1 = int(result[i].boxes[j].xyxy[0][0])
            y1 = int(result[i].boxes[j].xyxy[0][1])
            x2 = int(result[i].boxes[j].xyxy[0][2])
            y2 = int(result[i].boxes[j].xyxy[0][3])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            for x in segmenPoly:
                for y in x:
                    y[0] = round(y[0])
                    y[1] = round(y[1])

            pts = np.array(segmenPoly[0], np.int32)
            pts = pts.reshape((-1, 1, 2))

            rect = cv2.minAreaRect(pts)

            # Extract the 4 corners of the bounding box from the minimum bounding rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            img = cv2.polylines(image, [pts], True, (255, 0, 0), 2)
            # Draw the bounding box on the original image
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            cv2.imwrite('wkwk.jpg', img)"""

    for table in tables.values():
        # Determine all the cells that belong to this table
        cells = [cells[cell_id] for cell_id in get_children_ids(table)]

        # Determine the table's number of rows and columns
        n_rows = max(cell['RowIndex'] for cell in cells)
        n_cols = max(cell['ColumnIndex'] for cell in cells)
        content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

        # Fill in each cell
        for cell in cells:
            cell_contents = [
                words[child_id]['Text']
                if child_id in words
                else selections[child_id]['SelectionStatus']
                for child_id in get_children_ids(cell)
            ]
            i = cell['RowIndex'] - 1
            j = cell['ColumnIndex'] - 1
            content[i][j] = ' '.join(cell_contents)

        # We assume that the first row corresponds to the column names
        df = pd.DataFrame(content[1:], columns=content[0])
        dfs.append(df)

    
   
    return df, countListDetected, roi



