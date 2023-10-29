# Streamlit App

This is a Streamlit web application that allows users to convert PDF documents into text files.

It also provides a pipeline for performing Optical Character Recognition (OCR) on PDF documents and extracting Named Entities using spaCy's NER model. 
The pipeline is designed to handle PDF files, convert them to text, and then apply Named Entity Recognition to extract important information such as Disease, Symptoms, Cause and treatement (based on the training annotations data that the spacy model has been trained on).
## Features

- Load PDF files for text extraction.
- Choose between single text file output or separate text files for each page.
- Enable OCR (Optical Character Recognition) for scanned documents.
- Display PDF documents within the app.
- Support for multiple languages for OCR.
- Text Preprocessing.
- Named Entity Recognition (NER) for annotated data.
- Generating a CSV file (column names : labels, rows corresponding to them : entities extracted from the text).

## How to Use

1. Upload Your PDF: Click the "Load your PDF" button to upload your PDF file.

2. Choose Output Option: Select how you want the output text. You can choose between a single text file or separate text files for each page.

3. Enable OCR (Optional): Check the "Enable OCR" checkbox if you're dealing with scanned documents and want to perform OCR.

4. Extract Text: Click the "Extract Text" button to convert the PDF to text. The app will display the extracted text and the total number of pages.

5. Download Text: You can download the extracted text in either a single text file or a ZIP file containing separate text files for each page.

6. Clean Your Extracted Text :
   - Upload Your Text File
   - Click on the "Upload Your Text File" section.
   - Click the "Choose a text file" button and select the text file you want to clean (in .txt format).
   - Original Text: Once you've uploaded the file, you can view the original text in the "Original Text" expander.
   - Processed Text: The code will process the text, which includes lowercasing, tokenization, punctuation removal, stopword removal, and lemmatization.
   - You can view the cleaned text in the "Processed Text" expander.
   - Download Processed Text:
     If you're satisfied with the cleaned text, click the "Download your processed text" button to download the cleaned text as a .txt file.
7. Annotate Your Text (Optional):

If you want to annotate your text for Named Entity Recognition (NER), a link to an annotation website is provided.

### Note 

After manually annotating the data on the website, consider using the 'ner-tagging-text-classification (1).ipynb' notebook or any other code you might wanna create to train a custom NER model on you json file (annotations.json or train.json in my case).
To help increase the model's accuracy.

8. Test Your Model

- Perform Named Entity Recognition:

Click the "Perform Named Entity Recognition" button to apply the NER model to your text.

- Annotated Text:

The annotated text with recognized entities and labels will be displayed.

- Generate CSV File:

After performing NER, click the "Generate CSV File" button to create a CSV file containing recognized entities and labels.
The CSV file will be displayed below the button.


## Installation

1. Clone this repository:
```bash
   git clone https://github.com/imenbkr/NER-project/streamlit-app.git
```
2. Before using this code, you need to install the required Python libraries.
You can do this using pip by running the following command in your terminal or command prompt:
```pip install -r path/to/requirements.txt```

3. Additionally, you'll need to adjust the path to the custom spaCy NER model named "model-best" for Named Entity Recognition.
You can find it in the streamlit-app folder.
You might also need to adjust the path to the background images in the app.

5. Run the Streamlit app:
- go to your ./streamlit-app folder and type in the terminal (with the cd command)
- type the following command :

```bash
streamlit run home.py
```

## Screenshots

1. Home page

![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/4274943c-32d7-488c-b1cd-5f33e0a445f3)

2. Extract text from pdfs

![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/cca665b5-2cee-48ed-a1cb-df3551c7fbfa)
![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/09639231-dd70-427c-996b-ebd4ce4caac0)

3. Clean the extracted text

![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/594390b8-325a-4fd9-b085-2f9dbec4be5b)
![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/28c70007-90e4-4bd3-9098-59e077519105)
![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/b7b4c790-df01-4e06-88b5-3b4c5bc46ede)

If you want to annotate your text, here is a website that can help you!
[Click here to visit the website](https://tecoholic.github.io/ner-annotator/?fbclid=IwAR1Mc83YCkhzMJTHurwW0-utUFZa3mnlcqyTaau0J0oERDPh0ZxGzTsj5Bc)

4. Perform Named Entity Recognition on your extracted text 

![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/0bf44ab0-d385-4939-ba5c-2dc016bd1040)
![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/c3d9b8fa-8623-4094-a2ee-7f26978689d8)
![image](https://github.com/LaroussiBENYOUNES/ChatBot.NLP/assets/104791884/3d57a59d-f131-4b1c-99e1-eebaa826d3df)


## Credits

### Libraries and Resources

* Streamlit: Used for creating interactive web applications in Python.

* pdfminer: Used for extracting text from PDF documents.

* spaCy: Used for Natural Language Processing (NLP) tasks, including Named Entity Recognition (NER).

* nltk: Used for natural language processing tasks such as tokenization and stopword removal.

* pdf2image: Used for converting PDF pages to images for OCR.

* pytesseract: Used for Optical Character Recognition (OCR) on images.

* fpdf: Used for generating PDF files.

* tqdm: Used for creating progress bars in loops.

* Pillow (PIL Fork): Used for image processing tasks.

* scikit-learn: Used for machine learning and data preprocessing.

* Custom spaCy NER Model

The custom spaCy NER model used in this project was trained on a specific dataset for Named Entity Recognition.

* NER Annotation Tool

NER Annotator: An external tool that can be used for annotating text data for NER tasks.
