# -*- coding: utf-8 -*-
import os
import setuptools

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("./requirements.txt", "r", encoding="utf-8") as fh:
    dependences = fh.read().strip().split("\n")

setuptools.setup(
    name="PyDrawille",
    
    version="0.0.1.1",
    
    author="金羿Eilles",
    author_email="EillesWan@outlook.com",
    description="Using Unicode braille characters to draw pixels in console.",
    long_description=open("README.en.md", "r", encoding="utf-8")
    .read()
    .replace("./", "https://github.com/EillesWan/PyDrawille/tree/main/"),
    long_description_content_type="text/markdown",
    url="https://github.com/EillesWan/PyDrawille",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    install_requires=dependences,
    license="MPL 2.0",
)
