from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name        = 'optic',
    version     = '0.0.1',
    description = 'Easily display command-line options',
    url         = 'https://github.com/nmanske/optic',
    author      = 'Nathan Manske',
    author_email= 'nathaniel.manske@gmail.com',
    license     = 'GPLv3',
    scripts     = ['bin/optic']
)
