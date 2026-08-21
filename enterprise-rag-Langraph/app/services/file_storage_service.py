import shutil

# import uuid
# from pathlib import Path


# class FileStorageService:

#     def __init__(self):

#         self.upload_dir = Path("uploads")

#         self.upload_dir.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#     def save(self, upload_file):

#         unique_name = f"{uuid.uuid4()}{Path(upload_file.filename).suffix}"

#         file_path = self.upload_dir / unique_name

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(upload_file.file, buffer)

import uuid
from pathlib import Path


class FileStorageService:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save(self, upload_file):
        unique_name = f"{uuid.uuid4()}{Path(upload_file.filename).suffix}"
        file_path = self.upload_dir / unique_name
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return file_path
