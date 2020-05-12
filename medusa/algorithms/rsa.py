# Copyright 2020 Mina Pêcheux (mina.pecheux@gmail.com)
# ---------------------------
# Distributed under the MIT License:
# ==================================
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================
# [Medusa] Mini Encoding/Decoding Utility with Simple Algorithms
# ------------------------------------------------------------------------------

__author__ = 'Mina Pêcheux'
__copyright__ = 'Copyright 2020, Mina Pêcheux'

import binascii
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from .common import Algorithm


class Rsa(Algorithm):

    _name = 'rsa'

    def __init__(self):
        super().__init__()

        # set context
        self.keys = RSA.generate(3072)
        pub_key = self.keys.publickey()
        self.ctx['n'] = hex(pub_key.n)
        self.ctx['e'] = hex(pub_key.e)
        self.ctx['d'] = hex(self.keys.d)

    @staticmethod
    def get_params():
        return {'decode': {'required': ['n', 'e', 'd']}}

    def transform_params(self, params):
        if 'n' in params:
            params['n'] = int(params['n'], 0)
        if 'e' in params:
            params['e'] = int(params['e'], 0)
        if 'd' in params:
            params['d'] = int(params['d'], 0)

    def check_secure(self, params, action=None):
        return True, None

    def encode(self, content, params):
        encryptor = PKCS1_OAEP.new(self.keys.publickey())
        if isinstance(content, str):
            content = content.encode()
        encoded = encryptor.encrypt(content)
        encoded = binascii.hexlify(encoded)
        return encoded

    def decode(self, content, params):
        n, e, d = params['n'], params['e'], params['d']
        keys = RSA.construct((n, e, d))
        decryptor = PKCS1_OAEP.new(keys)
        content = binascii.unhexlify(content)
        decoded = decryptor.decrypt(content)
        return decoded
