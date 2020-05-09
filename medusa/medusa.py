# Copyright 2019 Mina Pêcheux (mina.pecheux@gmail.com)
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
# [Medusa] Mini Encoding/Decoding Util with Simple Algorithms
# ------------------------------------------------------------------------------

__author__ = 'Mina Pêcheux'
__copyright__ = 'Copyright 2020, Mina Pêcheux'

import argparse
import shutil
import getpass
import sys
import os
from time import sleep

from .utils import ShellColors, ALPHABET, V_TABLES


def parse_args(args):
    if args.decode:
        action = 'decode'
    elif args.encode:
        action = 'encode'
    parsed = dict(
        input=args.input,
        output=args.output,
        action=action,
        exclude=args.exclude,
        zip=args.zip,
        verbose=args.verbose
    )
    return parsed


class Medusa(object):

    def __init__(self, key, complement_key, exclude=[], verbose=False):
        '''Main Medusa object to encode/decode strings using the Vigenere technique.

        Parameters
        ----------
        key : str
            Main key to encode/decode content.
        complement_key : str
            Secondary key to encode/decode content.
        exclude : list(str), optional
            List of files to exclude from processing (empty list by default).
        verbose : bool, optional
            If true, the process with print logs during its execution (false by default).
        '''
        self.key = key
        self.complement_key = complement_key
        self.exclude = exclude
        self.verbose = verbose

    def encode(self, content):
        '''Encodes a string using the processor keys.

        Parameters
        ----------
        content : str
            Content to encode.

        Returns
        -------
        str
            Encoded content.
        '''
        key_rank = 0                # counter that goes through the characters of the key
        complement_key_rank = 0     # counter that goes through the complement key
        word_encoded = ''           # result word
        # go through the characters of the word to code
        for c in content:
            # apply Vigenere method
            for i in V_TABLES:
                if i[0] == self.key[key_rank]:
                    for j in i:
                        if i.index(j) == ALPHABET.index(c):
                            word_encoded += j

            # access new character of the key
            last_key_rank = key_rank
            key_rank = (key_rank + ord(self.complement_key[complement_key_rank])) % len(self.key)

            # if back to beginning of key
            if key_rank <= last_key_rank:
                # access next character of complement key
                complement_key_rank = (complement_key_rank + 1) % len(self.complement_key)

        return word_encoded

    def decode(self, content):
        '''Decodes a string using the processor keys.

        Parameters
        ----------
        content : str
            Content to decode.

        Returns
        -------
        str
            Decoded content.
        '''
        key_rank = 0                # counter that goes through the characters of the key
        complement_key_rank = 0     # counter that goes through the complement key
        word_decoded = ''           # result word
        # go through the characters of the word to decode
        for c in content:
            for i in V_TABLES:
                if i[0] == self.key[key_rank]:
                    for j in i:
                        if j == c:
                            word_decoded += ALPHABET[i.index(j)]

            # access new character of the key
            last_key_rank = key_rank
            key_rank = (key_rank + ord(self.complement_key[complement_key_rank])) % len(self.key)

            # if back to beginning of key
            if key_rank <= last_key_rank:
                # access next character of complement key
                complement_key_rank = (complement_key_rank + 1) % len(self.complement_key)

        return word_decoded

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

        # read file
        if self.verbose:
            print ('\n{}> {}'.format(ind, os.path.basename(input_path)))

        with open(input_path, 'r') as FILE_READ:
            content = FILE_READ.read()

        # encryption
        if action == 'encode':
            # write encoded file
            with open(output_path, 'w') as FILE_WRITE:
                FILE_WRITE.write(self.encode(content))
        # decryption
        elif action == 'decode':
            # write decoded file
            with open(output_path, 'w') as FILE_WRITE:
                FILE_WRITE.write(self.decode(content))

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

        # prepare output dir if need be
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        dir_name = os.path.basename(input_path)
        print ('')

        # get directory files
        if self.verbose:
            log = 'Reading files from directory: "{}"'.format(dir_name)
            print (ind + log)
            print (ind + '-' * len(log))
        files = [ f for f in os.listdir(input_path) ]

        # go through files in directory
        for f in files:
            if f.startswith('.') or f in self.exclude:
                if self.verbose:
                    print(ind + 'Ignoring:', f)
                continue

            if action == 'encode':
                sys.stdout.write('\r{}Encrypting "{}" ({}/{})'.format(ind, dir_name,
                                                                      files.index(f) + 1,
                                                                      len(files)))
            else:
                sys.stdout.write('\r{}Decrypting "{}" ({}/{})'.format(ind, dir_name,
                                                                      files.index(f) + 1,
                                                                      len(files)))
            sys.stdout.flush()

            # read input file
            ipath = os.path.abspath(os.path.join(input_path, f))
            opath = os.path.abspath(os.path.join(output_path, f))
            if os.path.isdir(ipath):
                self.process_dir(ipath, opath, action, indent=indent + 1)
            else:
                self.process_file(ipath, opath, action, indent=indent)

            sleep(0.1)

        if self.verbose: print ('')

    def process(self, args):
        '''Processes the inputs (using the args context).

        Parameters
        ----------
        args : dict
            Execution context.
        '''
        if self.verbose: print ('')
        input_path = os.path.abspath(args['input'])
        output_path = os.path.abspath(args['output'])
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
                    print ('\nZipping encrypted directory.')
                shutil.make_archive(output_path, 'zip', output_path)


