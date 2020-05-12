import os
import shutil
import getpass

from medusa import medusa

INPUT_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')


class MockedGetpass:
    def __init__(self, password):
        def noop(*args, **kwargs):
            return password

        self.oldpass = getpass.getpass
        self.newpass = noop

    def __enter__(self):
        getpass.getpass = self.newpass

    def __exit__(self, exc_type, exc_val, exc_tb):
        getpass.getpass = self.oldpass


def setup_module(module):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def teardown_module(module):
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)


class TestCLI():

    def test_cli_file(self):
        input_path = os.path.join(INPUT_DIR, 'input.txt')
        output_path = os.path.join(OUTPUT_DIR, 'output.txt')
        reencode_path = os.path.join(OUTPUT_DIR, 'new.txt')
        algo = 'caesar'

        with MockedGetpass('1'):
            medusa(algo=algo,
                   input=input_path,
                   output=output_path,
                   action='encode')
        with MockedGetpass('1'):
            medusa(algo=algo,
                   input=output_path,
                   output=reencode_path,
                   action='decode')

        with open(input_path, 'r') as FILE:
            text = FILE.read()
        with open(output_path, 'r') as FILE:
            encoded = FILE.read()
        with open(reencode_path, 'r') as FILE:
            decoded = FILE.read()

        assert decoded == text
        assert encoded != text

    def test_cli_dir(self):
        input_path = os.path.join(INPUT_DIR, 'input_dir')
        output_path = os.path.join(OUTPUT_DIR, 'output_dir')
        reencode_path = os.path.join(OUTPUT_DIR, 'new_dir')
        algo = 'caesar'

        with MockedGetpass('1'):
            medusa(algo=algo,
                   input=input_path,
                   output=output_path,
                   action='encode',
                   zip=True,
                   verbose=True)
        with MockedGetpass('1'):
            medusa(algo=algo,
                   input=output_path,
                   output=reencode_path,
                   action='decode')

        for f in os.listdir(input_path):
            with open(os.path.join(input_path, f), 'r') as FILE:
                text = FILE.read()
            with open(os.path.join(output_path, f), 'r') as FILE:
                encoded = FILE.read()
            with open(os.path.join(reencode_path, f), 'r') as FILE:
                decoded = FILE.read()

            assert decoded == text
            assert encoded != text

    def test_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '.medusa')

        with MockedGetpass('1'):
            args_encode = medusa(config=config_path, action='encode',
                                 return_args=True)
        with MockedGetpass('1'):
            args_decode = medusa(config=config_path, action='decode',
                                 return_args=True)

        input_path = os.path.join(
            os.path.dirname(__file__), args_encode['input'])
        output_path = os.path.join(
            os.path.dirname(__file__), args_encode['output'])
        reencode_path = os.path.join(
            os.path.dirname(__file__), args_decode['output'])
        with open(input_path, 'r') as FILE:
            text = FILE.read()
        with open(output_path, 'r') as FILE:
            encoded = FILE.read()
        with open(reencode_path, 'r') as FILE:
            decoded = FILE.read()

        assert decoded == text
        assert encoded != text
