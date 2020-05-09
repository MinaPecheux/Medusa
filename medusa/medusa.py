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
    parsed = dict(
        input=args.input,
        output=args.output,
        action=args.action,
        zip=args.zip,
        verbose=args.verbose
    )
    return parsed


class Medusa(object):

    def __init__(self, key, complement_key, verbose=False):
        '''Main Medusa object to encode/decode strings using the Vigenere technique.

        Parameters
        ----------
        key : string
            Main key to encode/decode content.
        complement_key : string
            Secondary key to encode/decode content.
        verbose : bool, optional
            If true, the process with print logs during its execution.
        '''
        self.key = key
        self.complement_key = complement_key
        self.verbose = verbose

    def encode(self, content):
        '''Encodes a string using the processor keys.

        Parameters
        ----------
        content : string
            Content to encode.

        Returns
        -------
        string
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
        content : string
            Content to decode.

        Returns
        -------
        string
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

    def process(self, args):
        '''Processes the inputs (using the args context).

        Parameters
        ----------
        args : dict
            Execution context.
        '''
        if self.verbose: print ('')
        input_name = args['input']
        input_type = 'dir' if os.path.isdir(input_name) else 'file'

        # if acting on FILE
        if input_type == 'file':
            # read file
            if self.verbose: print ('Reading file.')

            with open(input_name, mode='r') as FILE_READ:
                content = FILE_READ.read()

            # encryption
            if args['action'] == 'encode':
                # write encoded file
                if self.verbose: print ('Encrypting.')
                with open(args['output'], mode='w') as FILE_WRITE:
                    FILE_WRITE.write(self.encode(content))
            # decryption
            elif args['action'] == 'decode':
                # write decoded file
                if self.verbose: print ('Decrypting.')
                with open(args['output'], mode='w') as FILE_WRITE:
                    FILE_WRITE.write(self.decode(content))

        # else if acting on DIRECTORY
        elif input_type == 'dir':
            # prepare output dir if need be
            if not os.path.exists(args['output']):
                os.makedirs(args['output'])

            if self.verbose: print ('')

            # get directory files
            if self.verbose: print ('Reading files from directory.')
            files = [ f for f in os.listdir(input_name) ]

            # go through files in directory
            for f in files:
                if f.startswith('.'):
                    continue

                if args['action'] == 'encode':
                    sys.stdout.write('\rEncrypting... (%d/%d)' % (files.index(f) + 1, len(files)))
                else:
                    sys.stdout.write('\rDecrypting... (%d/%d)' % (files.index(f) + 1, len(files)))
                sys.stdout.flush()

                # read input file
                with open(os.path.join(input_name, f), mode='r') as FILE_READ:
                    content = FILE_READ.read()

                # write output file
                with open(os.path.join(args['output'], f), mode='w') as FILE_WRITE:
                    if args['action'] == 'encode':
                        FILE_WRITE.write(self.encode(content))
                    else:
                        FILE_WRITE.write(self.decode(content))

                sleep(0.1)

            if self.verbose: print ('')

            # if asked, zip the resulting directory
            if args['zip']:
                if self.verbose: print ('Zipping encrypted directory.')
                shutil.make_archive(args['output'], 'zip', args['output'])


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-a', '--action', type=str, required=True)
    parser.add_argument('-z', '--zip', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parse_args(parser.parse_args())

    # display info
    if args['verbose']:
        log = ShellColors.BLUE + '-------------------------------------\n'
        log += 'MEDUSA {}\n'.format('Encryption' if args['action'] == 'encode' else 'Decryption')
        log += '-------------------------------------\n'
        log += ShellColors.ENDC
        if args['type'] == 'file':
            log += 'Working on file: %s\n' % args['input']
        elif args['type'] == 'dir' or args['type'] == 'dirzip':
            log += 'Working on directory: %s\n' % args['input']

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
                processor = Medusa(key, complement_key, verbose=args['verbose'])
                processor.process(args)
            # else do nothing
            else:
                print (ShellColors.RED + 'No data overwriting. Process aborted.' + ShellColors.ENDC)
        else:
            # get keys
            key = getpass.getpass(prompt='Encoding key: ')
            complement_key = getpass.getpass(prompt='Complement key: ')
            # decode
            processor = Medusa(key, complement_key, verbose=args['verbose'])
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
            processor = Medusa(key, complement_key, verbose=args['verbose'])
            processor.process(args)

    if args['verbose']:
        print ('-------------------------------------\n' + ShellColors.ENDC)

