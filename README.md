# Medusa

The Mini Encoding/Decoding Utility with Simple Algorithms (Medusa) is a small Python lib to easily cypher and decypher files or directories using basic cryptography algorithms.

<div style="text-align: center;">
<img src="imgs/logo.png" alt="logo.png" width="150" height="150" />
</div>

For now, Medusa offers 4 encoding/decoding algorithms:
- the basic [Caesar (or shift) cipher](https://en.wikipedia.org/wiki/Caesar_cipher): a symmetric cryptography
  method that simply shifts letters by a given offset to get a ciphertext alphabet
- the [Vigenere cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher): a symmetric polyalphabetic cryptography
  method that uses a key and a complement key
- the [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard): a symmetric
  cypher (here, it uses a key that is derived into an initial integer value)
- the [Rivest-Shamir-Adleman (RSA)](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) algorithm: an asymmetric
  cypher with a public and a private key

_Note: to make it harder to decypher, Medusa uses a wide range of characters including Unicode characters... so it requires Python 3 to work._

## Install

To install Medusa, use `pip` from the online Github repository:

```
pip install git+https://github.com/MinaPecheux/Medusa.git#egg=medusa
```

This will install the Python lib and also a command-line `medusa` to run it directly in a shell.

## TL;DR

To encrypt a file or a folder, use the Medusa CLI with the `-e` or `--encrypt` argument:

```
medusa -e cli --algo vigenere -i <input_path> -o <output_path>
```

To decrypt a file or a folder, use the Medusa CLI with the `-d` or `--decrypt` argument:

```
medusa -d cli --algo vigenere -i <input_path> -o <output_path>
```

_Note: be careful that the Medusa CLI uses a subcommand `cli` for direct arguments passing. This is because the CLI
also allows for a config file-based set up (see below for more details)._

The module will automatically detect whether the input path is a file or a folder; if it is a folder, the directory will be processed recursively.

## Advanced CLI usage

### Autozip output

If you want process a folder and you want the processed output to be zipped automatically, simply add the `-z` or `--zip` argument!

```
medusa -e cli -a vigenere -i <input_path> -o <output_path> --zip
```

### Exclude specific files or folders

You can also ignore specific files or folders by passing a list of names in the `--exclude` argument:

```
medusa -e cli -a vigenere -i <input_path> -o <output_path> --exclude __pycache__ .DS_Store
```

### Verbose mode

To get more details on the process, enable the verbose logging mode with the `-v` or `--verbose` argument:

```
medusa -e cli -a vigenere -i <input_path> -o <output_path> -v
```

## Configuration file

It is often easier to write all of your settings in a config file and to then simply load this file upon CLI execution.
Medusa allows you to run the CLI with the `config` subcommand (rather than the `cli` subcommand as before):

```
medusa (-e | -d) config <config_file_path>
```

A Medusa
config file is of the following form:

    [encode]
    input = utests/data/input.txt
    output = utests/data/output.txt
    algo = vigenere
    zip = true # or "TRUE", or "True"

    [decode]
    input = utests/data/output.txt
    output = utests/data/new.txt
    algo = vigenere

_Note: You can write the `[encode]` and `[decode]` parts in whichever order you prefer, and you don't need to put spaces around the equal signs._

Here are the available settings (for each `[encode]` and `[decode]` part). Some are required (they are marked with a `*` sign below) while others are optional (they have default values):

| Parameter  | Description                                                              | Default    |
|------------|--------------------------------------------------------------------------|------------|
| `input` *  | Path to the input file or dir to process.                                |    -       |
| `output` * | Path to the output file or dir (where to write the processed data).      |    -       |
| `algo` *   | Algorithm to use for the encode/decode process.                          |    -       |
| `exclude`  | List of files or folders to ignore during processing.                    | empty list |
| `zip`      | If true, create a zip with the processed data (only for dir processing). | `false`    |
| `verbose`  | If true, print additional logs during process.                           | `false`    |

## Script usage

When you want to use Medusa in a Python script, you can either:

1. run a Medusa process with some args and then some interactive user inputs for on-the-fly keys definition
2. or instantiate a `Medusa` object to use and reuse as much as you want

The first possibility is a nice way of putting some Medusa logic in the middle of your script. You must pass the lib some args:

- the algorithm, the input path, the output path and the action to perform are required (the action can be either "encode" or "decode")
- you may pass optional parameters (see the previous section for details on each): `zip`, `exclude` and `verbose`

Here is an example script using this technique:

```py
from medusa import medusa

if __name__ == '__main__':
    # do some stuff...
    print('Hello world.')

    # run Medusa with some basic args
    medusa(algo='vigenere',
           input='../utests/data/input.txt',
           output='../utests/data/output.txt',
           action='encode')

    # wrap up with some other thing
    print('Goodbye world.')
```

You can also pass a path to a configuration file, like with the CLI:

```py
from medusa import medusa

if __name__ == '__main__':
    # do some stuff...
    print('Hello world.')

    # run Medusa with a config file
    medusa(config='.medusa', action='encode')

    # wrap up with some other thing
    print('Goodbye world.')
```

The second possibility allows you to reuse the same Medusa processor for multiple tasks, like so:

```py
from medusa import Medusa

if __name__ == '__main__':
    processor = Medusa(algo='vigenere',
                       params=dict(key='key',
                                   complement_key='complement_key'))

    # ENCODING
    # encode a string directly
    encoded = processor.encode('hello world')

    # encode some file
    processor.encode_file('../utests/data/input.txt',
                          '../utests/data/output.txt')

    # encode some directory
    processor.encode_dir('../utests/data/input_dir',
                         '../utests/data/output_dir')

    # DECODING
    # decode a string directly
    decoded = processor.decode('ÓÐ×ÑèÜèÝ×Ý')

    # decode some file
    processor.decode_file('../utests/data/output.txt',
                          '../utests/data/new.txt')

    # decode some directory
    processor.decode_dir('../utests/data/output_dir',
                         '../utests/data/new_dir')
```

_Note: whenever you use Medusa in a script, the lib will infer the path of the calling script as the base path for all input/output paths building. For example, if you save the above scripts in an `examples/` folder and then run them, all paths will be relative to this `examples/` subfolder._
