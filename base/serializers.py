import base64
import binascii
import uuid
from mimetypes import guess_extension

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from rest_framework.fields import FileField, empty


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


class Base64FieldMixin(object):
    EMPTY_VALUES = (None, "", [], (), {})

    @property
    def ALLOWED_TYPES(self):
        raise NotImplementedError

    @property
    def INVALID_FILE_MESSAGE(self):
        raise NotImplementedError

    @property
    def INVALID_TYPE_MESSAGE(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        self.trust_provided_content_type = kwargs.pop(
            "trust_provided_content_type", False
        )
        self.represent_in_base64 = kwargs.pop("represent_in_base64", False)
        super(Base64FieldMixin, self).__init__(*args, **kwargs)

    def get_file_extension(self, filename, decoded_file):
        raise NotImplementedError

    def get_file_name(self, decoded_file):
        return str(uuid.uuid4())

    def to_representation(self, file):
        if self.represent_in_base64:
            # If the underlying ImageField is blank, a ValueError would be
            # raised on `open`. When representing as base64, simply return an
            # empty base64 str rather than let the exception propagate unhandled
            # up into serializers.
            if not file:
                return ""

            try:
                with open(file.path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                raise IOError("Error encoding file")
        else:
            return super(Base64FieldMixin, self).to_representation(file)


class Base64FileField(Base64FieldMixin, FileField):
    """
    A django-rest-framework field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """

    @property
    def ALLOWED_TYPES(self):
        raise NotImplementedError("List allowed file extensions")

    INVALID_FILE_MESSAGE = "Please upload a valid file."
    INVALID_TYPE_MESSAGE = "The type of the file couldn't be determined."

    def get_file_extension(self, filename, decoded_file):
        raise NotImplementedError(
            "Implement file validation and return matching extension."
        )


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

    def to_internal_value(self, base64_data):
        FILE_MIME_TYPE = ""
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, str):
            # Strip base64 header, get mime_type from base64 header.
            if ";base64," in base64_data:
                header, base64_data = base64_data.split(";base64,")
                FILE_MIME_TYPE = header.replace("data:", "")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)

            # Generate file name:
            file_name = self.get_file_name(decoded_file)

            # Get the file name extension:
            file_extension = guess_extension(FILE_MIME_TYPE)[1:]

            if file_extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)

            complete_file_name = file_name + "." + file_extension
            data = SimpleUploadedFile(
                name=complete_file_name,
                content=decoded_file,
                content_type=FILE_MIME_TYPE,
            )
            return super(CustomBase64FileField, self).to_internal_value(data)
            
        raise ValidationError(_("Invalid type. This is not an base64 string: {}".format(type(base64_data))))