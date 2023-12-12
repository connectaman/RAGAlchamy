import io
import os
from PIL import Image
import requests
  
def extract_text_from_ocr(img,ocr_engine="tesseract"):
    if ocr_engine == "tesseract":
        try:
            import pytesseract
            # Replace the below line with the tesseract path for windows, any other operating system comment the below line
            #pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
            pil_image = Image.open(img)
            text = pytesseract.image_to_string(pil_image)
            return text
        except:
            raise Exception("pytesseract not installed. If using Window please download tesseract and pass the path")
        
def ImageChartDataExtractor():
    """
    Initialize a TableExtractor object.
    
    Args:
        model_name (str): The name or path of the pre-trained model to be used for table extraction.
        
    Returns:
        None
    """
    # Import necessary libraries
    from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration
    import torch
    
    # Define the constructor
    def __init__(self, model_name="google/deploy") -> None:
        # Initialize the Pix2StructProcessor and Pix2StructForConditionalGeneration
        self.processor = Pix2StructProcessor.from_pretrained(model_name)
        self.model = Pix2StructForConditionalGeneration.from_pretrained(model_name)
        # Set the device to GPU if available, otherwise use CPU
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # Move the model to the selected device
        self.model.to(self.device)
        
    # Define the method to extract table from image
    def extract_chart_data_from_image(self, img) -> str:
        """
        Extracts the underlying data table from an image.

        Parameters:
            img (PIL.Image.Image): The image from which to extract the table.

        Returns:
            str: The decoded data table extracted from the image.
        """
        # Preprocess the image and generate the underlying data table
        inputs = self.processor(images=img, text="Generate underlying data table of the table/chart/figure below:", return_tensors="pt").to(self.device)
        # Generate predictions using the model
        predictions = self.model.generate(**inputs, max_new_tokens=512)
        # Decode the predictions and remove special tokens
        return self.processor.decode(predictions[0], skip_special_tokens=True)
        
        

def TableTransformer():
    """
    Initialize a TableExtractor object.
    
    Args:
        model_name (str): The name or path of the pre-trained model to be used for table extraction.
        
    Returns:
        None
    """
    # Import necessary libraries
    from transformers import AutoImageProcessor, TableTransformerModel
    import torch
    
    # Define the constructor
    def __init__(self, model_name="microsoft/table-transformer-detection") -> None:
        # Initialize the Pix2StructProcessor and Pix2StructForConditionalGeneration
        self.processor = AutoImageProcessor.from_pretrained(model_name)
        self.model = TableTransformerModel.from_pretrained(model_name)
        # Set the device to GPU if available, otherwise use CPU
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # Move the model to the selected device
        self.model.to(self.device)
        
    # Define the method to extract table from image
    def extract_table_from_image(self, img) -> str:
        """
        Extracts the underlying data table from an image.

        Parameters:
            img (PIL.Image.Image): The image from which to extract the table.

        Returns:
            str: The decoded data table extracted from the image.
        """
        # Preprocess the image and generate the underlying data table
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)
        # Generate predictions using the model
        predictions = self.model(**inputs)
        # Decode the predictions and remove special tokens
        return predictions