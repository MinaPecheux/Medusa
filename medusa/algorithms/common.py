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

ALPHABET = [chr(x) for x in range(256)]


class Algorithm(object):

    _name = ''

    def __init__(self):
        '''Creates a new instance of this algorithm.'''
        self.ctx = {}

    @staticmethod
    def get_params():
        '''List of params that are required for the algorithm.

        Returns
        -------
        dict
            Dict of parameters: required, for encoding, for decoding...
        '''
        return {}

    def transform_params(self, params):
        '''Specific params transformer to prepare context args for processing.
        (Modifies the params dict in-place)

        Parameters
        ----------
        params : dict
            Processing context.
        '''
        pass

    def check_secure(self, params, action=None):
        '''Checks if the params are secured enough for processing.

        Parameters
        ----------
        params : dict
            Processing context.

        Returns
        -------
        (bool, str)
            Whether or not the params are valid and error message to warn the user.
        '''
        return True, None

    def get_ctx(self):
        '''Returns the algorithm context (may contain additional information after
        processing).

        Returns
        -------
        dict
            Context dict.
        '''
        return self.ctx

    def encode(self, content, params):
        '''Encodes a string using this algorithm.

        Parameters
        ----------
        content : str
            Content to encode.
        params : dict
            Processing context.

        Returns
        -------
        str
            Encoded content.
        '''
        raise NotImplementedError('Must provide a specific encoding function.')

    def decode(self, content, params):
        '''Decodes a string using this algorithm.

        Parameters
        ----------
        content : str
            Content to decode.
        params : dict
            Processing context.

        Returns
        -------
        str
            Decoded content.
        '''
        raise NotImplementedError('Must provide a specific decoding function.')
