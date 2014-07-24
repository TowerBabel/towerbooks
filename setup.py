import codecs
import os
import re
import sys
from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = """

TowerBooks is a library and API to be used for creating ebooks from docx, odt, rtf, and epub files.
The API works by transforming those files into a Book/Chapter Data Model that's extensible to be
used with any standard Python ORM framework.
The API also exports from a Data Model into one of those file formats for upload to Amazon/Apple etc.

"""
# remove the toctree from sphinx index, as it breaks long_description
parts = read("docs", "index.txt").split("split here", 2)
long_description = (parts[0] + long_description + parts[2] +
                    "\n\n" + read("docs", "news.txt"))

setup(name="towerbooks",
      version=find_version('towerbooks', '__init__.py'),
      description="towerbooks imports/exports docx,odt,rtf into/from an ORM Data Model",
      long_description=long_description,
      classifiers=[
        'Development Status :: 1 - Development',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: eReaders',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
      ],
      keywords='ereaders import export amazon apple',
      author='TowerBabel.com',
      author_email='sam@towerbabel.com',
      url='http://www.towerbabel.com',
      license='MIT',
      packages=['towerbooks', ],
      #entry_points=dict(console_scripts=['pip=pip:main', 'pip-%s=pip:main' % sys.version[:3]]),
      test_suite='nose.collector',
      tests_require=['nose', 'virtualenv>=1.7', 'mock'],
      zip_safe=False)
