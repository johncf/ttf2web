from setuptools import setup
from codecs import open
from os import path
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported.')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ttf2web',
    version='0.9.3',
    description='A tool to optimize fonts for web distribution.',
    long_description=long_description,
    url='https://github.com/johncf/ttf2web',
    author='John C F',
    author_email='john.ch.fr@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ttf woff2 webfont converter splitter css',
    py_modules=['ttf2web'],
    install_requires=['fonttools'],
    entry_points={
        'console_scripts': [
            'ttf2web=ttf2web:main',
        ],
    },
)
