import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove (cid:xxx) patterns
    text = re.sub(r'\(cid:\d+\)', '', text)
    
    # 3. Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # 4. NLP Processing
    doc = nlp(text)
    
    cleaned_tokens = []
    
    for token in doc:
        # Remove stopwords and short words
        IMPORTANT_WORDS = ["ai","ml","sql","c","c++"]

        if not token.is_stop and(len(token.text) > 2 or token.text in IMPORTANT_WORDS):
            cleaned_tokens.append(token.text)
    
    return " ".join(cleaned_tokens)


# Testing
if __name__ == "__main__":
    from parser import extract_text_from_pdf
    
    resume_path = "data/sample_resume.pdf"
    raw_text = extract_text_from_pdf(resume_path)
    
    clean_text = preprocess_text(raw_text)
    
    print("----- CLEANED TEXT -----\n")
    print(clean_text[:1000])  # print first 1000 chars