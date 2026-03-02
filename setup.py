"""
Setup script for the backtesting engine package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="backtesting_engine",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A flexible backtesting engine for trading strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/backtesting_engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Intended Audience :: Financial and Insurance Industry",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.1.0",
    ],
)