def main():
    parser = argparse.ArgumentParser()
    actions_parser = parser.add_mutually_exclusive_group(required=True)
    actions_parser.add_argument('-e', '--encode', action='store_true')
    actions_parser.add_argument('-d', '--decode', action='store_true')

    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('--exclude', type=str, default=[], nargs='+')
    parser.add_argument('-z', '--zip', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parse_args(parser.parse_args())

    # display info
    if args['verbose']:
        log = ShellColors.BLUE + '-------------------------------------\n'
        log += 'MEDUSA {}\n'.format('Encryption' if args['action'] == 'encode' else 'Decryption')
        log += '-------------------------------------\n'
        log += ShellColors.ENDC
        log += 'Working on: {}\n'.format(args['input'])
        print (log)

    # check for overwrite problems: if decoding, ask to overwrite already existing file
    if args['action'] == 'decode':
        # if there is already a file with the decoded name
        if os.path.exists(args['output']):
            q = input(ShellColors.YELLOW + 'Overwrite existing data? (y/n) ' + ShellColors.ENDC)
            # if overwriting allowed
            if q == 'y':
                # get keys
                key = getpass.getpass(prompt='Encoding key: ')
                complement_key = getpass.getpass(prompt='Complement key: ')
                # decode
                processor = Medusa(key, complement_key, exclude=args['exclude'], verbose=args['verbose'])
                processor.process(args)
            # else do nothing
            else:
                print (ShellColors.RED + 'No data overwriting. Process aborted.' + ShellColors.ENDC)
        else:
            # get keys
            key = getpass.getpass(prompt='Encoding key: ')
            complement_key = getpass.getpass(prompt='Complement key: ')
            # decode
            processor = Medusa(key, complement_key, exclude=args['exclude'], verbose=args['verbose'])
            processor.process(args)

    else:
        # get keys
        key = getpass.getpass(prompt='Encoding key: ')
        complement_key = getpass.getpass(prompt='Complement key: ')
        # if encoding, check for secure password
        if (len(key) == 0 or len(complement_key) == 0) and args['verbose']:
            print (ShellColors.RED + 'Password not secure. Process aborted.' + ShellColors.ENDC)
        else:
            # encode
            processor = Medusa(key, complement_key, exclude=args['exclude'], verbose=args['verbose'])
            processor.process(args)

    if args['verbose']:
        print ('-------------------------------------\n' + ShellColors.ENDC)

