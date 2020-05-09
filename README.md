# Medusa

The Mini Encoding/Decoding Utility with Simple Algorithms (Medusa) is a small Python lib to easily cypher and decypher files or directories using basic cryptography algorithms.

For now, Medusa uses the [Vigenere cypher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher).

This cryptography method is symmetric and it uses a key and a complement key to perform (de)cyphering on a text.

_Note: to make it harder to decypher, Medusa uses a wide range of characters including Unicode characters. So it requires Python 3 to work._

## Install

To install Medusa, use `pip` from the online Github repository:

```
pip install git+https://github.com/MinaPecheux/Medusa.git#egg=medusa
```

This will install the Python lib and also a command-line `medusa` to run it directly in a shell.

## TL;DR

To encrypt a file or a folder, use the Medusa CLI with the `-e` or `--encrypt` argument:

```
medusa -e -i <input_path> -o <output_path>
```

To decrypt a file or a folder, use the Medusa CLI with the `-d` or `--decrypt` argument:

```
medusa -d -i <input_path> -o <output_path>
```

The module will automatically detect whether the input path is a file or a folder; if it is a folder, the directory will be processed recursively.

## Advanced CLI usage

### Autozip output

If you want process a folder and you want the processed output to be zipped automatically, simply add the `-z` or `--zip` argument!

```
medusa -e -i <input_path> -o <output_path> --zip
```

### Exclude specific files or folders

You can also ignore specific files or folders by passing a list of names in the `--exclude` argument:

```
medusa -e -i <input_path> -o <output_path> \
    --exclude __pycache__ .DS_Store
```

### Verbose mode

To get more details on the process, enable the verbose logging mode with the `-v` or `--verbose` argument:

```
medusa -e -i <input_path> -o <output_path> -v
```

## Script usage

When you want to use Medusa in a Python script, you can either:

- run a Medusa process with some args and then some interactive user inputs for on-the-fly keys definition
- or instantiate a `Medusa` object to use and reuse as much as you want

The first possibility is a nice way of putting some Medusa logic in the middle of your script. You must pass the lib some args:

1. the input path, the output path and the action to perform are required (the action can be either "encode" or "decode")
2. you may pass optional parameters (see the previous section for details on each): `exclude`, `zip` and `verbose`

Here is an example script using this technique:

```py
from medusa import medusa

if __name__ == '__main__':
    # do some stuff...
    print('Hello world.')

    # run Medusa with some basic args
    medusa(dict(
        input='data/input.txt',
        output='data/output.txt',
        action='encode'
    ))

    # wrap up with some other thing
    print('Goodbye world.')
```

The second possibility allows you to reuse the same Medusa processor for multiple tasks, like so:

```py
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
```

_Note: whenever you use Medusa in a script, the lib will infer the path of the calling script as the base path for all input/output paths building. For example, if you save the above scripts in an `examples/` folder and then run them, all paths will be relative to this `examples/` subfolder._
