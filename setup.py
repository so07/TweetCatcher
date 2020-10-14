from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="tweet_catcher",
    version="0.1.3",
    author="so07",
    author_email="so07git@gmail.it",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.hpc.cineca.it/tweet_catcher",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["twint", "pandas", "langdetect"],
    entry_points={
        "console_scripts": [
            "tweet_catcher=tweet_catcher.catcher_main:main",
            "tweet_cleaner=tweet_catcher.cleaner_main:main",
            "tweet_converter=tweet_catcher.converter_main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
)
