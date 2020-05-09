# Medusa

The Mini Encoding/Decoding Utility with Simple Algorithms (Medusa) is a small Python lib to easily cypher and decypher files or directories using basic cryptography algorithms.

For now, Medusa uses the Vigenere technique.

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

## Advanced usage

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
