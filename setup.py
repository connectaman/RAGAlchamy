from setuptools import setup, find_packages
from datetime import datetime
import random

requires = open("requirements.txt","r").readlines()

setup(
    name="ragalchemy",
    package_dir={"": "."},
    version="1.0",
    packages=find_packages(),
    url="",
    long_description='A python package to extract, summarize and rag on pptx',
    license="Apache2.0",
    author="Aman Ulla",
    author_email="connectamanulla@gmail.com",
    description="A python package ragalchemy",
    python_requires=">=3.10",
    install_requires=requires,
    include_package_data=True,
)