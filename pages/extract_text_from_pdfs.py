import streamlit as st
import base64
import pdf2image
from PIL import Image
import pytesseract
from pytesseract import Output, TesseractError
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt

st.set_page_config(page_title="PDF to Text")
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

set_background('C:/NLP-project/streamlit-app/widgets/image1.png')

html_temp = """
            <div style="background-color:{};padding:1px">
            
            </div>
            """

# st.markdown("""
#     ## :outbox_tray: Text data extractor: PDF to Text
    
# """)
# st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
st.markdown("""
    ## Text data extractor: PDF to Text
    
""")
languages = {
    'English': 'eng',
    'French': 'fra',
    'Arabic': 'ara',
    'Spanish': 'spa',
}

#-----------------------------------------PAGE CONFIGURATIONS--------------------------------------
#st.set_page_config(
#        page_title="Main page",
#)


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

with st.sidebar:
    st.sidebar.markdown(f"<style>{sidebar_styles}</style>", unsafe_allow_html=True)

    st.write(
        "<div style='display: flex; justify-content: center;'>"
        "<img src='https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png' style='width: 150px;'>"
        "</div>",
        unsafe_allow_html=True
    )
    st.title(":outbox_tray: PDF to Text")
    textOutput = st.selectbox(
        "How do you want your output text?",
        ('One text file (.txt)', 'Text file per page (ZIP)'))
    ocr_box = st.checkbox('Enable OCR (scanned document)')
    
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # How does it work?
    Simply load your PDF and convert it to single-page or multi-page text.
    """)
    
    

pdf_file = st.file_uploader("Load your PDF", type=['pdf', 'png', 'jpg'])
hide="""
<style>
footer{
	visibility: hidden;
    	position: relative;
}
.viewerBadge_container__1QSob{
  	visibility: hidden;
}
#MainMenu{
	visibility: hidden;
}
<style>
"""
st.markdown(hide, unsafe_allow_html=True)
if pdf_file:
    path = pdf_file.read()
    file_extension = pdf_file.name.split(".")[-1]
    
    if file_extension == "pdf":
        # display document
        with st.expander("Display document"):
            displayPDF(path)
        if ocr_box:
            option = st.selectbox('Select the document language', list(languages.keys()))
        # pdf to text
        if textOutput == 'One text file (.txt)':
            if ocr_box:
                texts, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: "+str(nbPages)+" in total"
                text_data_f = "\n\n".join(texts)
            else:
                text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                totalPages = "Pages: "+str(nbPages)+" in total"

            st.info(totalPages)
            st.download_button("Download txt file", text_data_f)
        else:
            if ocr_box:
                text_data, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: "+str(nbPages)+" in total"
            else:
                text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
                totalPages = "Pages: "+str(nbPages)+" in total"
            st.info(totalPages)
            zipPath = save_pages(text_data)
            # download text data   
            with open(zipPath, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP (txt)",
                    data=fp,
                    file_name="pdf_to_txt.zip",
                    mime="application/zip"
                )
    else:
        option = st.selectbox("What's the language of the text in the image?", list(languages.keys()))
        pil_image = Image.open(pdf_file)
        text = pytesseract.image_to_string(pil_image, lang=languages[option])
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Display Image"):
                st.image(pdf_file)
        with col2:
            with st.expander("Display Text"):
                st.info(text)
        st.download_button("Download txt file", text)

    
