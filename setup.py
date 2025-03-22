from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chaos",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "pydantic>=2.10.4",
        "pydantic-settings>=2.7.1",
        "pydantic-core>=2.27.2",
        "firecrawl-py>=1.8.0",
        "rich>=13.9.4",
        "openai>=1.66.5",
        "pytest==8.3.4",
        "pytest-asyncio==0.25.3",
        "pytest-cov==6.0.0",
        "pytest-mock==3.14.0",
        "numpy",
    ],
    author="Aditya Patange (AdiPat)",
    author_email="contact.adityapatange@gmail.com",
    description="Chaos is a minimal, AI-based entropy analyzer for Python developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdiPat/chaos",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license_files=("LICENSE",),
)
