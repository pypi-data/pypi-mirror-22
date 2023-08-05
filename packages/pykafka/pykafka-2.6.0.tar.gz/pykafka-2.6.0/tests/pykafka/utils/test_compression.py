import platform
import pytest
import unittest2
from uuid import uuid4

from pykafka.utils import compression


class CompressionTests(unittest2.TestCase):
    """Keeping these simple by verifying what goes in is what comes out."""
    text = b"The man in black fled across the desert, and the gunslinger followed."

    def test_gzip(self):
        encoded = compression.encode_gzip(self.text)
        self.assertNotEqual(self.text, encoded)

        decoded = compression.decode_gzip(encoded)
        self.assertEqual(self.text, decoded)

    def test_snappy(self):
        encoded = compression.encode_snappy(self.text)
        self.assertNotEqual(self.text, encoded)

        decoded = compression.decode_snappy(encoded)
        self.assertEqual(self.text, decoded)

    def test_snappy_xerial(self):
        encoded = compression.encode_snappy(self.text, xerial_compatible=True)
        self.assertNotEqual(self.text, encoded)

        decoded = compression.decode_snappy(encoded)
        self.assertEqual(self.text, decoded)

    @pytest.mark.skipif(platform.python_implementation() == "PyPy",
                        reason="PyPy fails to compress large messages with Snappy")
    def test_snappy_large_payload(self):
        payload = b''.join([uuid4().bytes for i in range(10)])
        c = compression.encode_snappy(payload)
        self.assertEqual(compression.decode_snappy(c), payload)


if __name__ == '__main__':
    unittest2.main()
