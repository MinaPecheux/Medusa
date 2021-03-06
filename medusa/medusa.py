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

import argparse
import inspect
import getpass
import os
import shutil
import sys
from time import sleep
from tqdm import tqdm

from .config import load_config
from .algorithms import ALGORITHMS


class ShellColors(object):
    YELLOW = '\033[93m'
    BLUE = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MedusaError(Exception):
    pass


class Medusa(object):

    def __init__(self, algo, params, exclude=[], verbose=False, base_path=None,
                 exit_on_error=True):
        '''Main Medusa object to encode/decode strings using basic cryptography techniques.

        Parameters
        ----------
        algo : str
            Reference of the algorithm to use for encoding/decoding.
        params : dict
            Parameters to use in the algorithm (e.g. the specific keys to use).
        exclude : list(str), optional
            List of files to exclude from processing (empty list by default).
        verbose : bool, optional
            If true, the process with print logs during its execution (false by default).
        base_path : str, optional
            Root path to prepend all input/output paths with if they are not absolute.
        exit_on_error : bool, optional
            Whether or not to sys exit if object could not be instantiated (true by default).
        '''
        if algo not in ALGORITHMS:
            print('Unknown algorithm: "{}"'.format(algo))
            print('Available ciphers:')
            for a in ALGORITHMS:
                print('- {}'.format(a))
            if exit_on_error:
                sys.exit(1)
            else:
                raise MedusaError()

        self.algo = ALGORITHMS[algo]()
        self.algo_params = ALGORITHMS[algo].get_params()
        self.params = params
        self.exclude = exclude
        self.verbose = verbose
        self.exit_on_error = exit_on_error

        if not self._check_missing_params(self.params):
            raise MedusaError()
        if not self._check_secure_params(self.params):
            raise MedusaError()

        self.encode = self._wrap_processor(self.algo.encode, 'encode')
        self.decode = self._wrap_processor(self.algo.decode, 'decode')

        if base_path is None:
            self.base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        else:
            self.base_path = base_path

    def _check_missing_params(self, params, action=None):
        '''Checks if the object has all necessary args for required action.'''
        req_params = self.algo_params.get('common', {}).get('required', [])
        if action is not None:
            req_params += self.algo_params.get(action, {}).get('required', [])
        missing_params = [p for p in req_params if p not in params]
        if len(missing_params) > 0:
            msg = 'Invalid parameters: algorithm "{}" requires:'.format(
                self.algo._name)
            print('[Medusa - Error] {}'.format(msg))
            for param in missing_params:
                print('-', param)
            if self.exit_on_error:
                sys.exit(1)
            else:
                return False
        return True

    def _check_secure_params(self, params, action=None):
        '''Checks if the object has secure params for required action.'''
        check, error = self.algo.check_secure(params, action=action)
        if not check:
            print('[Medusa - Error] {}'.format(error))
            if self.exit_on_error:
                sys.exit(1)
            else:
                return False
        return True

    def _print_context(self):
        '''Prints the current context of the used algorithm (auto-generated keys, offsets...).'''
        for k, v in self.algo.ctx.items():
            print('[{:>6}] {}'.format(k.title().replace('_', ' '), v))

    def _wrap_processor(self, func, action):
        '''Wraps a processing function with auto check of params, auto update of
        params with object-specific values...'''
        def _wrapped(content, **kwargs):
            __is_direct = kwargs.pop('__is_direct', True)
            params = self.params.copy()
            params.update(kwargs)
            if not self._check_missing_params(params, action=action):
                raise MedusaError()
            if not self._check_secure_params(params, action=action):
                raise MedusaError()
            self.algo.transform_params(params)
            res = func(content, params)
            if action == 'decode' and not isinstance(res, str):
                res = res.decode()

            if __is_direct and action == 'encode':
                self._print_context()
            return res
        return _wrapped

    def get_context(self):
        '''Returns the current context of this object's algorithm.

        Returns
        -------
        dict
            Current algorithm context.
        '''
        return self.algo.ctx

    def process_file(self, input_path, output_path, action, indent=0):
        '''Processes one file (either for encoding or decoding).

        Parameters
        ----------
        input_path : str
            Absolute path to the original file.
        output_path : str
            Absolute path to the new processed file.
        action : str
            Action to perform, can be: "encode" or "decode".
        indent : int, optional
            Indent size for log verbose output (0 by default).
        '''
        ind = ' ' * 4 * indent

        if not os.path.isabs(input_path):
            input_path = os.path.join(self.base_path, input_path)
        if not os.path.isabs(output_path):
            output_path = os.path.join(self.base_path, output_path)

        # read file
        if self.verbose:
            print('\n{}> {}'.format(ind, os.path.basename(input_path)))

        try:
            with open(input_path, 'r') as FILE_READ:
                content = FILE_READ.read()
        except UnicodeDecodeError:
            with open(input_path, 'rb') as FILE_READ:
                content = FILE_READ.read()

        # process
        if action == 'encode':
            res = self.encode(content, __is_direct=False)
        elif action == 'decode':
            res = self.decode(content, __is_direct=False)

        # write encoded file
        if isinstance(res, str):
            with open(output_path, 'w') as FILE_WRITE:
                FILE_WRITE.write(res)
        elif isinstance(res, bytes):
            with open(output_path, 'wb') as FILE_WRITE:
                FILE_WRITE.write(res)
        else:
            i = os.path.basename(input_path)
            print(
                '[Medusa - Error] Invalid processing: could not write output for "{}".'.format(i))
            if self.exit_on_error:
                sys.exit(1)

    def encode_file(self, input_path, output_path):
        '''Encodes one file.

        Parameters
        ----------
        input_path : str
            Absolute path to the original file.
        output_path : str
            Absolute path to the new processed file.
        '''
        self.process_file(input_path, output_path, 'encode')

    def decode_file(self, input_path, output_path):
        '''Decodes one file.

        Parameters
        ----------
        input_path : str
            Absolute path to the original file.
        output_path : str
            Absolute path to the new processed file.
        '''
        self.process_file(input_path, output_path, 'decode')

    def process_dir(self, input_path, output_path, action, indent=0):
        '''Processes one directory recursively (either for encoding or decoding).

        Parameters
        ----------
        input_path : str
            Absolute path to the original directory.
        output_path : str
            Absolute path to the new processed directory.
        action : str
            Action to perform, can be: "encode" or "decode".
        indent : int, optional
            Indent size for log verbose output (0 by default).
        '''
        ind = ' ' * 4 * indent

        if not os.path.isabs(input_path):
            input_path = os.path.join(self.base_path, input_path)
        if not os.path.isabs(output_path):
            output_path = os.path.join(self.base_path, output_path)

        # prepare output dir if need be
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        dir_name = os.path.basename(input_path)
        print('')

        # get directory files
        if self.verbose:
            log = 'Reading files from directory: "{}"'.format(dir_name)
            print(ind + log)
            print(ind + '-' * len(log))
        files = [f for f in os.listdir(input_path)]

        # go through files in directory
        it = tqdm(files) if indent == 0 else files
        print('{}{} "{}"'.format(ind, 'Encrypting' if action == 'encode' else 'Decrypting',
                                 dir_name))
        for f in it:
            if f.startswith('.') or f in self.exclude:
                if self.verbose:
                    print(ind + 'Ignoring:', f)
                continue

            # read input file
            ipath = os.path.abspath(os.path.join(input_path, f))
            opath = os.path.abspath(os.path.join(output_path, f))
            if os.path.isdir(ipath):
                self.process_dir(ipath, opath, action, indent=indent + 1)
            else:
                self.process_file(ipath, opath, action, indent=indent)

            sleep(0.1)

        if self.verbose:
            print('')

    def encode_dir(self, input_path, output_path):
        '''Encodes one directory.

        Parameters
        ----------
        input_path : str
            Absolute path to the original directory.
        output_path : str
            Absolute path to the new processed directory.
        '''
        self.process_dir(input_path, output_path, 'encode')

    def decode_dir(self, input_path, output_path):
        '''Decodes one directory.

        Parameters
        ----------
        input_path : str
            Absolute path to the original directory.
        output_path : str
            Absolute path to the new processed directory.
        '''
        self.process_dir(input_path, output_path, 'decode')

    def process(self, args):
        '''Processes the inputs (using the args context).

        Parameters
        ----------
        args : dict
            Execution context.
        '''
        if self.verbose:
            print('')

        if not os.path.isabs(args['input']):
            input_path = os.path.join(self.base_path, args['input'])
        else:
            input_path = args['input']
        if not os.path.isabs(args['output']):
            output_path = os.path.join(self.base_path, args['output'])
        else:
            output_path = args['output']

        input_type = 'dir' if os.path.isdir(input_path) else 'file'

        # if acting on FILE
        if input_type == 'file':
            self.process_file(input_path=input_path,
                              output_path=output_path,
                              action=args['action'])
        # else if acting on DIRECTORY
        elif input_type == 'dir':
            self.process_dir(input_path=input_path,
                             output_path=output_path,
                             action=args['action'])

            # if asked, zip the resulting directory
            if args['zip']:
                if self.verbose:
                    print('\nZipping encrypted directory.')
                shutil.make_archive(output_path, 'zip', output_path)

        if args['action'] == 'encode':
            print('')
            self._print_context()


