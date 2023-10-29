import streamlit as st
import base64
import cv2
import subprocess
import numpy as np
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import json
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm

import io
import pandas as pd
import random
from spacy import displacy
from fpdf import FPDF
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import functions

import csv


#create a spaCy NLP pipeline
nlp = spacy.load("model-best")
#-----------------------------------------SET BACKGROUND IMAGE--------------------------------------
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def cooling_highlight(val):
    color = '#ACE5EE' if val else '#F2F7FA'
    return f'background-color: {color}'
#-----------------------------------------PAGE CONFIGURATIONS--------------------------------------

#define CSS styles for the sidebar
sidebar_styles = """
    .sidebar-content {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sidebar-image {
        max-width: 150px;
        display: block;
        margin: 0 auto;
    }
"""

def set_background_color(hex_color, color):
    style = f"""
        <style>
        .background-text {{
            background-color: {hex_color};
            padding: 5px; /* Adjust padding as needed */
            border-radius: 5px; /* Rounded corners */
            color: {color}; /* Text color */
        }}
        </style>
    """
    return style
#-----------------------------------------WELCOME PAGE--------------------------------------

st.title("Medaicon App")
set_background('C:/NLP-project/streamlit-app/widgets/medicine-capsules.png')
st.write("Medaicon App")
#-----------------------------------------SIDE BAR--------------------------------------
with st.sidebar:
    st.sidebar.markdown(f"<style>{sidebar_styles}</style>", unsafe_allow_html=True)

    st.write(
        "<div style='display: flex; justify-content: center;'>"
        "<img src='https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png' style='width: 150px;'>"
        "</div>",
        unsafe_allow_html=True
    )

    st.title("Welcome to the Medaicon App!")
    choice = st.radio("Navigation", ["Clean your extracted text",  "Test your model"], index=0)
    st.info("This project application helps you extract text from pdfs, train a spacy model on your annotated data and test it.")
    st.sidebar.success("Select an option above.")


#-----------------------------------------RADIO BUTTON CHOICES--------------------------------------

#define containers for each choice's content
if choice == "Clean your extracted text":
    st.title("Upload Your Text File")
    st.write("Text Cleaning :")
    uploaded_file = st.file_uploader("Choose a text file", type=(["txt"]))

    if uploaded_file is not None:
        raw_text= uploaded_file.read().decode('utf-8')
        file_details = {'file_name' : uploaded_file.name, "file_size": uploaded_file.size, "file_type": uploaded_file.type}
        st.write(file_details)
        
        col1, col2 = st.columns(2)
        with col1 :
            with st.expander("Original Text"):
                st.write(raw_text)
            with col2 :
                with st.expander("Processed Text"):
                    raw_text = functions.clean_text(raw_text)
                    st.session_state = raw_text
                    st.write(raw_text)
                    if st.button('Download your processed text'):
                        b64 = base64.b64encode(raw_text.encode()).decode()  # Corrected variable name and encoding
                        new_filename = "clean_text_result.txt"  # Fixed filename format
                        st.markdown('### Download File ###')
                        href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click here to download!</a>'
                        st.markdown(href, unsafe_allow_html=True)
        # NER website recommendation
        st.markdown("### If you want to annotate your text, here is a website that can help you! ###")
        st.markdown('[Click here](https://tecoholic.github.io/ner-annotator/?fbclid=IwAR1Mc83YCkhzMJTHurwW0-utUFZa3mnlcqyTaau0J0oERDPh0ZxGzTsj5Bc) to visit the website')
        st.markdown('#### An example of an annotated data ####')
        from PIL import Image
        image = Image.open('C:/NLP-project/streamlit-app/widgets/ner.png')
        st.image(image, width=800, use_column_width=False, caption='NER website')


            
elif choice == "Test your model":
    st.title('Named Entity Recognition')

    text = st.session_state 
   
    if st.button("Perform Named Entity Recognition"):
                    doc = functions.perform_named_entity_recognition(text)
                
                    html = functions.display_doc(doc)
                
                    if html is not None : 
                        html_string = f"<h3>{html}</h3>"
                        # display annotated text
                        st.markdown("Here's the Annotated text:")
                        st.markdown(set_background_color("#f2f7fa", 'black'), unsafe_allow_html=True)
                        styled_text = f"<div class='background-text'>{html_string}</div>"
                        st.markdown(styled_text, unsafe_allow_html=True)
                        detail = functions.details_dict(doc)
                        st.session_state = detail 
                            
                    else : 
                        st.write('none')

    if st.button('Generate CSV File '):
                        detail = st.session_state 
                        st.write(detail)
                        # Find the maximum length among the lists
                        max_length = max(len(detail[key]) for key in detail)

                        # Pad the lists with empty strings to have the same length
                        for key in detail:
                            detail[key] += [''] * (max_length - len(detail[key]))

                        # Create the DataFrame
                        df = pd.DataFrame(detail)
             
                        st.write(df)
                                                
                   


