from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

setup(
    name="pygena",
    version="0.1.0",
    author="Ahmet Atasoglu",
    author_email="ahmetatasoglu98@gmail.com",
    description="A simple genetic algorithm library in Python.",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/atasoglu/pygena",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
