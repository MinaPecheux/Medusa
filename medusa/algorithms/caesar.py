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


def required_params():
    '''List of params that are required for the Caesar process.

    Returns
    -------
    list(str)
        List of required parameters.
    '''
    return ['shift']


def check_secure(params):
    '''Checks if the params are secured enough for a Caesar process.

    Parameters
    ----------
    params : dict
        Params to use for processing.

    Returns
    -------
    (bool, str)
        Whether or not the params are valid and error message to warn the user.
    '''
    if params['shift'] == 0:
        return False, '"shift" cannot be zero'
    return True, None


def encode(content, params):
    '''Encodes a string using the Caesar technique.

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
    shift = params['shift']
    return ''.join([ALPHABET[(ALPHABET.index(c) + shift) % len(ALPHABET)]
                    for c in content])


def decode(content, params):
    '''Decodes a string using the Caesar technique.

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
    shift = params['shift']
    return ''.join([ALPHABET[(ALPHABET.index(c) - shift) % len(ALPHABET)]
                    for c in content])
