import os
import pytest
import subprocess
import shutil

from medusa import Medusa

INPUT_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

tests = [
    {'input': 'input.txt', 'output': 'output.txt', 'reencode': 'new.txt'},
]
test_ids = [
    '{}_to_{}'.format(d['input'], d['output']) for d in tests
]


def setup_module(module):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def teardown_module(module):
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)


class TestFile():

    @pytest.mark.parametrize('params', tests, ids=test_ids)
    def test_basic(self, params):
        processor = Medusa(algo='vigenere',
                           params=dict(key='key',
                                       complement_key='complement_key'))
        input_path = os.path.join(INPUT_DIR, params['input'])
        output_path = os.path.join(OUTPUT_DIR, params['output'])
        reencode_path = os.path.join(OUTPUT_DIR, params['reencode'])

        processor.encode_file(input_path, output_path)
        assert os.path.exists(output_path)

        processor.decode_file(output_path, reencode_path)
        assert os.path.exists(reencode_path)

        with open(input_path, 'r') as FILE:
            input_content = FILE.read()

        with open(output_path, 'r') as FILE:
            output_content = FILE.read()

        with open(reencode_path, 'r') as FILE:
            reencode_content = FILE.read()

        assert input_content == reencode_content
        assert input_content != output_content
