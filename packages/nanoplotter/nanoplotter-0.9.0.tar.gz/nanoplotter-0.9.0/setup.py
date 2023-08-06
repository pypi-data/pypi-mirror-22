# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='nanoplotter',
    version='0.9.0',
    description='Plotting functions of Oxford Nanopore sequencing data',
    long_description='Plotting functions of Oxford Nanopore sequencing data.',
    url='https://github.com/wdecoster/nanoplotter',
    author='Wouter De Coster',
    author_email='decosterwouter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='nanopore sequencing plotting quality control',
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn'],
    package_dir={'nanoplotter': 'nanoplotter'})
