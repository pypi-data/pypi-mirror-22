from distutils.core import setup
from setuptools import find_packages
setup(
    name = 'pair',
    packages = find_packages(exclude=['test',]),
    install_requires = ['networkx>=1.11',],
    version = '0.2.2',
    description = 'a ladder pairing/matching library',
    author = 'knyte',
    author_email = 'galactaknyte@gmail.com',
    url = 'https://github.com/knyte/pair',
    download_url = 'https://github.com/knyte/pair/tarball/0.2.2',
    license = 'MIT',
    keywords = ['ladder', 'pairing', 'matching', 'Munkres'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
    ],
)
