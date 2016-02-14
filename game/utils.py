import os
import random
import shutil
import zipfile
from string import ascii_lowercase as lowers

__author__ = 'hadi'

def generate_random_token(length=32):
    return ''.join([lowers[random.randrange(0, len(lowers))] for i in range(length)])


def make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def extract_zip(file_field, dst):
    make_dir(dst)
    file_field.open('r')
    zf = zipfile.ZipFile(file_field)
    zf.extractall(dst)