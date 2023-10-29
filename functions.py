import streamlit as st
from zipfile import ZipFile
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import base64
import spacy
import json
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm
from spacy.training.example import Example
from tqdm import tqdm
from spacy.util import minibatch, compounding
import random
from spacy import displacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import csv
import io

###################################### OCR & IMAGE TO TEXT ##############################################
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError

@st.cache_data
def images_to_txt(path, language):
    images = pdf2image.convert_from_bytes(path)
    all_text = []
    for i in images:
        pil_im = i
        text = pytesseract.image_to_string(pil_im, lang=language)
        # ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
        # ocr_dict now holds all the OCR info including text and location on the image
        # text = " ".join(ocr_dict['text'])
        # text = re.sub('[ ]{2,}', '\n', text)
        all_text.append(text)
    return all_text, len(all_text)

###################################### PDF TO TEXT ##############################################
@st.cache_data
def convert_pdf_to_txt_pages(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    size = 0
    c = 0
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(path):
      interpreter.process_page(page)
      t = retstr.getvalue()
      if c == 0:
        texts.append(t)
      else:
        texts.append(t[size:])
      c = c+1
      size = len(t)
    # text = retstr.getvalue()

    # fp.close()
    device.close()
    retstr.close()
    return texts, nbPages

@st.cache_data
def convert_pdf_to_txt_file(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(path):
      interpreter.process_page(page)
      t = retstr.getvalue()
    # text = retstr.getvalue()

    # fp.close()
    device.close()
    retstr.close()
    return t, nbPages

@st.cache_data 
def save_pages(pages):
  
  files = []
  for page in range(len(pages)):
    filename = "page_"+str(page)+".txt"
    with open("./file_pages/"+filename, 'w', encoding="utf-8") as file:
      file.write(pages[page])
      files.append(file.name)
  
  # create zipfile object
  zipPath = './file_pages/pdf_to_txt.zip'
  zipObj = ZipFile(zipPath, 'w')
  for f in files:
    zipObj.write(f)
  zipObj.close()

  return zipPath

def displayPDF(file):
  # Opening file from file path
  # with open(file, "rb") as f:
  base64_pdf = base64.b64encode(file).decode('utf-8')

  # Embedding PDF in HTML
  pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
  # Displaying File
  st.markdown(pdf_display, unsafe_allow_html=True)

#--------------------------------- Named Entity Recognition -----------------------------------
# Create a spaCy NLP pipeline
nlp = spacy.load("model-best")
# Named Entity Recognition and display functions
#@st.experimental_memo 
def perform_named_entity_recognition(text):
    doc = nlp(text)
    return doc

######COLOR GENERATOR FUNCTION ######
#@st.experimental_memo 
def color_gen(): #this function generates and returns a random color.
    random_number = random.randint(0,16777215) #16777215 ~= 256x256x256(R,G,B)
    hex_number = format(random_number, 'x')
    hex_number = '#' + hex_number
    return hex_number #generate color randomly

#####DISPLAY DOCUMENT FUNCTION########
#@st.experimental_memo 
def display_doc(doc):
    colors = {ent.label_: color_gen() for ent in doc.ents}
    options = {"ents": [ent.label_ for ent in doc.ents], "colors": colors}
    html = displacy.render(doc, style='ent', options=options, page=True, minify=True)
    return html
    #st.write(html, unsafe_allow_html=True)#display of entities recognition in text

#--------------------------------- Summary document -----------------------------------
#DETAILS EXTRACTION FUNCTION OF DOCUMENT(LABEL->ENTITIES) #
@st.cache_data
def details_dict(_doc):
    Details = {}
    for ent in _doc.ents:
    #     print(ent.ents,ent.label_)
        if(ent.label_ not in Details):
            Details[ent.label_]=[str(ent.ents[0])]
        else:
            if(str(ent.ents[0]).strip() not  in Details[ent.label_] ):
                Details[ent.label_].append(str(ent.ents[0]))
    return Details #return detail label+all his entities

@st.cache_data
def create_file_txt(dict_variable):
    #####
    #we must have details.txt file on our local machine
    text_file = open("details.txt", "w")
    #####
    Details=dict_variable

    for dic in Details:
        txt=dic.upper() +' : '
        for i in range(len(Details[dic])):
            if(i<len(Details[dic])-1):
                txt+=Details[dic][i]+' , '
            else:
                txt+=Details[dic][i]
        txt+='\n'
        text_file.write(txt)#close file
    text_file.close()

###################################### CLEAN TEXT BEFORE FEEDING IT TO THE NER MODEL ##############################################
@st.cache_data 
def clean_text(text):
    # Lowercase the text
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join the tokens back into a cleaned text
    cleaned_text = ' '.join(tokens)

    return cleaned_text
    
