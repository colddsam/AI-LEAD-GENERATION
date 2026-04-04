"""
Cold Scout OSS — Setup script for pip-installable package.
Allows: pip install coldscout-oss-x.x.x.tar.gz
"""
import os
from setuptools import setup, find_packages

version = open(os.path.join(os.path.dirname(__file__), "VERSION")).read().strip()

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="coldscout-oss",
    version=version,
    description="Self-hosted AI lead generation pipeline — free tier of Cold Scout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="colddsam",
    author_email="colddsam@gmail.com",
    url="https://github.com/colddsam/coldscout",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "coldscout=run:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
    ],
)
