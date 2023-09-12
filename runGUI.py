# pip install tk
# pip install Pillow
# pip install pytesseract
# pip install autocorrect
# pip install opencv-python
# pip install PyMuPDF

from tkinter import * # for GUI 
from tkinter import filedialog # for dialogbox window
from PIL import ImageTk, Image # for opening images  
import pytesseract # wrapper for tesseract engine  
from perform_ocr import TesseractOCR # for OCR
from spellchecker import correct_sentence # for text correction
from pre import preproc # for Image pre-processing
import fitz 


def extract_image_text(image_path):
    preproc.contrast(image_path)
    proc_out = TesseractOCR.extract_ocr('preprocessed.png')
    corrected_output = correct_sentence(proc_out)
    return corrected_output

def extract_pdf_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pdf_text=""

    # Loop through pages and extract text
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        # Convert the page to an image (you can specify DPI)
        page_image = page.get_pixmap()
        
        # Convert image to a Pillow Image object
        image = Image.frombytes("RGB", [page_image.width, page_image.height], page_image.samples)
        
        # Extract text using Pytesseract
        text = pytesseract.image_to_string(image)

        #   uncomment the following line if page number are required
        # pdf_text+=f"Page No.{page_number + 1}\n\n"+text+"\n"
        pdf_text+="\n"+text+"\n\n"
    return pdf_text
        

def extract_text(path):
    if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
        # Handle image files
        return extract_image_text(path)
    elif path.lower().endswith(('.pdf')):
        # Handle PDF files
        return extract_pdf_text(path)
    else:
        print("Unsupported file format")
        return ""

# button to start text extraction
def show_extract_button(path):
    extractBtn = Button(frame, text="Extract text", command=lambda: display_extracted_text(path), bg="cyan", fg="blue", pady=15,
                        padx=15, font=('Times', 15, 'bold'))
    extractBtn.grid(row=1, column=0, pady=10, padx=10, sticky='w')

# to display final extracted text to user
def display_extracted_text(path):
    extracted_text = extract_text(path)
    output_text.config(state=NORMAL)
    output_text.delete(1.0, END)
    output_text.insert(INSERT, extracted_text)
    output_text.config(state=DISABLED)

# resizing the input image to display appropriately
def resize_image(image, max_width, max_height):
    width, height = image.size
    if width > max_width or height > max_height:
        aspect_ratio = width / height
        if aspect_ratio > 1:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        # Resize the image with LANCZOS filter (anti-aliasing)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return resized_image
    else:
        return image

# dialogbox to upload image or pdf file
def upload():
    try:
        path = filedialog.askopenfilename()
        if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            # Handle image uploads
            image = Image.open(path)
        elif path.lower().endswith(('.pdf')):
            # Handle PDF uploads
            pdf_document = fitz.open(path)
            page = pdf_document[0]  # Upload the first page
            page_image = page.get_pixmap()
            image = Image.frombytes("RGB", [page_image.width, page_image.height], page_image.samples)
        else:
            print("Unsupported file format")
            return

        # Calculate target width and height as half of the screen dimensions
        max_width = root.winfo_screenwidth() // 2
        max_height = root.winfo_screenheight() // 2
        resized_img = resize_image(image, max_width, max_height)

        img = ImageTk.PhotoImage(resized_img)
        uploaded_img.configure(image=img)
        uploaded_img.image = img
        show_extract_button(path)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    except Exception as e:
        print(e)

# to scroll the page 
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root = Tk()
root.title("Welcome to Raghav's OCR App")

# Configure grid rows and columns to expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(row=0, column=0, rowspan=4, sticky='nsew')

scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, rowspan=4, sticky='ns')

canvas.configure(yscrollcommand=scrollbar.set)
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

uploadbtn = Button(frame, text="Upload an image or pdf", command=upload, bg="yellow", fg="brown", height=2, width=20,
                   font=('Times', 15, 'bold'))
uploadbtn.grid(row=0, column=0, padx=10, pady=10, sticky='w')

newline = Label(frame, text='\n')
newline.grid(row=1, column=0)

uploaded_img = Label(frame)
uploaded_img.grid(row=2, column=0)

# Bind mouse wheel event to the canvas
canvas.bind("<MouseWheel>", on_mousewheel)

# Add a Text widget for displaying OCR output
output_text = Text(frame, wrap=WORD, width=90, height=40, state=DISABLED)
output_text.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='w')

root.mainloop()