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

from .common import ALPHABET

ENCODE_TABLE = {
    c: {c2: ALPHABET[(j + i) % len(ALPHABET)]
        for j, c2 in enumerate(ALPHABET)}
    for i, c in enumerate(ALPHABET)
}
DECODE_TABLE = {
    c: {ALPHABET[(j + i) % len(ALPHABET)]: c2
        for j, c2 in enumerate(ALPHABET)}
    for i, c in enumerate(ALPHABET)
}


def required_params():
    '''List of params that are required for the Vigenere process.

    Returns
    -------
    list(str)
        List of required parameters.
    '''
    return ['key', 'complement_key']


def check_secure(params):
    '''Checks if the params are secured enough for a Vigenere process.

    Parameters
    ----------
    params : dict
        Params to use for processing.

    Returns
    -------
    (bool, str)
        Whether or not the params are valid and error message to warn the user.
    '''
    if len(params['key']) == 0:
        return False, '"key" cannot be empty'
    if len(params['complement_key']) == 0:
        return False, '"complement_key" cannot be empty'
    return True, None


def encode(content, params):
    '''Encodes a string using the Vigenere technique.

    Parameters
    ----------
    content : str
        Content to encode.
    params : dict
        Params to use for processing.

    Returns
    -------
    str
        Encoded content.
    '''
    key = params['key']
    complement_key = params['complement_key']

    key_rank = 0                # counter that goes through the characters of the key
    complement_key_rank = 0     # counter that goes through the complement key
    encoded = ''                # result content
    # go through the characters of the content to code
    for c in content:
        # apply Vigenere method
        row = ENCODE_TABLE[key[key_rank]]
        encoded += row[c]

        # access new character of the key
        last_key_rank = key_rank
        k = complement_key[complement_key_rank]
        key_rank = (key_rank + ord(k)) % len(key)

        # if back to beginning of key
        if key_rank <= last_key_rank:
            # access next character of complement key
            complement_key_rank = (complement_key_rank + 1) \
                % len(complement_key)

    return encoded


def decode(content, params):
    '''Decodes a string using the Vigenere technique.

    Parameters
    ----------
    content : str
        Content to decode.
    params : dict
        Params to use for processing.

    Returns
    -------
    str
        Decoded content.
    '''
    key = params['key']
    complement_key = params['complement_key']

    key_rank = 0                # counter that goes through the characters of the key
    complement_key_rank = 0     # counter that goes through the complement key
    decoded = ''                # result content
    # go through the characters of the content to decode
    for c in content:
        row = DECODE_TABLE[key[key_rank]]
        decoded += row[c]

        # access new character of the key
        last_key_rank = key_rank
        k = complement_key[complement_key_rank]
        key_rank = (key_rank + ord(k)) % len(key)

        # if back to beginning of key
        if key_rank <= last_key_rank:
            # access next character of complement key
            complement_key_rank = (complement_key_rank + 1) \
                % len(complement_key)

    return decoded
