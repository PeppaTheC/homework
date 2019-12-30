#!/usr/bin/env python3

from os import walk, path
import hashlib
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-p', type=str, help='Path to directory', dest='input_path')
parser.add_argument('-s', type=str, help='Sha256 of the file(s)', dest='input_sha256')
args = parser.parse_args()

input_path = args.input_path
input_sha256 = args.input_sha256


def get_hash(filename):
    """Gives hash of the given file.

    Args:
        filename: Name of file for which calculates sha256
    """
    with open(filename, "rb") as f:
        text = f.read()
        return hashlib.sha256(text).hexdigest()


def find_files_hash_in_path(input_path, input_sha256):
    """Returns absolute path of the file with hash equal to the given sha256 hash.

    Args:
        input_path: Directory name.
        input_sha256: Given sha256.
    """
    paths = []
    file_hash = 0
    for root, _, files in walk(input_path):
        for file in files:
            abs_path = path.abspath(root)
            abs_name = abs_path + '/' + file
            try:
                file_hash = get_hash(abs_name)
            except:
                pass
            if file_hash == input_sha256:
                print(abs_name)
    return paths


if __name__ == '__main__':
    find_files_hash_in_path(input_path, input_sha256)
