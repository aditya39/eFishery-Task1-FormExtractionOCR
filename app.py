import yaml
import os
import numpy as np
import pandas as pd
import streamlit as st
from ultralytics import YOLO
from clearml import InputModel
from segment import segment
from st_aggrid import AgGrid

os.environ['CLEARML_CONFIG_FILE'] = "clearml.conf"

# Config the page layout to wide at default
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# Open Config File
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Create Sidebar
with st.sidebar:
    st.title("Project 1 - Form Extractor with OCR - Textract AWS") # Sidebar Title
    st.image("efisherylogolandscape.jpg") # Sidebar Logo
    st.divider()
    
    # Create select box to select YOLOv8 model
    st.header("Choose a Model")
    selectModel = st.selectbox("What YOLOv8 model you would like to choose?", 
                               ("YOLOv8 Nano", "YOLOv8 Small", "YOLOv8 Medium","YOLOv8 Large", "YOLOv8 Xtreme"))

    # If model selected, pick the model from ClearML IDModel
    if selectModel == "YOLOv8 Nano":
        model = InputModel(model_id=cfg["model"]["yolov8n"]) # model_id pickup from config.yaml
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Small":
        model = InputModel(model_id=cfg["model"]["yolov8s"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Medium":
        model = InputModel(model_id=cfg["model"]["yolov8m"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    if selectModel == "YOLOv8 Large":
        model = InputModel(model_id=cfg["model"]["yolov8l"])
        store_model = model.get_local_copy()
        model = YOLO(store_model)

    # Create an expander which explain more about the models difference
    expander = st.expander("See explanation about the model..", expanded=False)
    expander.write("""Xtreme model give the most accuracy while sacrifice performance speed, Nano is the fastest model but least accurate.
    \nYou can check Yolov8 models comparation by expanding image below..
                   Visit YOLO8 github link for more, https://github.com/ultralytics/ultralytics""")
    expander.image("yolo8_detail.png")

    
# Main Page Container
with st.container():
    st.title("Form Extractor with Textract by AWS")
    st.divider()

    # Create Browse File Action
    st.subheader("Upload Form Image")
    file = st.file_uploader("Upload Your Form Image Here", type=["jpg", "jpeg", "png"])

    # Check if file exist then call detect function by passing file image & model
    if file:
        # countListDetection consist of information how many for each vibrio class detected
        df, countListDetected, img_yolo = segment(file, model) 

        # Create container for show image
        with st.container():
            col1, col2 = st.columns(2) # Create two columns to place the image
            with col1:
                st.image(file)
                st.markdown("<p style='text-align: center; color: white;'>Original Image</p>", unsafe_allow_html=True)
            with col2:
                st.image(img_yolo)
                st.markdown("<p style='text-align: center; color: white;'>Detected Vibro by YOLOv8</p>", unsafe_allow_html=True)
            st.divider()

            cols=pd.Series(df.columns)

            for dup in cols[cols.duplicated()].unique(): 
                cols[cols[cols == dup].index.values.tolist()] = [dup + '.' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]

            # rename the columns with the cols list.
            df.columns=cols

            # Create download Excel & CVS button
            @st.cache_data
            # Function to export to csv
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8')
            csv = convert_df(df)

            # Export to excel and read it as byte
            df.to_excel("E:/Bekerja/Lamaran/eFishery/Project_1/program/Form Laporan Budi Daya Harian.xlsx")
            with open("Form Laporan Budi Daya Harian.xlsx", "rb") as template_file:
                template_byte = template_file.read()
            
            # Result Section
            st.header("Result of OCR Extraction")
            st.write("Click button below to download the result..")
            # Excel download button
            st.download_button(
                label="Download data as Excel",
                data=template_byte,
                file_name='Form Laporan Budi Daya Harian.xlsx',
                mime='application/octet-stream',
             )
            # CSV download button
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Form Laporan Budi Daya Harian.csv',
                mime='text/csv',
             )
            
            # Show table in page with Agrid from streamlit
            AgGrid(df)
          
         
       
                
    

  