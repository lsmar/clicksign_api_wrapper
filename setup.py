import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'clicksign_api_wrapper'
AUTHOR = 'LsM'
AUTHOR_EMAIL = 'lucas.smar@gmail.com'
URL = 'https://github.com/lsmar/clicksign_api_wrapper'

LICENSE = 'MIT License'
DESCRIPTION = 'A simple Click Sign API Wrapper.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['requests']

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages())
