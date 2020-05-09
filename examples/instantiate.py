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
#          Example script: basic Medusa object instantiation.
# ------------------------------------------------------------------------------

from medusa import Medusa

if __name__ == '__main__':
    processor = Medusa('key', 'complement_key')

    # ENCODING
    # encode a string directly
    encoded = processor.encode('hello world')

    # encode some file
    processor.encode_file('data/input.txt', 'data/output.txt')

    # encode some directory
    processor.encode_dir('data/input_dir', 'data/output_dir')

    # DECODING
    # decode a string directly
    decoded = processor.decode('ÓÐ×ÑèÜèÝ×Ý')

    # decode some file
    processor.decode_file('data/output.txt', 'data/new.txt')

    # decode some directory
    processor.decode_dir('data/output_dir', 'data/new_dir')
