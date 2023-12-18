# RAGAlchamy

RAGAlchamy is a groundbreaking Python package designed to revolutionize the way you interact with PowerPoint presentations. 
Our package empowers you to effortlessly extract and manipulate a wide range of content within PPT files, including text, charts, and even perform OCR (Optical Character Recognition) on images embedded in your presentations.


# Installation

1. Install / Check python verion -> python>=3.10
2. Install all required packages
```
pip install -r requirements.txt
```
3. Install tesseract
    - Windows
        - Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
        - Copy the path of tesseract.exe and update it in the code (ragalchemy->extractors->image.py , line 11)
        ```
        pytesseract.pytesseract.tesseract_cmd = r'PATH TO tesseract.exe'
        ```
    - Linux
        ```
        sudo apt update
        sudo apt-get install tesseract-ocr
        ```
4. Run the sample notebook 
