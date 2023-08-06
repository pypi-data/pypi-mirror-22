"""
Setup of the wostools project.
"""

from setuptools import find_packages
from setuptools import setup

VERSION = '0.1.0'

setup(
    name='wostools',
    version=VERSION,
    author='Oscar D. Arbeláez-Echeverri <@odarbelaeze>, Juan C. Henao-Londoño',
    author_email='odarbelaeze@gmail.com',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    setup_requires=[],
    url='https://github.com/pcm-ca/wostools',
    download_url=f'https://github.com/pcm-ca/wostools/tarball/{VERSION}',
    keywords=['wos', 'bibliography', ],
    description='Utilities for the wos plain text files',
    license='MIT',
    long_description=open('README.rst').read(),
)
