import streamlit as st
import base64


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
    
#-----------------------------------------WELCOME PAGE--------------------------------------

st.title("Medaicon App")
set_background('C:/NLP-project/streamlit-app/widgets/medicine-capsules.png')
st.write("Welcome to Medaicon App!")
