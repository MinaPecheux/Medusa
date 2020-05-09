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
from os import listdir, makedirs
from os.path import exists
from time import sleep

from .utils import ShellColors, ALPHABET, V_TABLES


def parse_args(args):
    parsed = dict(
        input=args.input,
        type=args.type,
        action=args.action,
        verbose=args.verbose
    )
    return parsed


class Medusa(object):

    def __init__(self, key, complement_key, verbose=False):
        self.key = key
        self.complement_key = complement_key
        self.verbose = verbose

    def encode(self, string):
        key_rank = 0                # counter that goes through the characters of the key
        complement_key_rank = 0     # counter that goes through the complement key
        word_encoded = ''           # result word
        # go through the characters of the word to code
        for c in string:
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

    def decode(self, string):
        key_rank = 0                # counter that goes through the characters of the key
        complement_key_rank = 0     # counter that goes through the complement key
        word_decoded = ''           # result word
        # go through the characters of the word to decode
        for c in string:
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
        if self.verbose: print ('')
        input_name = args['input']

        # if acting on FILE
        if args['type'] == 'file':
            # read file
            if self.verbose: print ('Reading file.')

            with open(input_name, mode='r') as FILE_READ:
                content = FILE_READ.read()

            tmp = input_name.split('.')
            # encryption
            if args['action'] == 'encode':
                # write encoded file
                if self.verbose: print ('Encrypting.')
                with open(tmp[0] + '_m.' + tmp[1], mode='w') as FILE_WRITE:
                    FILE_WRITE.write(self.encode(content))
            # decryption
            elif args['action'] == 'decode':
                # write decoded file
                if self.verbose: print ('Decrypting.')
                with open(tmp[0][:-2] + '.' + tmp[1], mode='w') as FILE_WRITE:
                    FILE_WRITE.write(self.decode(content))

        # else if acting on DIRECTORY
        elif args['type'] == 'dir' or args['type'] == 'dirzip':
            # get directory files
            if self.verbose: print ('Reading files from directory.')
            files = [f for f in listdir(input_name)]

            # encryption
            if args['action'] == 'encode':
                # add encoding marker
                if not exists(input_name + '_m'):
                    makedirs(input_name + '_m')

                if self.verbose: print ('')
                # go through files in directory
                for f in files:
                    if f.startswith('.'):
                        continue

                    sys.stdout.write('\rEncrypting... (%d/%d)' % (files.index(f) + 1, len(files)))
                    sys.stdout.flush()
                    # read decoded file
                    with open(input_name + '/' + f, mode='r') as FILE_READ:
                        content = FILE_READ.read()

                    # write encoded file
                    with open(input_name + '_m/' + f, mode='w') as FILE_WRITE:
                        FILE_WRITE.write(self.encode(content))

                    sleep(0.1)

                if self.verbose: print ('')
                # if asked, zip the resulting directory
                if args['type'] == 'dirzip':
                    if self.verbose: print ('Zipping encrypted directory.')
                    shutil.make_archive(input_name + '_m', 'zip', input_name + '_m')

            # decryption
            if args['action'] == 'decode':
                # remove encoding marker
                if not exists(input_name[:-2]):
                    makedirs(input_name[:-2])

                # go through files in directory
                for f in files:
                    if f.startswith('.'):
                        continue

                    sys.stdout.write('\rDecrypting... (%d/%d)' % (files.index(f) + 1, len(files)))
                    sys.stdout.flush()
                    # read encoded file
                    with open(input_name + '/' + f, mode='r') as FILE_READ:
                        content = FILE_READ.read()

                    # write decoded file
                    with open(input_name[:-2] + '/' + f, mode='w') as FILE_WRITE:
                        FILE_WRITE.write(self.decode(content))

                if self.verbose: print ('')
                # if asked, zip the resulting directory
                if args['type'] == 'dirzip':
                    if self.verbose: print ('Zipping decrypted directory.')
                    shutil.make_archive(input_name, 'zip', input_name)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-a', '--action', type=str)
    parser.add_argument('-t', '--type', type=str, default='file')
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
        tmp = args['input'].split('.')
        if exists(tmp[0][:-2] + '.' + tmp[1]):
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

