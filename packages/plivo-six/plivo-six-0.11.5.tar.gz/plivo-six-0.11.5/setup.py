from setuptools import setup
import sys

requires = ['requests>=0.10.8', 'six']
if sys.version_info < (2, 6):
    requires.append('simplejson')

setup(
    name = "plivo-six",
    py_modules = ['plivo', "plivoxml"],
    version = "0.11.5",
    description = "Plivo Python library",
    author = "Plivo Team",
    author_email = "hello@plivo.com",
    url = "https://github.com/phuong/plivo-python",
    keywords = ["plivo", "rest"],
    install_requires = requires,
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony"
        ],
    long_description = """\
        Plivo Python library
         """ )
