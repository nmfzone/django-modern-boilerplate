import filetype
import os
import uuid
from core.settings import MEDIA_ROOT
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict


class UploadedFileWrapper(UploadedFile):
    def __init__(self, file=None, name=None, content_type=None, size=None,
                 charset=None, content_type_extra=None, base_uploaded_file=None):
        super().__init__(file, name, content_type, size, charset, content_type_extra)
        self.base_uploaded_file = base_uploaded_file

    def store(self, path=None):
        image_bytes = ContentFile(self.base_uploaded_file.read())
        extension = filetype.guess(image_bytes).extension

        img_uuid = "{0}.{1}".format(uuid.uuid4(), extension)
        upload_path = os.path.join(MEDIA_ROOT, str(path or '').lstrip('/'), img_uuid)

        final_path = default_storage.save(upload_path, image_bytes)

        return final_path

    def open(self, mode=None):
        self.base_uploaded_file.open(mode)
        return self

    def chunks(self, chunk_size=None):
        return self.base_uploaded_file.chunks(chunk_size)

    def multiple_chunks(self, chunk_size=None):
        return self.base_uploaded_file.multiple_chunks(chunk_size)

    def _get_name(self):
        return self.base_uploaded_file._get_name()

    def _set_name(self, name):
        self.base_uploaded_file._set_name(name)

    def __getattr__(self, name):
        if self._has_method('__getattr__'):
            return self.base_uploaded_file.__getattr__(name)

        return getattr(self.base_uploaded_file, name)

    def _has_method(self, name):
        method = getattr(self.base_uploaded_file, name, None)
        return method and callable(method)

    def __repr__(self):
        return self.base_uploaded_file.__repr__()

    def __str__(self):
        return self.base_uploaded_file.__str__()

    def __iter__(self):
        return self.base_uploaded_file.__iter__()

    def __len__(self):
        return self.base_uploaded_file.__len__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.base_uploaded_file.__exit__(exc_type, exc_value, tb)


def transform_uploaded_files(files):
    files = files or MultiValueDict()
    for file in files:
        obj = files.get(file)
        files.setlist(file, [
            UploadedFileWrapper(
                obj.file,
                obj.name,
                obj.content_type,
                obj.size,
                obj.charset,
                obj.content_type_extra,
                obj
            )
        ])
    return files
