# setup.py

from setuptools import setup, find_packages

setup(
    name='jackdir',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pathspec',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'jackdir=jackdir.main:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Copy directory tree and file contents to clipboard',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
