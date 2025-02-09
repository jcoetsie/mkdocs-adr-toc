from setuptools import setup, find_packages

setup(
    name='mkdocs-adr-toc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    author='Jürgen Coetsiers',
    author_email='jcoetsie@gmail.com',
    description='an MkDocs plugin that genberates a table of contents for ADRs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jcoetsie/mkdocs-adr-toc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
