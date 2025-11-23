from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-automation-utils",
    version="0.1.0",
    author="dhiraj",
    author_email="dhirajdas.666@gmail.com",
    description="A python package for automation developers working with Selenium and Appium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhirajdas.666/smart-automation-utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "selenium",
        "Appium-Python-Client"
    ],
)
