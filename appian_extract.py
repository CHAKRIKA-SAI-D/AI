import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# Set Tesseract OCR path if required (optional for Windows with PATH setup)
pytesseract.pytesseract.tesseract_cmd = r'tesseract'  # No need to hardcode if installed correctly

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""
    for page_num in range(len(pdf_document)):
        # Render the page as an image
        page = pdf_document[page_num]
        pix = page.get_pixmap()

        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Perform OCR using pytesseract
        extracted_text += pytesseract.image_to_string(img)
    return extracted_text

# Streamlit app
def main():
    st.title("PDF Text Extraction App")
    st.write("Upload a PDF file to extract text.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        st.write("Extracting text...")
        extracted_text = extract_text_from_pdf("temp.pdf")

        st.write("### Extracted Text:")
        st.text_area("", extracted_text, height=300)

    # Button to display the message
    if st.button("Process Further"):
        st.info("Adding soon")

if __name__ == "__main__":
    main()
