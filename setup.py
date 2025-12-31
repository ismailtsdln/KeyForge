# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='rpg',
    version='2.0.0',
    description='Python Random Password Generator - Secure password and passphrase generation',
    long_description=read_file('README.md') if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/ismailtasdelen/Python-Random-Password-Generator',
    author='İSMAİL TAŞDELEN',
    author_email='pentestdatabase@gmail.com',
    license='MIT',
    
    packages=find_packages(),
    python_requires=">=3.7",
    
    # Console script entry point for 'rpg' command
    entry_points={
        'console_scripts': [
            'rpg=source.cli:main',
        ],
    },
    
    # Core dependencies (no external deps for basic usage)
    install_requires=[],
    
    # Optional dependencies
    extras_require={
        'cli': [
            'colorama>=0.4.6',
            'pyperclip>=1.8.2',
            'qrcode[pil]>=7.4.2',
            'PyYAML>=6.0.1',
        ],
        'web': [
            'Flask>=3.0.0',
            'flask-cors>=4.0.0',
        ],
        'all': [
            'colorama>=0.4.6',
            'pyperclip>=1.8.2',
            'qrcode[pil]>=7.4.2',
            'PyYAML>=6.0.1',
            'Flask>=3.0.0',
            'flask-cors>=4.0.0',
        ],
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    
    keywords='password generator security random passphrase cli web',
    
    zip_safe=False
)

