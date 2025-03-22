from setuptools import setup, find_packages

setup(
    name='jackdir',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'pathspec',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'jackdir=jackdir.main:main',
            'jackdir-flask=jackdir.flask_app:run_flask_app'
        ],
    },
)