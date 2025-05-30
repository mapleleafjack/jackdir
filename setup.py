from setuptools import setup, find_packages

setup(
    name='jackdir',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'jackdir': ['client/build/**/*'],
    },
    install_requires=[
        'setuptools',
        'pyperclip',
        'pathspec',
        'flask',
        'Flask-Cors',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'jackdir=jackdir.main:main',
            'jackdir-flask=jackdir.flask_app:run_flask_app',
        ],
    },
)