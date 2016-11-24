"""
Includes classes for various encoding methods for images.
All all new encodings as classes here.

Note:
Try keep the `encode` and `decode` method signatures same,
so that switching across multiple encodings is easy.

For any configuration parameters dependent on the encoding,
use extra parameters in the constructor.
"""

import cv2


class JpegEncoding:
    "Converts images from and to JPEG"

    def __init__(self, _quality=70):
        self.quality = _quality

    def encode(self, frame):
        return cv2.imencode('.jpg',
                            frame,
                            [cv2.IMWRITE_JPEG_QUALITY, self.quality])[1]

    def decode(self, byte_list):
        return cv2.imdecode(byte_list, cv2.IMREAD_COLOR)

    def set_quality(self, quality):
        self.quality = quality
