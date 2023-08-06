from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='usncarve',
    version='1.2.2',
    description='A Python script to carve NTFS USN journal records from binary data',
    long_description=long_description,
    url='https://github.com/PoorBillionaire/USN-Record-Carver',
    author='Adam Witt',
    author_email='accidentalassist@gmail.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: Apache Software License'
    ],

    keywords='DFIR NTFS USN Carve Forensics Incident Response Microsoft Windows',
    packages=find_packages(),
    scripts=['usncarve.py']
)