def parse_args(args):
    if args.decode:
        action = 'decode'
    elif args.encode:
        action = 'encode'

    if 'config_file' in args:
        config = load_config(args.config_file)[action]
        config['action'] = action
    else:
        config = dict(
            algo=args.algo,
            input=args.input,
            output=args.output,
            action=action,
            exclude=args.exclude,
            zip=args.zip,
            verbose=args.verbose
        )
    return config


def input_params(algo, action):
    params = dict()
    ref_params = ALGORITHMS[algo].get_params()
    req_params = ref_params.get('common', {}).get('required', []) + \
        ref_params.get(action, {}).get('required', [])

    if len(req_params) > 0:
        print(ShellColors.BLUE + '[Medusa] Set params:')
        for param in req_params:
            prompt = '>> {}: '.format(param.title().replace('_', ' '))
            tmp = getpass.getpass(prompt=prompt)
            params[param] = tmp
        print(ShellColors.ENDC)
    return params


def main(return_args=False, **args):
    if len(args) == 0:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        actions_parser = parser.add_mutually_exclusive_group(required=True)
        actions_parser.add_argument('-e', '--encode', action='store_true')
        actions_parser.add_argument('-d', '--decode', action='store_true')

        # config file-base parser
        config_parser = subparsers.add_parser('config')
        config_parser.add_argument('config_file', type=str)

        # full cli parser
        cli_parser = subparsers.add_parser('cli')
        cli_parser.add_argument('-a', '--algo', type=str, required=True,
                                help='Algorithm to use for the encode/decode process.')
        cli_parser.add_argument('-i', '--input', type=str, required=True,
                                help='Path to the input file or dir to process.')
        cli_parser.add_argument('-o', '--output', type=str, required=True,
                                help='Path to the output file or dir (where to write the processed data).')

        cli_parser.add_argument('--exclude', type=str, default=[], nargs='+',
                                help='List of files or folders to ignore during processing.')
        cli_parser.add_argument('-z', '--zip', action='store_true',
                                help='If true, create a zip with the processed data (only for dir processing).')
        cli_parser.add_argument('-v', '--verbose', action='store_true',
                                help='If true, print additional logs during process.')

        args = parse_args(parser.parse_args())
    else:
        if 'config' in args:
            action = args['action']
            args = load_config(args['config'])[action]
            args['action'] = action

        if 'algo' not in args:
            print('[Medusa - Error] Missing argument: algo.')
            return
        if 'input' not in args:
            print('[Medusa - Error] Missing argument: input.')
            return
        if 'output' not in args:
            print('[Medusa - Error] Missing argument: output.')
            return
        if 'action' not in args:
            print('[Medusa - Error] Missing argument: action.')
            return
        if args['action'] not in ['encode', 'decode']:
            print(
                '[Medusa - Error] Invalid argument: action should be "encode" or "decode".')
            return

        if 'exclude' not in args:
            args['exclude'] = []
        if 'zip' not in args:
            args['zip'] = False
        if 'verbose' not in args:
            args['verbose'] = False

    st = inspect.stack()
    if len(st) == 2:
        base_path = os.path.abspath(os.path.dirname(
            os.path.dirname(inspect.stack()[0].filename)))
    else:
        base_path = os.path.abspath(os.path.dirname(
            inspect.stack()[1].filename))

    # display info
    if args['verbose']:
        log = ShellColors.BLUE + '-------------------------------------\n'
        log += 'MEDUSA {}\n'.format(
            'Encryption' if args['action'] == 'encode' else 'Decryption')
        log += '-------------------------------------\n'
        log += ShellColors.ENDC
        log += 'Working on: {}\n'.format(args['input'])
        log += 'Algorithm: {}\n'.format(args['algo'])
        print(log)

    # check for overwrite problems: if decoding, ask to overwrite already existing file
    if args['action'] == 'decode':
        # if there is already a file with the decoded name
        if os.path.exists(args['output']):
            q = input(ShellColors.YELLOW +
                      'Overwrite existing data? (y/n) ' + ShellColors.ENDC)
            # if overwriting allowed
            if q != 'y':
                print(ShellColors.RED +
                      'No data overwriting. Process aborted.' + ShellColors.ENDC)
                return

    # get params
    params = input_params(args['algo'], args['action'])
    # encode
    processor = Medusa(algo=args['algo'],
                       params=params,
                       exclude=args['exclude'],
                       verbose=args['verbose'],
                       base_path=base_path)
    processor.process(args)

    if args['verbose']:
        print('-------------------------------------\n' + ShellColors.ENDC)

    if return_args:
        return args
