"""
Setup configuration for the haplogrep_wrapper package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="haplogrep_wrapper",
    version="1.0.0",
    description="Python wrapper for Haplogrep3 CLI tool for mitochondrial haplogroup classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DNABR_AFR Project",
    python_requires=">=3.7",
    packages=find_packages(exclude=["examples", "docs", "tests"]),
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="haplogrep mitochondrial haplogroup bioinformatics vcf genetics",
)
