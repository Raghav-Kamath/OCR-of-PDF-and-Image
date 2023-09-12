from pytesseract import pytesseract

try:
    from PIL import Image
except ImportError:
    print('Import Image Error')

class TesseractOCR:
    def extract_ocr(filename):
        try:
        #   To set tesseract path manually in the code. Note: it varies according to your installation.
            pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # apply tesseract ocr
            text = pytesseract.image_to_string(Image.open(filename))
            return text
        except Exception as e:
            print(e)
            return "Error"
    
# ocr=OCR()

# text=ocr.extract_ocr("preprocessed.png")
# print(text)


