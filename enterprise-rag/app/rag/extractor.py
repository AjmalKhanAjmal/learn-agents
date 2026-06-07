# from pypdf import PdfReader


# def extract_pdf_text(path):
#     reader = PdfReader(path)

#     text = ""

#     for page in reader.pages:
#         text += page.extract_text() + "\n"

#     return text


from pypdf import PdfReader

def extract_pdf_text(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text