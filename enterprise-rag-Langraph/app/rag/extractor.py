from pypdf import PdfReader

def extract_to_text(file_object):
    reader = PdfReader(file_object)
    text = ""
    # print("pages  -- ",reader.pages)
    
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    
    return text
    