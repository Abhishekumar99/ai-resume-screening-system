import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text


# Testing
if __name__ == "__main__":
    resume_path = "data/sample_resume.pdf"
    extracted_text = extract_text_from_pdf(resume_path)
    
    print("----- Extracted Resume Text -----")
    print(extracted_text)