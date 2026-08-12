import re

from app.core.logger import logger
# from app.core.exceptions import TextCleaningError

class TextCleaner:
    """
    Cleans extracted document text before chunking.
    """

    def clean(self, text: str) -> str:
        """
        Clean extracted text.

        Parameters
        ----------
        text : str

        Returns
        -------
        str
        """

        logger.info("Starting text cleaning.")

        try:

            if not text:

                return ""

            cleaned = text

            # Replace Windows line endings
            cleaned = cleaned.replace("\r\n", "\n")

            # Replace tabs with spaces
            cleaned = cleaned.replace("\t", " ")

            # Remove multiple spaces
            cleaned = re.sub(
                r"[ ]{2,}",
                " ",
                cleaned
            )

            # Remove 3 or more blank lines
            cleaned = re.sub(
                r"\n{3,}",
                "\n\n",
                cleaned
            )

            # Remove leading/trailing whitespace
            cleaned = cleaned.strip()

            logger.info(
                "Cleaning completed. Characters=%d",
                len(cleaned)
            )

            return cleaned

        except Exception as error:

            logger.exception(
                "Text cleaning failed."
            )

            # raise TextCleaningError(
            #     str(error)
            # ) from error