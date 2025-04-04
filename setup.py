from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stock_quotes_lib",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for fetching and analyzing stock quotes from Alpha Vantage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stock_quotes_lib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.0.0",
    ],
)
