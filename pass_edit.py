#!/usr/bin/env python3

# pass_edit.py
# A script to rename fields in pass-encrypted files.
# Copyright (c) 2016 Nicholas Narsing <soren121@sorenstudios.com>.
#
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


import argparse
import subprocess
import re
import glob
import os

parser = argparse.ArgumentParser(description='Renames fields in pass-encrypted files.')
parser.add_argument('key_name', type=str, help='GPG key name to encrypt with.')
parser.add_argument('search', type=str, help='The name of the field to replace.')
parser.add_argument('replace', type=str, help='The new name of the field.')
args = parser.parse_args()

pass_path = os.environ['HOME'] + "/.password-store"

if not os.path.exists(pass_path):
    print(".password-store directory not found.")
    exit()

print('Replacing occurrences of  ' + args.search + ' with ' + args.replace)

for file in glob.glob(pass_path + "/*.gpg"):
    decrypt = subprocess.run(["gpg", "-d", file], stdout=subprocess.PIPE)
    content = decrypt.stdout.decode("utf-8")

    rec = re.compile(args.search + ': ', re.MULTILINE)
    content = rec.sub(args.replace + ': ', content)

    gpg_e = ["gpg", "-e", "--batch", "--yes", "-r " + args.key_name, "-o", file]
    encrypt = subprocess.run(gpg_e, input=str.encode(content))

    if encrypt.returncode == 0:
        print('[SUCCESS] ' + os.path.basename(file))
    else:
        print('[FAILURE] ' + os.path.basename(file))
