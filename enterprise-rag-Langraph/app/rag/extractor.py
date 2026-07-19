# from pypdf import PdfReader

# def extract_to_text(file_object):
#     reader = PdfReader(file_object)
#     text = ""
#     # print("pages  -- ",reader.pages)
    
#     for page in reader.pages:
#         text += page.extract_text() + "\n"
    
    
#     return text
    

from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.logger import logger
from app.core.exceptions import PDFExtractionError


class PDFExtractor:
    """
    Service responsible for extracting text
    from PDF documents.
    """

    def extract(self, file_path: str) -> str:
        """
        Extract text from a PDF.

        Parameters
        ----------
        file_path : str

        Returns
        -------
        str
        """

        pdf_path = Path(file_path)

        if not pdf_path.exists():

            raise PDFExtractionError(
                f"PDF not found : {pdf_path}"
            )

        logger.info(
            "Starting PDF extraction : %s",
            pdf_path.name
        )

        try:

            reader = PdfReader(pdf_path)

            if reader.is_encrypted:

                raise PDFExtractionError(
                    "Encrypted PDF is not supported."
                )

            pages = []

            for page_number, page in enumerate(
                reader.pages,
                start=1
            ):

                page_text = page.extract_text()

                if page_text:

                    pages.append(page_text.strip())

                else:

                    logger.warning(
                        "No text found on page %d",
                        page_number
                    )

            document = "\n\n".join(pages)

            logger.info(
                "PDF extraction completed. Characters=%d",
                len(document)
            )

            return document

        except PdfReadError as error:

            logger.exception(
                "Invalid PDF file."
            )

            raise PDFExtractionError(
                "Unable to read PDF."
            ) from error

        except Exception as error:

            logger.exception(
                "Unexpected extraction error."
            )

            raise PDFExtractionError(
                str(error)
            ) from error