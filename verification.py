import base64
import hashlib
import hmac

import os


def verify_signature(request):
    """Verify the signature on a request to the message receive handler"""

    actual = base64.b16encode(hmac.new(os.environ['API_KEY'], request.get_data(), hashlib.sha1).digest())
    expected = request.headers.get('X-Kik-Signature')

    return actual == expected
