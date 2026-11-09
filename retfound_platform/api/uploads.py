"""Bounded in-memory image upload parsing. No filenames become filesystem paths."""
from python_multipart import MultipartParser
from python_multipart.multipart import parse_options_header

MAX_UPLOAD_BYTES = 20 * 1024 * 1024
MAX_REQUEST_BYTES = MAX_UPLOAD_BYTES + 64 * 1024
MEDIA_TYPES = {'image/jpeg', 'image/png', 'image/tiff', 'image/bmp', 'image/webp', 'application/octet-stream'}


class UploadError(ValueError):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code = status, code
        super().__init__(message)


def extract_image(body: bytes, content_type: str) -> bytes:
    media, options = parse_options_header(content_type)
    if media.decode('ascii', errors='replace').lower() in MEDIA_TYPES:
        if not body:
            raise UploadError(422, 'empty_image', 'Choose an image to analyze.')
        if len(body) > MAX_UPLOAD_BYTES:
            raise UploadError(413, 'image_too_large', 'The image must be 20 MB or smaller.')
        return body
    if media != b'multipart/form-data':
        raise UploadError(415, 'unsupported_media_type', 'Send image bytes or multipart/form-data with one image field.')
    boundary = options.get(b'boundary', b'')
    if not boundary or len(boundary) > 200:
        raise UploadError(400, 'invalid_multipart', 'The multipart boundary is missing or invalid.')
    image = bytearray()
    field = bytearray()
    value = bytearray()
    headers = {}
    parts = 0
    ended = False

    def part_begin():
        nonlocal parts
        parts += 1
        if parts > 1:
            raise UploadError(422, 'one_image_required', 'Send exactly one file in the image field.')

    def header_field(data, start, end):
        field.extend(data[start:end])

    def header_value(data, start, end):
        value.extend(data[start:end])

    def header_end():
        headers[bytes(field).lower()] = bytes(value)
        field.clear()
        value.clear()

    def headers_finished():
        disposition, params = parse_options_header(headers.get(b'content-disposition', b''))
        if disposition != b'form-data' or params.get(b'name') != b'image' or not params.get(b'filename'):
            raise UploadError(422, 'image_field_required', 'Send a file in the image field.')

    def part_data(data, start, end):
        if len(image) + end - start > MAX_UPLOAD_BYTES:
            raise UploadError(413, 'image_too_large', 'The image must be 20 MB or smaller.')
        image.extend(data[start:end])

    def end():
        nonlocal ended
        ended = True

    parser = MultipartParser(boundary, {
        'on_part_begin': part_begin, 'on_header_field': header_field,
        'on_header_value': header_value, 'on_header_end': header_end,
        'on_headers_finished': headers_finished, 'on_part_data': part_data, 'on_end': end,
    })
    try:
        parser.write(body)
        parser.finalize()
    except UploadError:
        raise
    except Exception as exc:
        raise UploadError(400, 'invalid_multipart', 'The multipart upload is malformed.') from exc
    if not ended or parts != 1 or not image:
        raise UploadError(422, 'empty_image', 'The upload is incomplete or contains no image.')
    return bytes(image)
