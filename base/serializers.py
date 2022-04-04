import base64
import binascii
from mimetypes import guess_extension

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from rest_framework.fields import empty


class PassObject(object):
    pass


class BaseSerializer(serializers.ModelSerializer):
    pass_object = PassObject()

    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance

        if data is not empty:
            self.initial_data = data

        self.partial = kwargs.pop("partial", False)
        self.pass_object = kwargs.pop("pass_object", self.pass_object)

        kwargs.pop("many", None)

        read_only_fields = getattr(self.Meta, "read_only_fields", None)
        if read_only_fields is not None:
            if not isinstance(read_only_fields, (list, tuple)):
                raise TypeError(
                    "The `read_only_fields` option must be a list or tuple. "
                    "Got %s." % type(read_only_fields).__name__
                )

            if isinstance(read_only_fields, list):
                read_only_fields = read_only_fields + [
                    "is_deleted",
                    "created_at",
                    "updated_at",
                ]

            if isinstance(read_only_fields, tuple):
                read_only_fields = read_only_fields + (
                    "is_deleted",
                    "created_at",
                    "updated_at",
                )

            self.Meta.read_only_fields = read_only_fields

        super(BaseSerializer, self).__init__(instance, data, **kwargs)


class CustomBase64FileField(Base64FileField):
    """
    A django-rest-framework field for handling image-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """

    ALLOWED_TYPES = (
        "pdf",
        "docx",
        "doc",
        "xls",
        "xlsx",
    )
    INVALID_FILE_MESSAGE = "Please upload a file."
    INVALID_TYPE_MESSAGE = "The type of the image couldn't be determined."
    FILE_MIME_TYPE = ""

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, str):

            # Strip base64 header, get mime_type from base64 header.
            if ";base64," in base64_data:
                header, base64_data = base64_data.split(";base64,")
                self.FILE_MIME_TYPE = header.replace("data:", "")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)

            # Generate file name:
            file_name = self.get_file_name(decoded_file)

            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            if file_extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)

            complete_file_name = file_name + "." + file_extension
            data = SimpleUploadedFile(
                name=complete_file_name,
                content=decoded_file,
                content_type=self.FILE_MIME_TYPE,
            )

            return super(CustomBase64FileField, self).to_internal_value(data)

        raise ValidationError(
            "Invalid type. This is not an base64 string: {}".format(type(base64_data))
        )

    def get_file_extension(self, filename, decoded_file):
        return guess_extension(self.FILE_MIME_TYPE)[1:]
