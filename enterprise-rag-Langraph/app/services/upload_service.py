# class UploadService:

#     def __init__(
#         self,
#         storage,
#         # extractor,
#         # cleaner,
#         # splitter,
#         # embedder,
#         # vector_store
#     ):

#         self.storage = storage
#         # self.extractor = extractor
#         # self.cleaner = cleaner
#         # self.splitter = splitter
#         # self.embedder = embedder
#         # self.vector_store = vector_store


class UploadService:

    def __init__(self, storage):

        self.storage = storage

    def upload(self, upload_file):

        saved_path = self.storage.save(upload_file)

        return {
            "message": "File uploaded successfully",
            "path": str(saved_path)
        }