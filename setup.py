from setuptools import setup, find_packages

setup(
    name='jackdir',
    version='1.0.0',
    packages=find_packages(),  # This will automatically find 'jackdir' package
    install_requires=[
        'pyperclip',
        'pathspec'
    ],
    entry_points={
        'console_scripts': [
            'jackdir=jackdir.main:main',  # Note the 'jackdir.main' module reference
        ],
    },
)
