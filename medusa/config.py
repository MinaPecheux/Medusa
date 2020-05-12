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

import os
import re

BASE_CONFIG = {
    'exclude': [],
    'zip': False,
    'verbose': False
}

CONFIG_PARAMS = {
    'encode': ['input', 'output', 'algo', 'zip'],
    'decode': ['input', 'output', 'algo']
}


def apply_type_on_value(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    try:
        i = int(value)
        return i
    except:
        try:
            f = float(value)
            return f
        except:
            pass
    return value


def parse_config(lines, block):
    config = {}
    for line in lines.split('\n'):
        if len(line) == 0 or line == '[{}]'.format(block):
            continue
        k, v = line.split('=')
        k = k.strip()
        v = v.strip()

        if k in CONFIG_PARAMS[block]:
            config[k] = apply_type_on_value(v)
    return config


def load_config(config_file=None):
    if not os.path.abspath(config_file):
        config_file = os.path.join(os.getcwd(), config_file)

    # if no config file, abort
    if not os.path.exists(config_file):
        return {}

    # read custom project config file
    data = ''
    with open(config_file, 'r') as FILE:
        data = FILE.read()

    # parse config
    config = {'encode': BASE_CONFIG.copy(), 'decode': BASE_CONFIG.copy()}

    encode_lines = re.search(r'\[encode\]\n([^\[])*', data)
    if encode_lines:
        config['encode'].update(parse_config(encode_lines.group(0), 'encode'))

    decode_lines = re.search(r'\[decode\]\n([^\[])*', data)
    if decode_lines:
        config['decode'].update(parse_config(decode_lines.group(0), 'decode'))

    return config
