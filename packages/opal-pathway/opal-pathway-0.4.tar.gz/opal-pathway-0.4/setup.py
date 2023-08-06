import os
from setuptools import setup, find_packages

long_desc = """
Opal pathway is a plugin for the Opal web framework. It is a method for
easily creating long forms with custom logic for whatever the user
requires.

Source code and documentation available at https://github.com/openhealthcare/opal-pathway/
"""

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='opal-pathway',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    license='LICENSE',
    description='The pathway OPAL Plugin',
    long_description=README,
    url='http://opal.openhealthcare.org.uk/',
    author='',
    author_email='',
)
